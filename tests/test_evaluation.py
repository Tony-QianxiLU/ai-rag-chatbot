from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.evaluation import EvaluationCase, evaluate_retrieval, pass_rate


def test_evaluate_retrieval_marks_expected_source_as_passed() -> None:
    documents = [
        LoadedDocument(filename="rag.txt", text="RAG uses retrieval and generation."),
        LoadedDocument(filename="agents.txt", text="Agents use tools and planning."),
    ]
    cases = [EvaluationCase(question="What uses retrieval?", expected_source="rag.txt")]

    results = evaluate_retrieval(documents, cases)

    assert len(results) == 1
    assert results[0].passed is True
    assert pass_rate(results) == 1.0


def test_pass_rate_handles_empty_results() -> None:
    assert pass_rate([]) == 0.0

