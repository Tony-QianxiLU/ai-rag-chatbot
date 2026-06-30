import chromadb
from chromadb.config import Settings

from ai_rag_chatbot.chunking import TextChunk
from ai_rag_chatbot.embeddings import EmbeddingProvider
from ai_rag_chatbot.retrieval import RetrievedChunk


class ChromaVectorStore:
    def __init__(
        self,
        persist_dir: str,
        embedding_provider: EmbeddingProvider,
        collection_name: str = "documents",
    ) -> None:
        self._embedding_provider = embedding_provider
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def reset(self) -> None:
        self._client.delete_collection(self._collection.name)
        self._collection = self._client.get_or_create_collection(name=self._collection.name)

    def add_chunks(self, chunks: list[TextChunk]) -> None:
        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]
        embeddings = self._embedding_provider.embed_documents(texts)
        self._collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=texts,
            metadatas=[
                {
                    "source": chunk.source,
                    "index": chunk.index,
                }
                for chunk in chunks
            ],
            embeddings=embeddings,
        )

    def retrieve(self, query: str, top_k: int = 3) -> list[RetrievedChunk]:
        query_embedding = self._embedding_provider.embed_query(query)
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        retrieved: list[RetrievedChunk] = []
        for chunk_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
            strict=True,
        ):
            chunk = TextChunk(
                id=chunk_id,
                source=str(metadata["source"]),
                index=int(metadata["index"]),
                text=document,
            )
            score = max(0, int(round((1 - float(distance)) * 100)))
            retrieved.append(RetrievedChunk(chunk=chunk, score=score))

        return retrieved

