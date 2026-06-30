from ai_rag_chatbot.rag import RagPipeline


def test_empty_question_returns_getting_started_message() -> None:
    response = RagPipeline().answer("")

    assert "Ask a question" in response.answer
    assert response.sources == []


def test_question_returns_phase_one_response() -> None:
    response = RagPipeline().answer("What is RAG?")

    assert "phase 1 prototype" in response.answer
    assert response.sources == ["Project roadmap"]

