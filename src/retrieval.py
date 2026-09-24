from typing import List

from langchain_core.documents import Document

from .embeddings import load_vectorstore


def retrieve_documents(
    query: str,
    k: int = 6
) -> List[Document]:

    # --------------------------------------------------
    # 1. Load Pinecone vector store
    # --------------------------------------------------

    vectorstore = load_vectorstore()

    # --------------------------------------------------
    # 2. Retrieve documents directly from Pinecone
    # --------------------------------------------------

    candidates = vectorstore.similarity_search(
        query,
        k=20
    )

    # --------------------------------------------------
    # 3. Remove interviewer segments
    # --------------------------------------------------

    expert_documents = [
        document
        for document in candidates
        if document.metadata.get("speaker") != "Interviewer"
    ]

    # --------------------------------------------------
    # 4. Return top-k expert documents
    # --------------------------------------------------

    return expert_documents[:k]