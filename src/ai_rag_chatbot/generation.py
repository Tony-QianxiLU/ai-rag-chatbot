from typing import Protocol

from langchain_openai import ChatOpenAI

from ai_rag_chatbot.retrieval import RetrievedChunk


class AnswerGenerator(Protocol):
    def generate(self, question: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        pass


class TemplateAnswerGenerator:
    """Offline answer generator used when no LLM API key is configured."""

    def generate(self, question: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        if not retrieved_chunks:
            return "I could not find relevant context in the uploaded documents."

        context = retrieved_chunks[0].chunk.text[:700]
        return (
            "Relevant context was retrieved from the uploaded documents. "
            "Configure OPENAI_API_KEY to enable LLM-generated answers.\n\n"
            f"Question: {question}\n\n"
            f"Top context: {context}"
        )


class OpenAIAnswerGenerator:
    def __init__(self, model: str) -> None:
        self._model = ChatOpenAI(model=model, temperature=0)

    def generate(self, question: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        context = "\n\n".join(
            f"Source: {result.chunk.source}\n{result.chunk.text}" for result in retrieved_chunks
        )
        prompt = (
            "You are a helpful RAG assistant. Answer only from the provided context. "
            "If the context is insufficient, say what is missing.\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context}"
        )
        response = self._model.invoke(prompt)
        return str(response.content)

