# Deployment

## Live URL

<https://ry84fwqnk4abfhufqkhrmz.streamlit.app/>

## Local

```bash
uv sync
PYTHONPATH=src uv run streamlit run src/ai_rag_chatbot/app.py
```

## Streamlit Community Cloud

Use the public GitHub repository:

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

## Production Considerations

- Store secrets only in the deployment platform's secret manager.
- Use platform storage or external object storage for persistent uploaded documents.
- Monitor retrieval latency, model latency, token spend, and exception rates.
- Add evaluation gates before deployment when adding new retrievers or prompts.
- Add authentication before deploying with private enterprise data.
