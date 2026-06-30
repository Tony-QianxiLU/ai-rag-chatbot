# Architecture

## Goal

The goal of this project is to build a document-based chatbot that can answer questions using retrieved context from uploaded documents.

## Phase 1

The current phase creates a clean local application skeleton:

- Streamlit UI
- RAG pipeline interface
- Settings management
- Tests
- Documentation

## Target RAG Flow

1. Upload documents.
2. Extract text.
3. Split text into chunks.
4. Generate embeddings for each chunk.
5. Store embeddings in Chroma.
6. Retrieve relevant chunks for a user question.
7. Generate an answer with an OpenAI model.
8. Return answer and source references.

