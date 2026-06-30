import streamlit as st

from ai_rag_chatbot.rag import RagPipeline


st.set_page_config(page_title="AI RAG Chatbot", page_icon="AI", layout="wide")

st.title("AI RAG Chatbot")
st.caption("A portfolio project for document-based retrieval-augmented generation.")

with st.sidebar:
    st.header("Project Status")
    st.write("Phase 1: Streamlit prototype and RAG pipeline skeleton.")
    st.write("Next: document upload, chunking, embeddings, Chroma, and OpenAI responses.")

question = st.text_input("Ask a question about your documents")

pipeline = RagPipeline()
response = pipeline.answer(question)

st.subheader("Answer")
st.write(response.answer)

if response.sources:
    st.subheader("Sources")
    for source in response.sources:
        st.write(f"- {source}")
