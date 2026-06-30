import pytest

from ai_rag_chatbot.document_loader import load_document, load_text_file


def test_load_text_file_decodes_utf8_content() -> None:
    document = load_text_file("notes.txt", "Hello RAG".encode())

    assert document.filename == "notes.txt"
    assert document.text == "Hello RAG"
    assert document.character_count == 9


def test_load_document_rejects_unsupported_file_type() -> None:
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document("notes.docx", b"content")


def test_load_document_rejects_empty_upload() -> None:
    with pytest.raises(ValueError, match="empty"):
        load_document("notes.txt", b"")
