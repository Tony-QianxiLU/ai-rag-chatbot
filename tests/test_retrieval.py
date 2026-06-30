from ai_rag_chatbot.chunking import TextChunk
from ai_rag_chatbot.retrieval import KeywordRetriever, tokenize


def test_tokenize_normalizes_words() -> None:
    assert tokenize("RAG, rag! Vector-search.") == {"rag", "vector", "search"}


def test_keyword_retriever_returns_matching_chunks_by_score() -> None:
    chunks = [
        TextChunk(id="a:0", source="a.txt", index=0, text="RAG uses retrieval"),
        TextChunk(id="b:0", source="b.txt", index=0, text="Embeddings support vector retrieval"),
    ]

    results = KeywordRetriever(chunks).retrieve("RAG retrieval")

    assert [result.chunk.id for result in results] == ["a:0", "b:0"]
    assert [result.score for result in results] == [2, 1]


def test_keyword_retriever_returns_empty_list_for_no_matches() -> None:
    chunks = [TextChunk(id="a:0", source="a.txt", index=0, text="unrelated text")]

    assert KeywordRetriever(chunks).retrieve("vector database") == []
