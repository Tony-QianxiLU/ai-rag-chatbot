from dataclasses import dataclass

from ai_rag_chatbot.document_loader import LoadedDocument


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

    def answer(self, question: str, documents: list[LoadedDocument] | None = None) -> RagResponse:
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

        source_names = [document.filename for document in loaded_documents]
        return RagResponse(
            answer=(
                "Documents are loaded and text extraction is working. The next milestone "
                "will split the extracted text into chunks before adding embeddings and retrieval."
            ),
            sources=source_names,
        )
