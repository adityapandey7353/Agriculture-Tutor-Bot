import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION

def get_collection():
    client = chromadb.Client()

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=embedding_function
    )

    return collection