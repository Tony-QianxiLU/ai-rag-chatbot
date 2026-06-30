# Deployment

## Local

Run the app locally:

```bash
uv run streamlit run src/ai_rag_chatbot/app.py
```

## Streamlit Community Cloud

This project is suitable for Streamlit Community Cloud once a public demo is ready.

Suggested settings:

- Main file path: `src/ai_rag_chatbot/app.py`
- Python version: `3.12`
- Secrets:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL`
  - `EMBEDDING_MODEL`

## Production Considerations

- Do not commit `.env` files.
- Store API keys in the deployment platform's secret manager.
- Use persistent storage for Chroma if uploaded documents should survive restarts.
- Add evaluation checks before deployment.
- Monitor latency, cost, and failure cases.

