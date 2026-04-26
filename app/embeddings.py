from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL
from functools import lru_cache

@lru_cache(maxsize=1)
def get_embedding_function():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)