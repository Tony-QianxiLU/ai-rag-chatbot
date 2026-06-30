from ai_rag_chatbot.document_loader import LoadedDocument


SAMPLE_DOCUMENT = LoadedDocument(
    filename="sample-rag-brief.txt",
    text=(
        "Retrieval augmented generation combines search with language generation. "
        "A RAG system first splits source documents into chunks, converts those chunks "
        "into embeddings, stores them in a vector database, and retrieves the most "
        "relevant chunks for a user question. The language model then writes an answer "
        "grounded in the retrieved context and returns citations so the user can inspect "
        "where the answer came from. This pattern is useful for enterprise knowledge "
        "assistants because it reduces hallucination risk and keeps answers tied to "
        "approved documents."
    ),
)

SAMPLE_QUESTION = "What does retrieval augmented generation combine?"
