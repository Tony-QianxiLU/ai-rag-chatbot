from dataclasses import dataclass

from ai_rag_chatbot.document_loader import LoadedDocument


@dataclass(frozen=True)
class TextChunk:
    id: str
    source: str
    index: int
    text: str

    @property
    def word_count(self) -> int:
        return len(self.text.split())


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 200,
    overlap: int = 40,
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    step = chunk_size - overlap

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(
            TextChunk(
                id=f"{source}:{index}",
                source=source,
                index=index,
                text=" ".join(chunk_words),
            )
        )
        index += 1
        start += step

    return chunks


def chunk_documents(
    documents: list[LoadedDocument],
    chunk_size: int = 200,
    overlap: int = 40,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for document in documents:
        chunks.extend(
            chunk_text(
                text=document.text,
                source=document.filename,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )
    return chunks

