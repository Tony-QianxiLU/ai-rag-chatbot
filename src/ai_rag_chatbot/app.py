import streamlit as st

from ai_rag_chatbot.chunking import chunk_documents
from ai_rag_chatbot.config import settings
from ai_rag_chatbot.demo_data import SAMPLE_DOCUMENT, SAMPLE_QUESTION
from ai_rag_chatbot.document_loader import LoadedDocument, load_document
from ai_rag_chatbot.embeddings import HashEmbeddingProvider, OpenAIEmbeddingProvider
from ai_rag_chatbot.generation import OpenAIAnswerGenerator, TemplateAnswerGenerator
from ai_rag_chatbot.rag import RagPipeline
from ai_rag_chatbot.vector_store import ChromaVectorStore


st.set_page_config(page_title="AI RAG Chatbot", page_icon="AI", layout="wide")

st.title("AI RAG Chatbot")
st.caption("A portfolio project for document-based retrieval-augmented generation.")

with st.sidebar:
    st.header("Project Status")
    st.write("Portfolio-ready RAG app with public deployment.")
    chunk_size = st.slider("Chunk size", min_value=50, max_value=500, value=200, step=50)
    overlap = st.slider("Chunk overlap", min_value=0, max_value=100, value=40, step=10)
    retrieval_mode = st.radio(
        "Retrieval mode",
        options=["Keyword", "Local vector", "OpenAI vector"],
    )
    use_sample_document = st.checkbox("Load sample document", value=True)

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["txt", "pdf"],
    accept_multiple_files=True,
)

documents: list[LoadedDocument] = []
if use_sample_document:
    documents.append(SAMPLE_DOCUMENT)

for uploaded_file in uploaded_files:
    try:
        documents.append(load_document(uploaded_file.name, uploaded_file.getvalue()))
    except ValueError as error:
        st.error(f"{uploaded_file.name}: {error}")

if documents:
    st.subheader("Loaded Documents")
    for document in documents:
        with st.expander(f"{document.filename} ({document.character_count:,} characters)"):
            preview = document.text[:2_000] or "No extractable text found."
            st.text(preview)

chunks = chunk_documents(documents, chunk_size=chunk_size, overlap=overlap) if documents else []

if chunks:
    st.subheader("Chunks")
    st.write(f"Created {len(chunks)} chunks from {len(documents)} document(s).")
    with st.expander("Preview first chunk"):
        first_chunk = chunks[0]
        st.write(f"Source: {first_chunk.source}")
        st.write(f"Words: {first_chunk.word_count}")
        st.text(first_chunk.text[:2_000])

question = st.text_input(
    "Ask a question about your documents",
    value=SAMPLE_QUESTION if use_sample_document else "",
)

pipeline = RagPipeline()

vector_store = None
if chunks and retrieval_mode in {"Local vector", "OpenAI vector"}:
    if retrieval_mode == "OpenAI vector" and settings.openai_api_key:
        embedding_provider = OpenAIEmbeddingProvider(model=settings.embedding_model)
    else:
        embedding_provider = HashEmbeddingProvider()
        if retrieval_mode == "OpenAI vector":
            st.warning("OPENAI_API_KEY is not set. Falling back to local hash embeddings.")

    vector_store = ChromaVectorStore(
        persist_dir=settings.chroma_persist_dir,
        embedding_provider=embedding_provider,
    )

answer_generator = (
    OpenAIAnswerGenerator(model=settings.openai_model)
    if settings.openai_api_key
    else TemplateAnswerGenerator()
)

try:
    response = pipeline.answer(
        question,
        documents=documents,
        chunks=chunks,
        vector_store=vector_store,
        answer_generator=answer_generator,
    )
except Exception as error:
    st.subheader("Answer")
    st.error(f"RAG pipeline failed: {error}")
else:
    st.subheader("Answer")
    st.write(response.answer)

    if response.citations:
        st.subheader("Citations")
        for citation in response.citations:
            with st.expander(f"{citation.source} | {citation.chunk_id} | score {citation.score}"):
                st.write(citation.preview)
    elif response.sources:
        st.subheader("Sources")
        for source in response.sources:
            st.write(f"- {source}")
