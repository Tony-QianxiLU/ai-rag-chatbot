"""Alternative retrieval backend built on LlamaIndex, mirroring ChromaVectorStore.

The main app uses LangChain end to end. This module shows the same chunk-in,
ranked-chunk-out retrieval contract implemented with LlamaIndex's indexing
APIs over the same Chroma database, so the two frameworks can be compared on
equal footing. See docs/llamaindex-comparison.md for the rationale.
"""

import chromadb
from chromadb.config import Settings
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.schema import Document, TextNode
from llama_index.vector_stores.chroma import ChromaVectorStore as LlamaChromaVectorStore
from pydantic import PrivateAttr

from ai_rag_chatbot.chunking import TextChunk
from ai_rag_chatbot.embeddings import EmbeddingProvider
from ai_rag_chatbot.retrieval import RetrievedChunk


class LangChainEmbeddingAdapter(BaseEmbedding):
    """Adapts this project's EmbeddingProvider protocol to LlamaIndex's BaseEmbedding.

    Lets the LlamaIndex pipeline reuse the same HashEmbeddingProvider (offline,
    deterministic, CI-friendly) or OpenAIEmbeddingProvider as the LangChain pipeline,
    instead of duplicating embedding logic per framework.
    """

    _provider: EmbeddingProvider = PrivateAttr()

    def __init__(self, provider: EmbeddingProvider, model_name: str = "ai-rag-chatbot-adapter") -> None:
        super().__init__(model_name=model_name)
        self._provider = provider

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._provider.embed_query(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._provider.embed_query(query)

    def _get_text_embedding(self, text: str) -> list[float]:
        return self._provider.embed_query(text)

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self._provider.embed_documents(texts)


class LlamaIndexVectorStore:
    """LlamaIndex-backed equivalent of ChromaVectorStore with the same interface."""

    def __init__(
        self,
        persist_dir: str,
        embedding_provider: EmbeddingProvider,
        collection_name: str = "documents_llamaindex",
    ) -> None:
        self._embed_model = LangChainEmbeddingAdapter(embedding_provider)
        self._collection_name = collection_name
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self._vector_store = self._build_vector_store()

    def _build_vector_store(self) -> LlamaChromaVectorStore:
        collection = self._client.get_or_create_collection(name=self._collection_name)
        return LlamaChromaVectorStore(chroma_collection=collection)

    def reset(self) -> None:
        self._client.delete_collection(self._collection_name)
        self._vector_store = self._build_vector_store()

    def replace_chunks(self, chunks: list[TextChunk]) -> None:
        self.reset()
        self.add_chunks(chunks)

    def add_chunks(self, chunks: list[TextChunk]) -> None:
        if not chunks:
            return

        documents = [
            Document(
                text=chunk.text,
                doc_id=chunk.id,
                metadata={"source": chunk.source, "index": chunk.index},
            )
            for chunk in chunks
        ]
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=self._embed_model,
            show_progress=False,
        )

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            embed_model=self._embed_model,
        )
        retriever = index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)

        retrieved: list[RetrievedChunk] = []
        for node_with_score in nodes:
            node = node_with_score.node
            if not isinstance(node, TextNode):
                continue

            chunk = TextChunk(
                id=node.node_id,
                source=str(node.metadata["source"]),
                index=int(node.metadata["index"]),
                text=node.get_content(),
            )
            similarity = node_with_score.score if node_with_score.score is not None else 0.0
            score = max(0, min(100, int(round(similarity * 100))))
            retrieved.append(RetrievedChunk(chunk=chunk, score=score))

        return retrieved
