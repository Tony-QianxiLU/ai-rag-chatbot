from pathlib import Path

from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.evaluate import BENCHMARK_DOCUMENTS
from ai_rag_chatbot.evaluation import (
    EvaluationCase,
    EvaluationResult,
    evaluate_rag,
    evaluate_retrieval,
    load_evaluation_cases,
    pass_rate,
    render_markdown_report,
    write_json_report,
    write_markdown_report,
)


def test_evaluate_rag_scores_retrieval_citations_and_groundedness() -> None:
    documents = [
        LoadedDocument(filename="rag.txt", text="RAG uses retrieval and generation."),
        LoadedDocument(filename="agents.txt", text="Agents use tools and planning."),
    ]
    cases = [
        EvaluationCase(
            id="retrieval",
            question="What uses retrieval?",
            expected_source="rag.txt",
            expected_answer_terms=["retrieval", "generation"],
        )
    ]

    report = evaluate_rag(documents, cases)

    assert report.summary.total_cases == 1
    assert report.summary.passed_cases == 1
    assert report.summary.retrieval_accuracy == 1.0
    assert report.summary.citation_coverage == 1.0
    assert report.summary.groundedness_rate == 1.0
    assert report.summary.average_latency_ms >= 0.0
    assert report.results[0].passed is True
    assert pass_rate(report.results) == 1.0


def test_evaluate_retrieval_keeps_backward_compatible_result_list() -> None:
    documents = [LoadedDocument(filename="rag.txt", text="RAG uses retrieval and generation.")]
    cases = [
        EvaluationCase(
            id="legacy",
            question="What uses retrieval?",
            expected_source="rag.txt",
            expected_answer_terms=["retrieval"],
        )
    ]

    results = evaluate_retrieval(documents, cases)

    assert len(results) == 1
    assert results[0].expected_source == "rag.txt"
    assert results[0].retrieval_passed is True


def test_load_evaluation_cases_reads_jsonl() -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))

    assert len(cases) == 4
    assert cases[0].id == "rag-retrieval"
    assert cases[0].expected_source == "rag-architecture.txt"
    assert "citations" in cases[0].expected_answer_terms


def test_benchmark_documents_pass_current_evaluation_suite() -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))

    report = evaluate_rag(BENCHMARK_DOCUMENTS, cases)

    assert report.summary.total_cases == 4
    assert report.summary.overall_pass_rate == 1.0
    assert all(result.passed for result in report.results)


def test_render_markdown_report_includes_summary_and_cases() -> None:
    result = EvaluationResult(
        id="case-1",
        question="Question?",
        expected_source="source.txt",
        retrieved_sources=["source.txt"],
        answer="Answer from source.",
        latency_ms=2.5,
        retrieval_passed=True,
        citation_passed=True,
        groundedness_passed=True,
        passed=True,
    )
    report = evaluate_rag(
        [LoadedDocument(filename="source.txt", text="Answer from source.")],
        [
            EvaluationCase(
                id="case-1",
                question="Question?",
                expected_source="source.txt",
                expected_answer_terms=["answer"],
            )
        ],
    )
    report = type(report)(summary=report.summary, results=[result])

    markdown = render_markdown_report(report)

    assert "# RAG Evaluation Report" in markdown
    assert "Retrieval accuracy" in markdown
    assert "| case-1 | PASS | PASS | PASS | 2.5 ms | source.txt | source.txt |" in markdown


def test_write_reports_creates_json_and_markdown(tmp_path: Path) -> None:
    cases = load_evaluation_cases(Path("data/evaluation_cases.jsonl"))
    report = evaluate_rag(BENCHMARK_DOCUMENTS, cases)
    json_path = tmp_path / "report.json"
    markdown_path = tmp_path / "report.md"

    write_json_report(report, json_path)
    write_markdown_report(report, markdown_path)

    assert '"overall_pass_rate": 1.0' in json_path.read_text(encoding="utf-8")
    assert "## Case Results" in markdown_path.read_text(encoding="utf-8")


def test_pass_rate_handles_empty_results() -> None:
    assert pass_rate([]) == 0.0
