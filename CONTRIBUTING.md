# Contributing

Thanks for your interest in improving AI RAG Chatbot.

## Development Setup

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/ai_rag_chatbot/app.py
```

## Quality Checks

Run these before opening a pull request:

```bash
uv run ruff check .
uv run pytest
```

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Add or update tests for behavior changes.
- Update documentation when user-facing behavior changes.
- Do not commit real API keys, `.env` files, private documents, or generated vector stores.

## Project Priorities

- Clear RAG architecture.
- Reproducible local development.
- Reliable tests without paid API calls.
- Secure handling of secrets and uploaded documents.
