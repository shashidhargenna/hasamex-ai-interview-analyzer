import os
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


def get_embeddings() -> OpenAIEmbeddings:
    """
    Create the OpenAI embedding model.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Please add it to the .env file."
        )

    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )


def get_vectorstore() -> PineconeVectorStore:
    """
    Connect to the existing Pinecone index.
    """

    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if not pinecone_api_key:
        raise ValueError(
            "PINECONE_API_KEY is not set. "
            "Please add it to the .env file."
        )

    if not INDEX_NAME:
        raise ValueError(
            "PINECONE_INDEX_NAME is not set. "
            "Please add it to the .env file."
        )

    embeddings = get_embeddings()

    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=pinecone_api_key,
    )

    return vectorstore


def create_vectorstore(
    documents: List[Document]
) -> PineconeVectorStore:
    """
    Add transcript documents to Pinecone.

    Each document uses its segment_id as its vector ID
    so that transcript segments have deterministic IDs.
    """

    vectorstore = get_vectorstore()

    ids = [
        document.metadata["segment_id"]
        for document in documents
    ]

    vectorstore.add_documents(
        documents=documents,
        ids=ids
    )

    return vectorstore


def load_vectorstore() -> PineconeVectorStore:
    """
    Load/connect to the existing Pinecone vector store.
    """

    return get_vectorstore()