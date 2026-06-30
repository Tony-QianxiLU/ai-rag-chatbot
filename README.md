# AI RAG Chatbot

[![CI](https://github.com/Tony-QianxiLU/ai-rag-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/Tony-QianxiLU/ai-rag-chatbot/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Tony-QianxiLU/ai-rag-chatbot)](https://github.com/Tony-QianxiLU/ai-rag-chatbot/releases)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Live Demo](https://img.shields.io/badge/live%20demo-Streamlit-ff4b4b)](https://ry84fwqnk4abfhufqkhrmz.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-minded retrieval-augmented generation (RAG) chatbot that answers questions from uploaded `.txt` and `.pdf` documents, retrieves grounded context, and returns source citations through a Streamlit interface.

This project is part of my AI engineering portfolio. It is designed to demonstrate practical GenAI application engineering: document ingestion, chunking, retrieval, vector storage, optional OpenAI integration, deterministic local fallbacks, tests, CI, deployment, and interview-ready documentation.

## Live Demo

[Open the deployed Streamlit app](https://ry84fwqnk4abfhufqkhrmz.streamlit.app/)

## Features

- Upload `.txt` and `.pdf` documents.
- Use a built-in sample document for instant demos.
- Extract and preview document text.
- Split documents into configurable overlapping chunks.
- Retrieve context with deterministic keyword search.
- Retrieve context with Chroma vector search.
- Use local deterministic hash embeddings for offline development and CI.
- Enable OpenAI embeddings when `OPENAI_API_KEY` is configured.
- Generate grounded answers with source citations.
- Fall back to template answers when no paid API key is available.
- Evaluate retrieval quality with simple pass-rate helpers.
- Run quality checks with Ruff, pytest, and GitHub Actions.
- Deploy publicly on Streamlit Community Cloud.

## Architecture

```mermaid
flowchart TD
    user["User"] --> ui["Streamlit UI"]
    ui --> loader["Document Loader"]
    loader --> chunker["Text Chunker"]
    chunker --> retriever["Retriever"]
    retriever --> embedder["Embedding Provider"]
    embedder --> vector_db["Vector Database: Chroma"]
    vector_db --> generator["LLM or Template Generator"]
    generator --> answer["Answer with Citations"]
```

## RAG Pipeline

```text
User
  |
  v
Streamlit
  |
  v
Retriever
  |
  v
Embedding
  |
  v
Vector Database
  |
  v
LLM
  |
  v
Answer
```

## Tech Stack

- Python 3.12
- Streamlit
- LangChain
- LangChain OpenAI
- Chroma
- pypdf
- pydantic-settings
- pytest
- Ruff
- uv
- GitHub Actions

## Folder Structure

```text
ai-rag-chatbot/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   `-- workflows/
|-- docs/
|   |-- demo/
|   |-- images/
|   |-- architecture.md
|   |-- deployment.md
|   |-- evaluation.md
|   `-- walkthrough.md
|-- src/
|   `-- ai_rag_chatbot/
|       |-- app.py
|       |-- chunking.py
|       |-- config.py
|       |-- demo_data.py
|       |-- document_loader.py
|       |-- embeddings.py
|       |-- evaluation.py
|       |-- generation.py
|       |-- rag.py
|       |-- retrieval.py
|       `-- vector_store.py
|-- tests/
|-- .env.example
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

## Installation

Install `uv` if needed:

```bash
brew install uv
```

Install dependencies:

```bash
uv sync
```

## Environment Variables

Create a local `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Supported variables:

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | No | Enables OpenAI embeddings and answer generation. |
| `OPENAI_MODEL` | No | Chat model for grounded answer generation. |
| `EMBEDDING_MODEL` | No | OpenAI embedding model. |
| `CHROMA_PERSIST_DIR` | No | Local Chroma persistence directory. |

Never commit real API keys.

## Quick Start

Run the Streamlit app:

```bash
PYTHONPATH=src uv run streamlit run src/ai_rag_chatbot/app.py
```

Run quality checks:

```bash
uv run ruff check .
uv run pytest
```

## Screenshots

![AI RAG Chatbot screenshot](docs/images/rag-chatbot.png)

Fallback screenshot:

![AI RAG Chatbot Streamlit UI](docs/assets/streamlit-home.png)

## Demo GIF

![AI RAG Chatbot demo](docs/demo/rag-chatbot-demo.gif)

## Usage

1. Open the app.
2. Keep `Load sample document` enabled for a fast demo, or upload your own `.txt` or `.pdf`.
3. Choose a retrieval mode:
   - `Keyword` for deterministic local search.
   - `Local vector` for offline vector retrieval.
   - `OpenAI vector` when an OpenAI API key is configured.
4. Ask a question about the uploaded documents.
5. Review the answer and citations.

## Example Prompts

```text
What does retrieval augmented generation combine?
```

```text
Why are citations useful in a RAG system?
```

```text
How does the app reduce hallucination risk?
```

## Example Output

```text
Relevant context was retrieved from the uploaded documents. Configure OPENAI_API_KEY
to enable LLM-generated answers.

Question: What does retrieval augmented generation combine?

Top context: Retrieval augmented generation combines search with language generation...
```

Citation:

```text
sample-rag-brief.txt | sample-rag-brief.txt:0 | score 4
```

## Technical Highlights

- Clean separation between UI, ingestion, chunking, retrieval, generation, and evaluation.
- Local deterministic embeddings make tests reproducible without paid API calls.
- Optional OpenAI components can be enabled through environment variables.
- Source references are returned as structured dataclasses, not loose strings.
- Chroma integration uses explicit replace semantics for predictable demo behavior.
- Tests cover chunking, document loading, embeddings, retrieval, generation, vector store behavior, and evaluation.

## Deployment

The public demo is deployed on Streamlit Community Cloud.

Suggested Streamlit settings:

- Repository: `Tony-QianxiLU/ai-rag-chatbot`
- Branch: `main`
- Main file path: `src/ai_rag_chatbot/app.py`
- Python version: `3.12`

Optional secrets:

```toml
OPENAI_API_KEY = "..."
OPENAI_MODEL = "gpt-4.1-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
```

## Future Improvements

- Add a curated retrieval evaluation dataset.
- Track precision, recall, citation quality, latency, and cost.
- Add persistent document collections with user sessions.
- Add hybrid retrieval and reranking.
- Add observability dashboards for retrieval and generation failures.
- Add a FastAPI backend for production deployment.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements

- Streamlit for fast AI app deployment.
- LangChain and LangChain OpenAI for LLM application primitives.
- Chroma for local vector search.
- OpenAI for optional embeddings and grounded answer generation.
