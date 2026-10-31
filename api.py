"""
api.py - Servidor REST API con FastAPI para consumir el Agente RAG Local (AgentLocalRag).

Permite que cualquier frontend (React, Vue, mobile, etc.) envíe preguntas en JSON
y reciba respuestas conversacionales, fuentes documentales, fecha/hora y tiempo de inferencia.
"""

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

import config
from ingest import ingest_documents
from query import load_chat_engine, clean_query_input, should_display_sources
from core_setup import resolve_llm_model

# Inicializar FastAPI
app = FastAPI(
    title="AgentLocalRag - API Agente RAG Local",
    description="API REST para interactuar con el agente RAG local conversacional basado en Ollama, ChromaDB y LlamaIndex.",
    version="1.0.0",
)

# Montar interfaz frontend
FRONTEND_DIR = config.BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# Configuración de CORS para permitir conexiones desde cualquier frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (localhost:3000, 5173, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caché de sesiones de chat en memoria
# Permite mantener historial conversacional independiente por cada usuario / frontend
sessions: Dict[str, any] = {}
default_engine = None
total_indexed_docs = 0


@app.on_event("startup")
def startup_event():
    """Inicializa el índice vectorial y el motor RAG al arrancar la API."""
    global default_engine, total_indexed_docs
    try:
        default_engine, total_indexed_docs = load_chat_engine()
        sessions["default"] = default_engine
        print(f"[API] Motor RAG inicializado con éxito. {total_indexed_docs} fragmentos en ChromaDB.")
        print(f"[API] Modelo LLM activo: {config.LLM_MODEL}")
    except Exception as e:
        print(f"[API Error] Error al cargar el motor RAG: {e}")


def get_or_create_session(session_id: str, reset: bool = False):
    """Retorna la instancia del motor de chat para una sesión o crea una nueva."""
    if reset and session_id in sessions:
        del sessions[session_id]

    if session_id not in sessions:
        engine, _ = load_chat_engine()
        sessions[session_id] = engine

    return sessions[session_id]


# ==============================================================================
# ESQUEMAS PYDANTIC (ENTRADA Y SALIDA)
# ==============================================================================

class QueryRequest(BaseModel):
    pregunta: str = Field(
        ...,
        description="Pregunta o consulta del usuario para el agente.",
        example="¿Cuál es la duración del turno nocturno de soporte técnico?"
    )
    session_id: Optional[str] = Field(
        default="default",
        description="Identificador de sesión para conservar la memoria conversacional.",
        example="usuario_123"
    )
    reset_history: Optional[bool] = Field(
        default=False,
        description="Si es True, reinicia la memoria conversacional de la sesión."
    )


class FuenteItem(BaseModel):
    archivo: str = Field(..., description="Nombre del archivo de origen en la base documental.")
    fragmento: str = Field(..., description="Extracto de texto relevante recuperado.")
    score: Optional[float] = Field(None, description="Puntuación de similitud semántica del fragmento.")


class QueryResponse(BaseModel):
    status: str = Field(default="success", description="Estado de la respuesta ('success' o 'error').")
    pregunta: str = Field(..., description="Pregunta enviada por el usuario.")
    respuesta: str = Field(..., description="Respuesta generada en lenguaje natural por el agente.")
    fuentes: List[FuenteItem] = Field(default_factory=list, description="Documentos y fragmentos de donde se obtuvo la información.")
    fecha: str = Field(..., description="Fecha y hora de la consulta en formato ISO 8601 (UTC).")
    tiempo_respuesta_segundos: float = Field(..., description="Tiempo total de inferencia y respuesta del modelo en segundos.")
    modelo: str = Field(..., description="Modelo LLM utilizado para la inferencia.")
    session_id: str = Field(..., description="ID de sesión utilizado.")


class ReindexRequest(BaseModel):
    clean: Optional[bool] = Field(
        default=True,
        description="Si es True, elimina la colección previa en ChromaDB para una reindexación limpia."
    )
    from_backend: Optional[bool] = Field(
        default=False,
        description="Si es True, el Agente consulta la API del Backend (http://localhost:5001/policies/export) para traer la última versión de la BD."
    )
    backend_url: Optional[str] = Field(
        default="http://localhost:5001",
        description="URL base del Backend corporativo."
    )
    filename: Optional[str] = Field(
        default=None,
        description="Nombre opcional del archivo a crear o actualizar dentro de data/ (ej: 'manual_corporativo.txt').",
        example="manual_corporativo.txt"
    )
    content: Optional[str] = Field(
        default=None,
        description="Contenido de texto opcional para actualizar o crear el archivo antes de indexar.",
        example="# MANUAL ACTUALIZADO...\n1.1 ..."
    )


class ReindexResponse(BaseModel):
    status: str = Field(default="success", description="Estado de la re-indexación.")
    mensaje: str = Field(..., description="Mensaje explicativo del resultado.")
    fragmentos_indexados: int = Field(..., description="Cantidad total de fragmentos (embeddings) guardados en ChromaDB.")
    archivos_procesados: List[str] = Field(default_factory=list, description="Lista de archivos procesados desde data/.")
    fecha: str = Field(..., description="Fecha y hora de finalización en formato ISO 8601.")
    tiempo_ejecucion_segundos: float = Field(..., description="Tiempo total que tomó la indexación en segundos.")


# ==============================================================================
# ENDPOINTS DE LA API
# ==============================================================================

@app.get("/", tags=["Interfaz y Documentación"])
def read_root():
    """Ruta raíz que sirve directamente la interfaz de usuario web o metadatos."""
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return {
        "mensaje": "AgentLocalRag - API Agente RAG Local Operativa",
        "docs_url": "/docs",
        "modelo_activo": config.LLM_MODEL,
        "documentos_indexados": total_indexed_docs,
    }


@app.get("/app.js", include_in_schema=False)
def serve_app_js():
    """Sirve el script app.js del frontend."""
    js_file = FRONTEND_DIR / "app.js"
    if js_file.exists():
        return FileResponse(str(js_file), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js no encontrado")


@app.get("/health", tags=["Salud"])
def health_check():
    """Endpoint para verificar el estado de salud del servicio."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modelo": resolve_llm_model(),
        "embeddings": config.EMBEDDING_MODEL_OLLAMA if config.EMBEDDING_PROVIDER == "ollama" else config.EMBEDDING_MODEL_HF,
        "coleccion": config.CHROMA_COLLECTION_NAME,
        "fragmentos_activos": total_indexed_docs,
    }


@app.post("/api/ask", response_model=QueryResponse, tags=["Consulta RAG"])
@app.post("/api/chat", response_model=QueryResponse, tags=["Consulta RAG"])
def ask_question(payload: QueryRequest):
    """
    Endpoint principal para consultar al agente RAG.

    Recibe la pregunta en formato JSON, consulta la base documental,
    evalúa el contexto con el modelo local y retorna la respuesta natural,
    fuentes de origen, fecha/hora y tiempo de respuesta.
    """
    cleaned_question = clean_query_input(payload.pregunta)
    if not cleaned_question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    session_id = payload.session_id or "default"
    engine = get_or_create_session(session_id, reset=payload.reset_history)

    t_start = time.time()
    iso_date = datetime.now(timezone.utc).isoformat()

    try:
        if hasattr(engine, "chat"):
            response = engine.chat(cleaned_question)
        else:
            response = engine.query(cleaned_question)

        elapsed = round(time.time() - t_start, 3)
        answer_text = str(response).strip()

        # Extraer fuentes documentales si la respuesta es factual/documental
        fuentes_list = []
        if hasattr(response, "source_nodes") and should_display_sources(answer_text, cleaned_question):
            for node in response.source_nodes:
                metadata = node.node.metadata or {}
                fuentes_list.append(
                    FuenteItem(
                        archivo=metadata.get("file_name", "Desconocido"),
                        fragmento=node.node.get_content().strip(),
                        score=round(node.score, 4) if node.score is not None else None,
                    )
                )

        return QueryResponse(
            status="success",
            pregunta=payload.pregunta,
            respuesta=answer_text,
            fuentes=fuentes_list,
            fecha=iso_date,
            tiempo_respuesta_segundos=elapsed,
            modelo=resolve_llm_model(),
            session_id=session_id,
        )

    except Exception as e:
        elapsed = round(time.time() - t_start, 3)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "mensaje": f"Error al procesar la consulta: {str(e)}",
                "fecha": iso_date,
                "tiempo_respuesta_segundos": elapsed,
            }
        )


@app.post("/api/reindex", response_model=ReindexResponse, tags=["Mantenimiento e Ingesta"])
def reindex_database(payload: Optional[ReindexRequest] = None):
    """
    Endpoint para que un backend o administrador solicite al agente re-indexar la base vectorial.

    Permite:
    1. Reindexar los archivos existentes en ./data/.
    2. Opcionalmente recibir un archivo nuevo o actualizado (filename + content)
       para escribirlo en ./data/ antes de reindexar.
    3. Aplica re-indexación limpia (clean=True) para que los datos obsoletos se eliminen.
    4. Recarga automáticamente los motores en memoria para que las nuevas consultas
       utilicen inmediatamente la información actualizada.
    """
    global default_engine, total_indexed_docs
    t_start = time.time()
    iso_date = datetime.now(timezone.utc).isoformat()
    clean_mode = True if payload is None else payload.clean

    try:
        # 1. Si se solicitó extraer los datos directamente desde el Backend
        if payload and payload.from_backend:
            import httpx
            backend_url = (payload.backend_url or "http://localhost:5000").rstrip("/")
            export_url = f"{backend_url}/policies/export"
            print(f"[API Ingest] Agente consultando API del Backend en {export_url}...")
            with httpx.Client(timeout=15.0) as http_client:
                b_resp = http_client.get(export_url)
                b_resp.raise_for_status()
                b_data = b_resp.json()
                b_filename = b_data.get("filename", "manual_corporativo.txt")
                b_content = b_data.get("contenido", "")
                target_path = config.DATA_DIR / b_filename
                target_path.write_text(b_content, encoding="utf-8")
                print(f"[API Ingest] Datos obtenidos del Backend y guardados en {target_path}")

        # 2. Si se envió un archivo o contenido directo en el payload
        elif payload and payload.filename and payload.content is not None:
            safe_name = Path(payload.filename).name
            target_path = config.DATA_DIR / safe_name
            target_path.write_text(payload.content, encoding="utf-8")
            print(f"[API Ingest] Archivo '{safe_name}' escrito exitosamente en {target_path}")

        # 3. Ejecutar el pipeline de ingestión limpia
        ingest_documents(clean=clean_mode)

        # Recargar motores en memoria con el nuevo índice de ChromaDB
        sessions.clear()
        default_engine, total_indexed_docs = load_chat_engine()
        sessions["default"] = default_engine

        elapsed = round(time.time() - t_start, 3)
        data_files = [f.name for f in config.DATA_DIR.glob("**/*") if f.is_file() and not f.name.startswith(".")]

        return ReindexResponse(
            status="success",
            mensaje=f"Base vectorial re-indexada con éxito ({total_indexed_docs} fragmentos activos en ChromaDB).",
            fragmentos_indexados=total_indexed_docs,
            archivos_procesados=data_files,
            fecha=iso_date,
            tiempo_ejecucion_segundos=elapsed,
        )

    except Exception as e:
        elapsed = round(time.time() - t_start, 3)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "mensaje": f"Error durante la re-indexación: {str(e)}",
                "fecha": iso_date,
                "tiempo_ejecucion_segundos": elapsed,
            }
        )


@app.get("/api/documents", tags=["Mantenimiento e Ingesta"])
def list_documents():
    """Lista los archivos documentales almacenados actualmente en data/."""
    files_info = []
    for f in config.DATA_DIR.glob("**/*"):
        if f.is_file() and not f.name.startswith("."):
            files_info.append({
                "archivo": f.name,
                "tamano_bytes": f.stat().st_size,
                "ultima_modificacion": datetime.fromtimestamp(f.stat().st_mtime, timezone.utc).isoformat()
            })
    return {
        "status": "success",
        "total_archivos": len(files_info),
        "archivos": files_info,
        "directorio": str(config.DATA_DIR.resolve())
    }


if __name__ == "__main__":
    print(f"🚀 Iniciando servidor API AgentLocalRag en http://localhost:8000")
    print(f"📖 Documentación interactiva Swagger en http://localhost:8000/docs")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

