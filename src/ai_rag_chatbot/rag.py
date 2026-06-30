from dataclasses import dataclass

from ai_rag_chatbot.chunking import TextChunk, chunk_documents
from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.retrieval import KeywordRetriever
from ai_rag_chatbot.vector_store import ChromaVectorStore


@dataclass(frozen=True)
class RagResponse:
    answer: str
    sources: list[str]


class RagPipeline:
    """Minimal RAG pipeline interface for the first prototype.

    The implementation is intentionally simple in phase 1. Later milestones will
    replace this placeholder with document loading, chunking, embeddings, vector
    retrieval, and LLM response generation.
    """

    def answer(
        self,
        question: str,
        documents: list[LoadedDocument] | None = None,
        chunks: list[TextChunk] | None = None,
        vector_store: ChromaVectorStore | None = None,
    ) -> RagResponse:
        normalized_question = question.strip()
        if not normalized_question:
            return RagResponse(
                answer="Ask a question about your documents to get started.",
                sources=[],
            )

        loaded_documents = documents or []
        if not loaded_documents:
            return RagResponse(
                answer=(
                    "Upload at least one document first. The next milestone will use "
                    "the extracted text for chunking and retrieval."
                ),
                sources=[],
            )

        available_chunks = chunks or chunk_documents(loaded_documents)
        if not available_chunks:
            return RagResponse(
                answer="The uploaded documents did not contain extractable text.",
                sources=[],
            )

        if vector_store:
            vector_store.reset()
            vector_store.add_chunks(available_chunks)
            retrieved_chunks = vector_store.retrieve(normalized_question)
        else:
            retrieved_chunks = KeywordRetriever(available_chunks).retrieve(normalized_question)
        if not retrieved_chunks:
            return RagResponse(
                answer=(
                    f"Documents are loaded and split into {len(available_chunks)} chunks, "
                    "but no matching chunk was found for this question."
                ),
                sources=[],
            )

        context_preview = retrieved_chunks[0].chunk.text[:500]
        source_names = sorted({result.chunk.source for result in retrieved_chunks})
        return RagResponse(
            answer=(
                "Retrieved relevant context from the uploaded documents. "
                "The next milestone will send this context to an LLM for grounded answer generation.\n\n"
                f"Top context preview: {context_preview}"
            ),
            sources=source_names,
        )
