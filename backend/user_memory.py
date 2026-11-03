"""
backend/user_memory.py - Memoria Vectorial y Comportamental por Usuario en ChromaDB.
Permite al Agente RAG recordar las acciones, preguntas anteriores, cotizaciones incompletas
y el historial específico del usuario autenticado (asociado a su UID).
"""

import os
import time
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional

import chromadb
import config

USER_MEMORY_COLLECTION = "translogix_user_memory"


def get_chroma_client():
    """Retorna cliente persistente de ChromaDB."""
    return chromadb.PersistentClient(path=str(config.CHROMA_PERSIST_DIR))


def get_user_memory_collection():
    """Obtiene o crea la colección de memoria de usuario en ChromaDB."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=USER_MEMORY_COLLECTION,
        metadata={"description": "Memoria episódica y comportamental de usuarios de TransLogix Express"}
    )


def compute_ollama_embedding(text: str) -> List[float]:
    """Calcula el vector de embedding usando Ollama bge-m3 local."""
    url = f"{config.OLLAMA_BASE_URL}/api/embed"
    payload = {
        "model": config.EMBEDDING_MODEL_OLLAMA,
        "input": text
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        embeddings = res.get("embeddings") or res.get("embedding")
        if isinstance(embeddings, list) and len(embeddings) > 0 and isinstance(embeddings[0], list):
            return embeddings[0]
        return embeddings


def save_user_event_to_vector_memory(uid: str, tipo_evento: str, descripcion: str, metadatos: Optional[dict] = None):
    """
    Vectoriza y almacena un evento de usuario en ChromaDB para recuperación semántica.
    """
    if not uid:
        return

    collection = get_user_memory_collection()
    now_iso = datetime.now(timezone.utc).isoformat()
    doc_id = f"mem_{uid}_{int(time.time()*1000)}"

    # Crear texto enriquecido semánticamente para el embedding
    meta_details = json.dumps(metadatos or {}, ensure_ascii=False)
    doc_text = (
        f"Historial de usuario UID {uid}: Evento [{tipo_evento}] registrado el {now_iso}. "
        f"Detalle: {descripcion}. Metadatos: {meta_details}"
    )

    try:
        vec = compute_ollama_embedding(doc_text)
        collection.add(
            ids=[doc_id],
            documents=[doc_text],
            embeddings=[vec],
            metadatas=[{
                "uid": str(uid),
                "tipo_evento": str(tipo_evento),
                "timestamp": now_iso
            }]
        )
    except Exception as e:
        # Fallback si Ollama embed no responde: insertar sin embeddings explícitos
        collection.add(
            ids=[doc_id],
            documents=[doc_text],
            metadatas=[{
                "uid": str(uid),
                "tipo_evento": str(tipo_evento),
                "timestamp": now_iso
            }]
        )


def search_user_memory(uid: str, query_text: str, top_k: int = 3) -> List[Dict]:
    """
    Busca memorias relevantes del usuario en ChromaDB filtrando por su UID.
    """
    if not uid:
        return []

    collection = get_user_memory_collection()
    if collection.count() == 0:
        return []

    try:
        query_vec = compute_ollama_embedding(query_text)
        results = collection.query(
            query_embeddings=[query_vec],
            where={"uid": str(uid)},
            n_results=top_k
        )
    except Exception:
        results = collection.query(
            query_texts=[query_text],
            where={"uid": str(uid)},
            n_results=top_k
        )

    memories = []
    if results and results.get("documents") and len(results["documents"]) > 0:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
        for d, m in zip(docs, metas):
            memories.append({"documento": d, "metadata": m})

    return memories


def build_user_context_injection(uid: str, current_query: str) -> str:
    """
    Construye un bloque contextual con los datos, historial reciente y memorias
    vectoriales del usuario para inyectar en el prompt del LLM.
    """
    if not uid:
        return ""

    from backend.db.database import get_user_by_uid, get_user_events

    user = get_user_by_uid(uid)
    if not user:
        return ""

    recent_events = get_user_events(uid, limit=5)
    semantic_memories = search_user_memory(uid, current_query, top_k=3)

    lines = [
        "\n--- [CONTEXTO DE USUARIO AUTENTICADO Y MEMORIA HISTÓRICA] ---",
        f"• Nombre del Usuario: {user['nombre']}",
        f"• Email: {user['email']}",
        f"• Empresa / Organización: {user['empresa']}",
        f"• UID del Usuario: {user['uid']}",
    ]

    if recent_events:
        lines.append("• Historial reciente de actividad en el portal:")
        for ev in recent_events:
            ts = ev['timestamp'].split('T')[0]
            lines.append(f"  - [{ts}] {ev['tipo_evento']}: {ev['descripcion']}")

    if semantic_memories:
        lines.append("• Memorias relevantes recordadas de sesiones previas:")
        for m in semantic_memories:
            lines.append(f"  - {m['documento']}")

    lines.append(
        "Directiva de Personalización: Saluda al usuario por su nombre. "
        "Si pregunta por sus envíos pendientes, cotizaciones incompletas o consultas anteriores, "
        "responde usando con naturalidad la información de arriba y ofrécele completar la acción.\n"
        "--- FIN CONTEXTO USUARIO ---\n"
    )

    return "\n".join(lines)

