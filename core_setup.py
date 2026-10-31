"""
core_setup.py - Inicialización modular de componentes: LLM, Embeddings y ChromaDB.
"""

import sys
import chromadb
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

import config


def get_llm() -> Ollama:
    """Configura y retorna la instancia del LLM local vía Ollama."""
    return Ollama(
        model=config.LLM_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        temperature=config.LLM_TEMPERATURE,
        request_timeout=config.REQUEST_TIMEOUT,
        system_prompt=config.SYSTEM_PROMPT,
    )


def get_embedding_model():
    """
    Configura y retorna el modelo de embeddings BGE-M3.
    Soporta ejecución vía Ollama o mediante HuggingFace local según config.EMBEDDING_PROVIDER.
    """
    if config.EMBEDDING_PROVIDER == "ollama":
        from llama_index.embeddings.ollama import OllamaEmbedding

        return OllamaEmbedding(
            model_name=config.EMBEDDING_MODEL_OLLAMA,
            base_url=config.OLLAMA_BASE_URL,
            request_timeout=config.REQUEST_TIMEOUT,
        )
    elif config.EMBEDDING_PROVIDER == "huggingface":
        try:
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        except ImportError:
            raise ImportError(
                "Para usar HuggingFace, asegúrate de instalar: "
                "pip install llama-index-embeddings-huggingface sentence-transformers"
            )
        return HuggingFaceEmbedding(
            model_name=config.EMBEDDING_MODEL_HF,
        )
    else:
        raise ValueError(
            f"Proveedor de embeddings no soportado: '{config.EMBEDDING_PROVIDER}'. "
            "Usa 'ollama' o 'huggingface'."
        )


def get_chroma_vector_store() -> ChromaVectorStore:
    """Inicializa y retorna el almacenamiento vectorial persistente con ChromaDB."""
    chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_PERSIST_DIR))
    chroma_collection = chroma_client.get_or_create_collection(
        name=config.CHROMA_COLLECTION_NAME
    )
    return ChromaVectorStore(chroma_collection=chroma_collection)


def setup_global_settings():
    """Establece los componentes predeterminados en LlamaIndex Settings."""
    Settings.llm = get_llm()
    Settings.embed_model = get_embedding_model()
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
