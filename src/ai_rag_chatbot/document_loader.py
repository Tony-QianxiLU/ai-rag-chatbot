from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader


@dataclass(frozen=True)
class LoadedDocument:
    filename: str
    text: str

    @property
    def character_count(self) -> int:
        return len(self.text)


def load_text_file(filename: str, content: bytes) -> LoadedDocument:
    text = content.decode("utf-8", errors="replace").strip()
    return LoadedDocument(filename=filename, text=text)


def load_pdf_file(filename: str, content: bytes) -> LoadedDocument:
    reader = PdfReader(BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n\n".join(page.strip() for page in pages if page.strip())
    return LoadedDocument(filename=filename, text=text)


def load_document(filename: str, content: bytes) -> LoadedDocument:
    lower_name = filename.lower()

    if lower_name.endswith(".txt"):
        return load_text_file(filename, content)

    if lower_name.endswith(".pdf"):
        return load_pdf_file(filename, content)

    supported_types = ".txt, .pdf"
    raise ValueError(f"Unsupported file type. Supported types: {supported_types}")
