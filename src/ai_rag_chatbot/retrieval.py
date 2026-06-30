import re
from dataclasses import dataclass

from ai_rag_chatbot.chunking import TextChunk


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: TextChunk
    score: int


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text)}


class KeywordRetriever:
    """Simple deterministic retriever used before vector search is added."""

    def __init__(self, chunks: list[TextChunk]) -> None:
        self._chunks = chunks

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        results: list[RetrievedChunk] = []
        for chunk in self._chunks:
            chunk_tokens = tokenize(chunk.text)
            score = len(query_tokens.intersection(chunk_tokens))
            if score > 0:
                results.append(RetrievedChunk(chunk=chunk, score=score))

        return sorted(results, key=lambda result: result.score, reverse=True)[:top_k]

