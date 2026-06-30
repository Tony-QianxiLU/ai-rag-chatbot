from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean

from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.rag import RagPipeline


@dataclass(frozen=True)
class EvaluationCase:
    id: str
    question: str
    expected_source: str
    expected_answer_terms: list[str]
    expected_citation_count: int = 1


@dataclass(frozen=True)
class EvaluationResult:
    id: str
    question: str
    expected_source: str
    retrieved_sources: list[str]
    answer: str
    latency_ms: float
    retrieval_passed: bool
    citation_passed: bool
    groundedness_passed: bool
    passed: bool


@dataclass(frozen=True)
class EvaluationSummary:
    total_cases: int
    passed_cases: int
    retrieval_accuracy: float
    citation_coverage: float
    groundedness_rate: float
    overall_pass_rate: float
    average_latency_ms: float


@dataclass(frozen=True)
class EvaluationReport:
    summary: EvaluationSummary
    results: list[EvaluationResult]


def load_evaluation_cases(path: Path) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            payload = json.loads(stripped)
            try:
                cases.append(
                    EvaluationCase(
                        id=payload["id"],
                        question=payload["question"],
                        expected_source=payload["expected_source"],
                        expected_answer_terms=list(payload["expected_answer_terms"]),
                        expected_citation_count=int(payload.get("expected_citation_count", 1)),
                    )
                )
            except KeyError as error:
                raise ValueError(f"Missing required field on line {line_number}: {error}") from error

    return cases


def evaluate_rag(
    documents: list[LoadedDocument],
    cases: list[EvaluationCase],
    pipeline: RagPipeline | None = None,
) -> EvaluationReport:
    evaluator_pipeline = pipeline or RagPipeline()
    results: list[EvaluationResult] = []

    for case in cases:
        started_at = time.perf_counter()
        response = evaluator_pipeline.answer(case.question, documents=documents)
        latency_ms = (time.perf_counter() - started_at) * 1000

        retrieved_sources = [citation.source for citation in response.citations]
        answer_lower = response.answer.lower()
        retrieval_passed = case.expected_source in retrieved_sources
        citation_passed = len(response.citations) >= case.expected_citation_count
        groundedness_passed = all(
            expected_term.lower() in answer_lower for expected_term in case.expected_answer_terms
        )
        passed = retrieval_passed and citation_passed and groundedness_passed

        results.append(
            EvaluationResult(
                id=case.id,
                question=case.question,
                expected_source=case.expected_source,
                retrieved_sources=retrieved_sources,
                answer=response.answer,
                latency_ms=latency_ms,
                retrieval_passed=retrieval_passed,
                citation_passed=citation_passed,
                groundedness_passed=groundedness_passed,
                passed=passed,
            )
        )

    return EvaluationReport(summary=summarize_results(results), results=results)


def evaluate_retrieval(
    documents: list[LoadedDocument],
    cases: list[EvaluationCase],
) -> list[EvaluationResult]:
    return evaluate_rag(documents, cases).results


def summarize_results(results: list[EvaluationResult]) -> EvaluationSummary:
    total_cases = len(results)
    if total_cases == 0:
        return EvaluationSummary(
            total_cases=0,
            passed_cases=0,
            retrieval_accuracy=0.0,
            citation_coverage=0.0,
            groundedness_rate=0.0,
            overall_pass_rate=0.0,
            average_latency_ms=0.0,
        )

    passed_cases = sum(result.passed for result in results)
    return EvaluationSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        retrieval_accuracy=pass_rate_for(results, "retrieval_passed"),
        citation_coverage=pass_rate_for(results, "citation_passed"),
        groundedness_rate=pass_rate_for(results, "groundedness_passed"),
        overall_pass_rate=passed_cases / total_cases,
        average_latency_ms=mean(result.latency_ms for result in results),
    )


def pass_rate(results: list[EvaluationResult]) -> float:
    if not results:
        return 0.0

    return sum(result.passed for result in results) / len(results)


def pass_rate_for(results: list[EvaluationResult], field_name: str) -> float:
    if not results:
        return 0.0

    return sum(bool(getattr(result, field_name)) for result in results) / len(results)


def report_to_dict(report: EvaluationReport) -> dict[str, object]:
    return {
        "summary": asdict(report.summary),
        "results": [asdict(result) for result in report.results],
    }


def write_json_report(report: EvaluationReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")


def render_markdown_report(report: EvaluationReport) -> str:
    summary = report.summary
    lines = [
        "# RAG Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Total cases: {summary.total_cases}",
        f"- Passed cases: {summary.passed_cases}",
        f"- Retrieval accuracy: {summary.retrieval_accuracy:.0%}",
        f"- Citation coverage: {summary.citation_coverage:.0%}",
        f"- Groundedness rate: {summary.groundedness_rate:.0%}",
        f"- Overall pass rate: {summary.overall_pass_rate:.0%}",
        f"- Average latency: {summary.average_latency_ms:.1f} ms",
        "",
        "## Case Results",
        "",
        "| Case | Retrieval | Citations | Grounded | Latency | Expected source | Retrieved sources |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]

    for result in report.results:
        lines.append(
            "| "
            f"{result.id} | "
            f"{_format_status(result.retrieval_passed)} | "
            f"{_format_status(result.citation_passed)} | "
            f"{_format_status(result.groundedness_passed)} | "
            f"{result.latency_ms:.1f} ms | "
            f"{result.expected_source} | "
            f"{', '.join(result.retrieved_sources) or 'None'} |"
        )

    return "\n".join(lines) + "\n"


def write_markdown_report(report: EvaluationReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown_report(report), encoding="utf-8")


def _format_status(passed: bool) -> str:
    return "PASS" if passed else "FAIL"
