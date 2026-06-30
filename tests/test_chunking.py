import pytest

from ai_rag_chatbot.chunking import chunk_documents, chunk_text
from ai_rag_chatbot.document_loader import LoadedDocument


def test_chunk_text_splits_words_with_overlap() -> None:
    text = "one two three four five six"

    chunks = chunk_text(text, source="notes.txt", chunk_size=3, overlap=1)

    assert [chunk.text for chunk in chunks] == [
        "one two three",
        "three four five",
        "five six",
    ]
    assert chunks[0].id == "notes.txt:0"
    assert chunks[1].index == 1


def test_chunk_documents_keeps_source_names() -> None:
    documents = [
        LoadedDocument(filename="a.txt", text="alpha beta gamma"),
        LoadedDocument(filename="b.txt", text="delta epsilon zeta"),
    ]

    chunks = chunk_documents(documents, chunk_size=10, overlap=0)

    assert [chunk.source for chunk in chunks] == ["a.txt", "b.txt"]


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError, match="overlap must be smaller"):
        chunk_text("hello world", source="notes.txt", chunk_size=10, overlap=10)
