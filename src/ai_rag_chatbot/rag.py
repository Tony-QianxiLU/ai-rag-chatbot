from dataclasses import dataclass


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

    def answer(self, question: str) -> RagResponse:
        normalized_question = question.strip()
        if not normalized_question:
            return RagResponse(
                answer="Ask a question about your documents to get started.",
                sources=[],
            )

        return RagResponse(
            answer=(
                "This is the phase 1 prototype. The next milestone will connect "
                "document upload, embeddings, retrieval, and an LLM-generated answer."
            ),
            sources=["Project roadmap"],
        )

