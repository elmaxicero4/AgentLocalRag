"""
ingest.py - Pipeline de ingestión de documentos locales a ChromaDB con LlamaIndex.

Carga los archivos contenidos en ./data/, aplica chunking semántico mediante
SentenceSplitter, genera embeddings con bge-m3 y los almacena en ChromaDB.
"""

import sys
import argparse
import logging
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
import chromadb

import config
from core_setup import get_chroma_vector_store, setup_global_settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ingest")


def reset_collection():
    """Elimina la colección existente en ChromaDB para una indexación limpia."""
    logger.info("Reinicializando colección ChromaDB...")
    client = chromadb.PersistentClient(path=str(config.CHROMA_PERSIST_DIR))
    try:
        client.delete_collection(name=config.CHROMA_COLLECTION_NAME)
        logger.info(f"Colección '{config.CHROMA_COLLECTION_NAME}' eliminada exitosamente.")
    except Exception as e:
        logger.info(f"Colección '{config.CHROMA_COLLECTION_NAME}' no existía previamente ({e}).")


def ingest_documents(clean: bool = False):
    """
    Lee documentos desde ./data/, genera chunks y embeddings, y los persiste en ChromaDB.
    """
    logger.info(f"Iniciando proceso de ingestión...")
    logger.info(f"Directorio de datos: {config.DATA_DIR.resolve()}")
    logger.info(f"Directorio ChromaDB: {config.CHROMA_PERSIST_DIR.resolve()}")

    if clean:
        reset_collection()

    # 1. Configurar LLM y Embeddings globales
    logger.info("Configurando modelos de LLM y Embeddings...")
    setup_global_settings()

    # 2. Verificar que existan archivos en ./data/
    data_files = [f for f in config.DATA_DIR.glob("**/*") if f.is_file() and not f.name.startswith(".")]
    if not data_files:
        logger.warning(
            f"No se encontraron documentos en '{config.DATA_DIR}'. "
            "Por favor, añade archivos (.txt, .pdf, .md, etc.) antes de indexar."
        )
        return

    logger.info(f"Se encontraron {len(data_files)} archivos para procesar:")
    for f in data_files:
        logger.info(f"  - {f.name} ({f.stat().st_size} bytes)")

    # 3. Cargar documentos usando SimpleDirectoryReader
    reader = SimpleDirectoryReader(
        input_dir=str(config.DATA_DIR),
        recursive=True,
        filename_as_id=True,
    )
    documents = reader.load_data()
    logger.info(f"Documentos cargados en memoria: {len(documents)}")

    # 4. Configurar almacenamiento en ChromaDB
    vector_store = get_chroma_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Generar embeddings y persistir
    logger.info(
        f"Generando embeddings ({config.EMBEDDING_PROVIDER}:{config.EMBEDDING_MODEL_OLLAMA if config.EMBEDDING_PROVIDER == 'ollama' else config.EMBEDDING_MODEL_HF}) "
        f"con chunk_size={config.CHUNK_SIZE} y chunk_overlap={config.CHUNK_OVERLAP}..."
    )

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    # Verificar cantidad de registros indexados en Chroma
    client = chromadb.PersistentClient(path=str(config.CHROMA_PERSIST_DIR))
    collection = client.get_collection(config.CHROMA_COLLECTION_NAME)
    total_embeddings = collection.count()

    logger.info(f"============================================================")
    logger.info(f"¡Ingestión completada con éxito!")
    logger.info(f"Total de fragmentos (embeddings) en ChromaDB: {total_embeddings}")
    logger.info(f"Directorio persistido en: {config.CHROMA_PERSIST_DIR.resolve()}")
    logger.info(f"============================================================")


def main():
    parser = argparse.ArgumentParser(description="Ingesta y vectorización de documentos para RAG Local.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Borra la colección existente antes de indexar los documentos.",
    )
    args = parser.parse_args()

    try:
        ingest_documents(clean=args.clean)
    except Exception as e:
        logger.error(f"Error crítico durante la ingestión: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
