"""
backend/server.py - Servidor Backend de Negocio de AgentLocalRag (FastAPI).
Gestiona las políticas en SQLite e interactúa con el Agente RAG para consultas y auto-indexación.
"""

from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from db.database import get_all_policies, get_policy_by_id
from service import (
    sync_database_to_agent,
    update_policy_and_autoindex,
    add_policy_and_autoindex,
    ask_agent_through_backend
)

app = FastAPI(
    title="AgentLocalRag - Backend Central de Negocio",
    description="Servicio Backend empresarial que gestiona la base de datos de políticas y notifica al Agente RAG para auto-indexarse.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# ESQUEMAS
# ==============================================================================

class PolicyUpdateRequest(BaseModel):
    contenido: str = Field(..., description="Nuevo texto de la política.")
    titulo: Optional[str] = Field(None, description="Título opcional.")


class PolicyCreateRequest(BaseModel):
    seccion: str = Field(..., description="Código y nombre de sección (ej: '6. POLÍTICA DE TELETRABAJO').")
    titulo: str = Field(..., description="Título descriptivo de la política.")
    contenido: str = Field(..., description="Cuerpo del texto normativo.")


class ChatRequest(BaseModel):
    pregunta: str = Field(..., description="Pregunta para enviar al Agente RAG.")
    session_id: Optional[str] = Field(default="backend_session", description="ID de sesión.")


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/policies", tags=["Políticas Corporativas"])
def list_policies():
    """Retorna todas las políticas registradas en la base de datos del backend."""
    return {
        "status": "success",
        "politicas": get_all_policies()
    }


@app.get("/policies/export", tags=["Sincronización"])
def export_policies_for_agent():
    """
    Endpoint que el Agente RAG consulta cuando desea extraer e indexar
    todo el conocimiento documental directamente desde la base de datos del Backend.
    """
    from db.database import compile_knowledge_document, get_all_policies
    policies = get_all_policies()
    document_content = compile_knowledge_document()
    return {
        "status": "success",
        "total_politicas": len(policies),
        "filename": "manual_corporativo.txt",
        "contenido": document_content
    }


@app.get("/policies/{policy_id}", tags=["Políticas Corporativas"])
def get_policy(policy_id: int):
    """Obtiene una política por su identificador."""
    policy = get_policy_by_id(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Política no encontrada.")
    return {"status": "success", "politica": policy}


@app.put("/policies/{policy_id}", tags=["Políticas Corporativas"])
def update_policy_endpoint(policy_id: int, payload: PolicyUpdateRequest):
    """
    Actualiza una política en la BD y desencadena automáticamente la auto-indexación en el Agente RAG.
    """
    try:
        resultado = update_policy_and_autoindex(
            policy_id=policy_id,
            nuevo_contenido=payload.contenido,
            nuevo_titulo=payload.titulo
        )
        return resultado
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en backend: {str(e)}")


@app.post("/policies", tags=["Políticas Corporativas"])
def create_policy_endpoint(payload: PolicyCreateRequest):
    """
    Crea una nueva política en la BD y le solicita automáticamente al Agente que la indexe.
    """
    try:
        resultado = add_policy_and_autoindex(
            seccion=payload.seccion,
            titulo=payload.titulo,
            contenido=payload.contenido
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear política: {str(e)}")


@app.post("/policies/sync", tags=["Sincronización"])
def force_sync_agent():
    """Fuerza al agente a re-indexar la base vectorial con el contenido actual de la BD."""
    try:
        res = sync_database_to_agent(clean=True)
        return {
            "status": "success",
            "mensaje": "Sincronización enviada al agente.",
            "detalle_agente": res
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conectando con Agente RAG: {str(e)}")


@app.post("/chat", tags=["Consultas Agente"])
def query_agent(payload: ChatRequest):
    """Permite al backend consumir la API del Agente RAG y devolver la respuesta al cliente."""
    try:
        return ask_agent_through_backend(payload.pregunta, payload.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar al Agente: {str(e)}")


if __name__ == "__main__":
    print("🏢 Levantando Servidor Backend de Negocio en http://localhost:5001")
    print("📖 Swagger UI del Backend en http://localhost:5001/docs")
    uvicorn.run("server:app", host="0.0.0.0", port=5001, reload=True)

