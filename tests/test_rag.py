from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.rag import RagPipeline


def test_empty_question_returns_getting_started_message() -> None:
    response = RagPipeline().answer("")

    assert "Ask a question" in response.answer
    assert response.sources == []


def test_question_returns_phase_one_response() -> None:
    response = RagPipeline().answer(
        "What is RAG?",
        documents=[LoadedDocument(filename="notes.txt", text="RAG means retrieval.")],
    )

    assert "Relevant context was retrieved" in response.answer
    assert response.sources == ["notes.txt"]


def test_question_without_documents_requests_upload() -> None:
    response = RagPipeline().answer("What is RAG?")

    assert "Upload at least one document" in response.answer
    assert response.sources == []


def test_question_with_no_matching_chunks_returns_no_match_message() -> None:
    response = RagPipeline().answer(
        "What is vector search?",
        documents=[LoadedDocument(filename="notes.txt", text="Bananas and apples.")],
    )

    assert "no matching chunk" in response.answer
    assert response.sources == []
