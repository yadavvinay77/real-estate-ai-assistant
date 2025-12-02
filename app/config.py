# app/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Real Estate AI Assistant"
    DATABASE_URL: str

    # OLLAMA model instead of OpenAI
    OLLAMA_MODEL: str = "qwen2.5:1.5b"

    # RAG paths
    RAG_DOCS_PATH: str = "app/data/rag_docs"
    VECTOR_STORE_PATH: str = "app/data/vectorstore"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
