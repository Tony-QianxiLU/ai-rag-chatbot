# Architecture

## Goal

The goal of this project is to build a document-based chatbot that can answer questions using retrieved context from uploaded documents.

## Current Phase

The current phase adds document upload, text extraction, chunking, retrieval, vector storage, and answer generation:

- Streamlit UI
- RAG pipeline interface
- Settings management
- `.txt` text extraction
- `.pdf` text extraction
- Document preview
- Configurable chunk size and overlap
- Keyword retrieval over chunks
- Chroma vector storage
- Local hash embeddings for development
- Optional OpenAI embeddings for production-style retrieval
- Offline template answer generation
- Optional OpenAI grounded answer generation
- Source citations with chunk metadata
- Retrieval evaluation helpers
- CI and deployment documentation
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
