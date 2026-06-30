# Demo Walkthrough

## What To Show

This demo shows a RAG application moving through the core pipeline:

1. Upload a `.txt` or `.pdf` document.
2. Extract text.
3. Split text into chunks.
4. Retrieve relevant chunks.
5. Generate a grounded answer.
6. Show citations with source, chunk id, score, and preview.

## Suggested Interview Demo

Use a short text file:

```text
Retrieval augmented generation combines search with language generation. It helps models answer using external documents instead of relying only on model memory.
```

Ask:

```text
What does retrieval augmented generation combine?
```

Expected behavior:

- The app loads the document.
- The app creates chunks.
- The retriever finds the relevant chunk.
- The answer is grounded in the uploaded text.
- The citation shows the source document and chunk metadata.

## What This Proves

- I understand the major components of RAG.
- I can build a working app around document upload, retrieval, and answer generation.
- I can design systems that run locally without paid API calls but can switch to OpenAI integrations.
- I can add evaluation and CI instead of stopping at a visual demo.

## 60-90 Second Walkthrough Script

This is the interview-ready version:

1. "This is an AI RAG Chatbot. The goal is to answer questions from uploaded documents while keeping the answer grounded in retrieved context and citations."
2. "The architecture is `upload -> chunk -> retrieve -> generate -> cite`. I separated the UI, document loader, chunker, retriever, vector store, generator, and evaluation code so each part is testable."
3. "The live demo includes a sample document and default question, so an interviewer can test it immediately without uploading a file."
4. "The app supports deterministic keyword retrieval, local vector retrieval, and optional OpenAI vector search when an API key is configured."
5. "The v0.3.0 evaluation suite checks retrieval accuracy, citation coverage, grounded answer terms, and latency, then writes Markdown and JSON reports."
6. "This project proves I can build, test, deploy, evaluate, document, and explain a production-minded GenAI application."

## Video Asset

[Watch the 63-second walkthrough video](video/rag-chatbot-walkthrough.mp4)
