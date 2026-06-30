from dataclasses import dataclass

from ai_rag_chatbot.chunking import TextChunk, chunk_documents
from ai_rag_chatbot.document_loader import LoadedDocument
from ai_rag_chatbot.generation import AnswerGenerator, TemplateAnswerGenerator
from ai_rag_chatbot.retrieval import KeywordRetriever
from ai_rag_chatbot.vector_store import ChromaVectorStore


@dataclass(frozen=True)
class SourceReference:
    source: str
    chunk_id: str
    score: int
    preview: str


@dataclass(frozen=True)
class RagResponse:
    answer: str
    sources: list[str]
    citations: list[SourceReference]


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
        answer_generator: AnswerGenerator | None = None,
    ) -> RagResponse:
        normalized_question = question.strip()
        if not normalized_question:
            return RagResponse(
                answer="Ask a question about your documents to get started.",
                sources=[],
                citations=[],
            )

        loaded_documents = documents or []
        if not loaded_documents:
            return RagResponse(
                answer=(
                    "Upload at least one document first. The next milestone will use "
                    "the extracted text for chunking and retrieval."
                ),
                sources=[],
                citations=[],
            )

        available_chunks = chunks or chunk_documents(loaded_documents)
        if not available_chunks:
            return RagResponse(
                answer="The uploaded documents did not contain extractable text.",
                sources=[],
                citations=[],
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
                citations=[],
            )

        source_names = sorted({result.chunk.source for result in retrieved_chunks})
        citations = [
            SourceReference(
                source=result.chunk.source,
                chunk_id=result.chunk.id,
                score=result.score,
                preview=result.chunk.text[:240],
            )
            for result in retrieved_chunks
        ]
        generator = answer_generator or TemplateAnswerGenerator()
        return RagResponse(
            answer=generator.generate(normalized_question, retrieved_chunks),
            sources=source_names,
            citations=citations,
        )
