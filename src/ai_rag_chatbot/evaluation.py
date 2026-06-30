from dataclasses import dataclass

from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.rag import RagPipeline


@dataclass(frozen=True)
class EvaluationCase:
    question: str
    expected_source: str


@dataclass(frozen=True)
class EvaluationResult:
    question: str
    expected_source: str
    retrieved_sources: list[str]
    passed: bool


def evaluate_retrieval(
    documents: list[LoadedDocument],
    cases: list[EvaluationCase],
) -> list[EvaluationResult]:
    pipeline = RagPipeline()
    results: list[EvaluationResult] = []

    for case in cases:
        response = pipeline.answer(case.question, documents=documents)
        retrieved_sources = [citation.source for citation in response.citations]
        results.append(
            EvaluationResult(
                question=case.question,
                expected_source=case.expected_source,
                retrieved_sources=retrieved_sources,
                passed=case.expected_source in retrieved_sources,
            )
        )

    return results


def pass_rate(results: list[EvaluationResult]) -> float:
    if not results:
        return 0.0

    passed_count = sum(result.passed for result in results)
    return passed_count / len(results)

