# LangChain vs LlamaIndex

## Why both frameworks live in this repo

The main app (`rag.py`, `vector_store.py`, `app.py`) is built end to end on LangChain. `llamaindex_pipeline.py` implements the same chunk-in, ranked-chunk-out retrieval contract on top of LlamaIndex, over the same Chroma database. The goal is not to duplicate the app — it is to demonstrate the same retrieval problem solved with both of the two dominant GenAI orchestration frameworks, and to be explicit about why a given framework gets picked.

## What's shared vs framework-specific

`LangChainEmbeddingAdapter` (in `llamaindex_pipeline.py`) wraps this project's own `EmbeddingProvider` protocol — the same `HashEmbeddingProvider` and `OpenAIEmbeddingProvider` used by the LangChain path — inside LlamaIndex's `BaseEmbedding` interface. Embedding logic is written once; only the orchestration layer differs:

| Concern | LangChain path (`vector_store.py`) | LlamaIndex path (`llamaindex_pipeline.py`) |
| --- | --- | --- |
| Vector DB | Chroma, queried directly | Chroma, wrapped by `llama-index-vector-stores-chroma` |
| Embedding call | Direct `EmbeddingProvider` calls | Same provider, adapted to `BaseEmbedding` |
| Indexing | Manual `upsert` against the collection | `VectorStoreIndex.from_documents` |
| Retrieval | Manual `collection.query` + score mapping | `index.as_retriever().retrieve()` |
| Output | `RetrievedChunk` | `RetrievedChunk` (same dataclass) |

Both return the same type, so either backend could be swapped behind `rag.py` without touching the rest of the app.

## When to reach for which

- **LangChain** — better fit when the work is mostly chains/agents: composing prompts, tool calling, multi-step LLM orchestration (this project's `ai-agent-assistant` is LangGraph for that reason). Lower-level control over retrieval, at the cost of writing more of the plumbing yourself.
- **LlamaIndex** — purpose-built for the indexing/retrieval half of RAG: document parsing, node/chunk abstractions, and a large catalog of pre-built indices and retrievers. Less code for "index this corpus, retrieve from it," less convenient for general agent orchestration.

In production, the choice is rarely framework-exclusive. A common pattern is LlamaIndex for ingestion/indexing and LangChain (or a custom orchestrator) for the surrounding agent/chain logic — which is the shape this repo mirrors.

## Try it

```python
from ai_rag_chatbot.embeddings import HashEmbeddingProvider
from ai_rag_chatbot.llamaindex_pipeline import LlamaIndexVectorStore
from ai_rag_chatbot.demo_data import SAMPLE_DOCUMENT
from ai_rag_chatbot.chunking import chunk_text

chunks = chunk_text(SAMPLE_DOCUMENT.text, source=SAMPLE_DOCUMENT.filename)
store = LlamaIndexVectorStore(persist_dir=".llamaindex-demo", embedding_provider=HashEmbeddingProvider())
store.add_chunks(chunks)
for result in store.retrieve("What does retrieval augmented generation combine?"):
    print(result.score, result.chunk.text[:80])
```

Covered by `tests/test_llamaindex_pipeline.py`, which runs offline against `HashEmbeddingProvider` like the rest of the suite.
