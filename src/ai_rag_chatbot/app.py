import streamlit as st

from ai_rag_chatbot.chunking import chunk_documents
from ai_rag_chatbot.document_loader import LoadedDocument, load_document
from ai_rag_chatbot.rag import RagPipeline


st.set_page_config(page_title="AI RAG Chatbot", page_icon="AI", layout="wide")

st.title("AI RAG Chatbot")
st.caption("A portfolio project for document-based retrieval-augmented generation.")

with st.sidebar:
    st.header("Project Status")
    st.write("Phase 4: keyword retrieval over document chunks.")
    st.write("Next: embeddings, Chroma, and OpenAI responses.")
    chunk_size = st.slider("Chunk size", min_value=50, max_value=500, value=200, step=50)
    overlap = st.slider("Chunk overlap", min_value=0, max_value=100, value=40, step=10)

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["txt", "pdf"],
    accept_multiple_files=True,
)

documents: list[LoadedDocument] = []
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

question = st.text_input("Ask a question about your documents")

pipeline = RagPipeline()
response = pipeline.answer(question, documents=documents, chunks=chunks)

st.subheader("Answer")
st.write(response.answer)

if response.sources:
    st.subheader("Sources")
    for source in response.sources:
        st.write(f"- {source}")
