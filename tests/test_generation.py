from ai_rag_chatbot.chunking import TextChunk
from ai_rag_chatbot.generation import TemplateAnswerGenerator
from ai_rag_chatbot.retrieval import RetrievedChunk


def test_template_answer_generator_uses_retrieved_context() -> None:
    chunk = TextChunk(
        id="notes.txt:0",
        source="notes.txt",
        index=0,
        text="RAG combines retrieval with generation.",
    )
    retrieved = [RetrievedChunk(chunk=chunk, score=2)]

    answer = TemplateAnswerGenerator().generate("What is RAG?", retrieved)

    assert "Question: What is RAG?" in answer
    assert "RAG combines retrieval" in answer


def test_template_answer_generator_handles_empty_context() -> None:
    answer = TemplateAnswerGenerator().generate("What is RAG?", [])

    assert "could not find relevant context" in answer
