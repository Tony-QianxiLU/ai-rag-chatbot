import streamlit as st

from ai_rag_chatbot.document_loader import LoadedDocument, load_document
from ai_rag_chatbot.rag import RagPipeline


st.set_page_config(page_title="AI RAG Chatbot", page_icon="AI", layout="wide")

st.title("AI RAG Chatbot")
st.caption("A portfolio project for document-based retrieval-augmented generation.")

with st.sidebar:
    st.header("Project Status")
    st.write("Phase 2: document upload and text extraction.")
    st.write("Next: chunking, embeddings, Chroma, and OpenAI responses.")

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

question = st.text_input("Ask a question about your documents")

pipeline = RagPipeline()
response = pipeline.answer(question, documents=documents)

st.subheader("Answer")
st.write(response.answer)

if response.sources:
    st.subheader("Sources")
    for source in response.sources:
        st.write(f"- {source}")
