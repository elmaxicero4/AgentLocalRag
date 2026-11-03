"""
core_setup.py - Inicialización modular de componentes: LLM, Embeddings y ChromaDB.
"""

import sys
from typing import Optional, List, Dict
import chromadb
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

import config


def get_installed_llm_models() -> List[Dict[str, any]]:
    """
    Obtiene la lista de modelos instalados en Ollama, excluyendo modelos de embeddings,
    con metadata de tamaño y categoría para el selector de modelos.
    """
    try:
        import ollama

        client = ollama.Client(host=config.OLLAMA_BASE_URL)
        installed = client.list().models
        models_list = []

        for m in installed:
            name = m.model
            # Excluir modelos de embeddings conocidos
            if "bge" in name.lower() or "embed" in name.lower():
                continue

            size_gb = round(getattr(m, "size", 0) / (1024**3), 2)

            # Clasificación de tamaño/tier
            tier = "Desconocido"
            if ":1b" in name.lower() or ":1.5b" in name.lower():
                tier = "1B / 1.5B (Ultra Rápido / Mínimo Consumo)"
            elif ":3b" in name.lower():
                tier = "3B (Ligero / Bajo Consumo)"
            elif ":7b" in name.lower() or "-7b" in name.lower() or ":8b" in name.lower():
                tier = "7B / 8B (Rápido)"
            elif ":14b" in name.lower() or "-14b" in name.lower():
                tier = "14B (Equilibrado)"
            elif ":32b" in name.lower() or "-32b" in name.lower():
                tier = "32B (Razonamiento Alto)"
            elif ":35b" in name.lower() or "-35b" in name.lower():
                tier = "35B (MoE Profundo)"
            elif ":26b" in name.lower():
                tier = "26B (Avanzado)"

            models_list.append({
                "id": name,
                "nombre": name,
                "tier": tier,
                "size_gb": size_gb,
                "is_active": False,
            })

        return models_list
    except Exception as e:
        print(f"[Core] Error al listar modelos de Ollama: {e}", file=sys.stderr)
        return []


def resolve_llm_model(model_override: Optional[str] = None) -> str:
    """Verifica si el modelo configurado o solicitado existe en Ollama; si no, aplica fallback inteligente."""
    requested = model_override or config.LLM_MODEL
    try:
        import ollama

        client = ollama.Client(host=config.OLLAMA_BASE_URL)
        installed_models = [m.model for m in client.list().models]
        if any(m == requested or m.startswith(requested + ":") for m in installed_models):
            return requested

        # Lista de modelos de respaldo instalados con alta capacidad de razonamiento
        fallbacks = [
            "qwen2.5-coder:32b",
            "qwen2.5-coder:14b",
            "llama3.2:3b",
            "qwen2.5:3b",
            "llama3.2:1b",
            "qwen2.5:1.5b",
            "qwen3:8b",
            "qwen2.5:7b-instruct",
            "qwen2.5-coder:7b",
        ]
        for fb in fallbacks:
            if any(m == fb or m.startswith(fb + ":") for m in installed_models):
                print(
                    f"\n⚠️  [AVISO OLLAMA] El modelo '{requested}' no está descargado en tu Ollama.\n"
                    f"👉 Para descargarlo ejecuta: ollama pull {requested}\n"
                    f"✅ Usando automáticamente el modelo instalado: '{fb}' para continuar sin errores.\n",
                    file=sys.stderr,
                )
                return fb
    except Exception:
        pass
    return requested


def get_llm(model_name: Optional[str] = None) -> Ollama:
    """Configura y retorna la instancia del LLM local vía Ollama."""
    active_model = resolve_llm_model(model_name)
    return Ollama(
        model=active_model,
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
