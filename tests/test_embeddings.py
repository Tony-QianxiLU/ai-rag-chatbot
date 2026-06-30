from ai_rag_chatbot.embeddings import HashEmbeddingProvider


def test_hash_embedding_provider_returns_stable_vector() -> None:
    provider = HashEmbeddingProvider(dimensions=16)

    first = provider.embed_query("retrieval augmented generation")
    second = provider.embed_query("retrieval augmented generation")

    assert first == second
    assert len(first) == 16


def test_hash_embedding_provider_embeds_documents() -> None:
    provider = HashEmbeddingProvider(dimensions=8)

    embeddings = provider.embed_documents(["hello world", "vector search"])

    assert len(embeddings) == 2
    assert all(len(embedding) == 8 for embedding in embeddings)

