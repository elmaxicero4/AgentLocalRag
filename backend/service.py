"""
backend/service.py - Servicio de negocio del Backend.
Orquesta los cambios en la base de datos empresarial y notifica automáticamente
al Agente RAG para que se auto-indexe inmediatamente.
"""

from typing import Dict, Any, Optional
from db.database import (
    get_all_policies,
    get_policy_by_id,
    update_policy,
    insert_policy,
    compile_knowledge_document
)
from agent_client import AgentClient

# Instancia del cliente HTTP hacia el Agente RAG
agent = AgentClient(base_url="http://localhost:8000")


def sync_database_to_agent(clean: bool = True) -> Dict[str, Any]:
    """
    Compila todas las políticas actuales de la BD SQLite del backend
    y le pide al Agente que las re-indexe limpiamente.
    """
    document_content = compile_knowledge_document()
    print("[Backend Service] Notificando al Agente RAG para auto-indexar con los datos actuales de la BD...")
    reindex_result = agent.notify_reindex(
        clean=clean,
        filename="manual_corporativo.txt",
        content=document_content
    )
    return reindex_result


def update_policy_and_autoindex(
    policy_id: int,
    nuevo_contenido: str,
    nuevo_titulo: Optional[str] = None
) -> Dict[str, Any]:
    """
    Actualiza una política en la BD del backend y desencadena
    automáticamente la auto-indexación en el Agente RAG.
    """
    existing = get_policy_by_id(policy_id)
    if not existing:
        raise ValueError(f"No existe política con el ID {policy_id}")

    # 1. Actualizar en la base de datos SQLite
    success = update_policy(policy_id, nuevo_contenido, nuevo_titulo)
    if not success:
        raise RuntimeError("No se pudo actualizar la política en la base de datos.")

    print(f"[Backend Service] Política #{policy_id} ('{existing['seccion']}') actualizada en SQLite.")

    # 2. Desencadenar la auto-indexación del agente por API
    reindex_res = sync_database_to_agent(clean=True)

    return {
        "status": "success",
        "mensaje": f"Política #{policy_id} actualizada y Agente RAG auto-indexado exitosamente.",
        "politica_id": policy_id,
        "autoindex_resultado": reindex_res
    }


def add_policy_and_autoindex(
    seccion: str,
    titulo: str,
    contenido: str
) -> Dict[str, Any]:
    """
    Inserta una nueva política en la BD del backend y desencadena
    automáticamente la auto-indexación en el Agente RAG.
    """
    # 1. Insertar en la base de datos SQLite
    new_id = insert_policy(seccion, titulo, contenido)
    print(f"[Backend Service] Nueva política creada con ID #{new_id}: '{seccion}'.")

    # 2. Desencadenar la auto-indexación del agente por API
    reindex_res = sync_database_to_agent(clean=True)

    return {
        "status": "success",
        "mensaje": f"Nueva política #{new_id} registrada y Agente RAG auto-indexado exitosamente.",
        "politica_id": new_id,
        "autoindex_resultado": reindex_res
    }


def ask_agent_through_backend(pregunta: str, session_id: str = "default") -> Dict[str, Any]:
    """Permite al backend consultar directamente al Agente RAG."""
    return agent.ask(pregunta=pregunta, session_id=session_id)

