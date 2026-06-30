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

