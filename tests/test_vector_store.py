from ai_rag_chatbot.chunking import TextChunk
from ai_rag_chatbot.embeddings import HashEmbeddingProvider
from ai_rag_chatbot.vector_store import ChromaVectorStore


def test_chroma_vector_store_retrieves_chunks(tmp_path) -> None:
    chunks = [
        TextChunk(id="a:0", source="a.txt", index=0, text="RAG retrieval context"),
        TextChunk(id="b:0", source="b.txt", index=0, text="unrelated cooking notes"),
    ]
    store = ChromaVectorStore(
        persist_dir=str(tmp_path / "chroma"),
        embedding_provider=HashEmbeddingProvider(dimensions=32),
    )

    store.add_chunks(chunks)
    results = store.retrieve("RAG retrieval", top_k=1)

    assert len(results) == 1
    assert results[0].chunk.source == "a.txt"


def test_chroma_vector_store_replaces_chunks(tmp_path) -> None:
    store = ChromaVectorStore(
        persist_dir=str(tmp_path / "chroma"),
        embedding_provider=HashEmbeddingProvider(dimensions=32),
    )

    store.replace_chunks(
        [TextChunk(id="a:0", source="a.txt", index=0, text="RAG retrieval context")]
    )
    store.replace_chunks(
        [TextChunk(id="b:0", source="b.txt", index=0, text="Agent planning context")]
    )

    results = store.retrieve("Agent planning", top_k=1)

    assert results[0].chunk.source == "b.txt"
