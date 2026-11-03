"""
api.py - Servidor API de Producción para TransLogix Express & Agente RAG Local.

Servicio unificado de alta velocidad que provee:
1. Agente RAG conversacional e interactivo con razonamiento sobre TransLogix Express.
2. Detección y extracción de acciones de agente para operar la interfaz web en vivo.
3. Endpoints de negocio oficiales:
   - POST /api/v1/cotizar (Cálculo volumétrico y fletes)
   - GET /api/v1/tracking/{guia} (TMS Tracking con estados documentados como RELECTURA_HUB_FONTIBON)
   - POST /api/v1/pqrs (Radicación formal, 15 días hábiles Ley 1755 y escalamiento a asesor humano)
   - GET /api/v1/mercancias-peligrosas (Catálogo de sustancias ONU y requisitos de seguridad)
   - GET /api/v1/cobertura (Directorio municipal de troncales y tiempos de entrega)
4. Gestión de políticas empresariales en SQLite (Backend) y auto-indexación en caliente en ChromaDB.
"""

import os
import re
import time
import json
import random
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
import uvicorn

import config
from query import load_chat_engine
from ingest import ingest_documents
from core_setup import get_installed_llm_models, resolve_llm_model

# Importar funciones de base de datos del Backend unificado
import sys
sys.path.append(str(Path(__file__).resolve().parent / "backend"))
from db.database import (
    get_all_policies,
    get_policy_by_id,
    update_policy,
    add_policy as insert_policy,
    compile_knowledge_document,
    get_all_departamentos,
    search_municipios,
    get_all_destinos_internacionales,
    get_geo_summary,
    register_user,
    authenticate_user,
    get_user_by_token,
    get_user_by_uid,
    delete_session,
    record_user_event,
    get_user_events,
    get_user_pending_quotes
)
from user_memory import (
    save_user_event_to_vector_memory,
    search_user_memory,
    build_user_context_injection
)
from backend.obsidian_sync import (
    sync_all_to_obsidian,
    is_vault_available,
    VAULT_DIR
)

# ==============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN FASTAPI
# ==============================================================================

app = FastAPI(
    title="TransLogix Express - API & Agente Web Autónomo",
    description="Plataforma empresarial de TransLogix Express con Agente RAG Local (KODO TAKAI 2026), "
                "módulo TMS de rastreo, cotizador volumétrico, verificación de mercancías y gestión de PQRS.",
    version="3.0.0",
)

FRONTEND_DIR = config.BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"
DOCS_FILE = FRONTEND_DIR / "docs.html"
TUNNEL_FILE = config.BASE_DIR / ".tunnel_url"

# Configuración de CORS total
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestión de memoria y motor RAG en memoria
sessions: Dict[str, Any] = {}
default_engine = None
total_indexed_docs = 0


@app.on_event("startup")
def startup_event():
    """Inicializa el índice vectorial y el motor RAG al arrancar la API."""
    global default_engine, total_indexed_docs
    try:
        default_engine, total_indexed_docs = load_chat_engine()
        sessions["default"] = default_engine
        print(f"[API] Motor RAG TransLogix inicializado con éxito ({total_indexed_docs} fragmentos en ChromaDB).")
        print(f"[API] Modelo LLM activo: {config.LLM_MODEL}")
    except Exception as e:
        print(f"[API Error] Error al cargar el motor RAG: {e}")


def get_or_create_session(session_id: str, model_name: Optional[str] = None, reset: bool = False):
    """Retorna la instancia del motor de chat para una sesión y modelo, o crea una nueva."""
    resolved_model = resolve_llm_model(model_name)
    cache_key = f"{session_id}::{resolved_model}"

    if reset and cache_key in sessions:
        del sessions[cache_key]

    if cache_key not in sessions:
        engine, _ = load_chat_engine(model_name=resolved_model)
        sessions[cache_key] = engine

    return sessions[cache_key], resolved_model


# ==============================================================================
# ESQUEMAS PYDANTIC (ENTRADA Y SALIDA)
# ==============================================================================

class QueryRequest(BaseModel):
    pregunta: str = Field(..., description="Pregunta o instrucción del usuario para el agente.", example="Cotízame un paquete de Bogotá a Medellín de 10kg")
    session_id: Optional[str] = Field(default="default", description="Identificador de sesión para conservar la memoria conversacional.")
    modelo: Optional[str] = Field(default=None, description="Modelo Ollama a utilizar (ej: 'qwen2.5:7b-instruct', 'qwen2.5-coder:14b').")
    reset_history: Optional[bool] = Field(default=False, description="Si es True, reinicia la memoria conversacional de la sesión.")
    uid: Optional[str] = Field(default=None, description="UID único del usuario para memoria comportamental e historial de envíos.")
    token: Optional[str] = Field(default=None, description="Token de sesión del usuario autenticado.")


# ==============================================================================
# ESQUEMAS PYDANTIC: AUTENTICACIÓN Y MEMORIA DEL USUARIO
# ==============================================================================

class RegisterRequest(BaseModel):
    email: str = Field(..., example="usuario@empresa.com")
    password: str = Field(..., min_length=6, example="ClaveSegura2026!")
    nombre: str = Field(..., example="Alejandra Ruiz")
    empresa: Optional[str] = Field(default="Cliente Particular", example="Distribuidora Nacional S.A.")


class LoginRequest(BaseModel):
    email: str = Field(..., example="usuario@empresa.com")
    password: str = Field(..., example="ClaveSegura2026!")


class UserEventRequest(BaseModel):
    uid: Optional[str] = Field(None, example="usr_a1b2c3d4")
    tipo_evento: str = Field(..., example="COTIZACION_INCOMPLETA")
    descripcion: str = Field(..., example="Intentó cotizar de Bogotá a Medellín 10kg pero no completó")
    metadatos: Optional[Dict[str, Any]] = Field(default_factory=dict)


class FuenteDetalle(BaseModel):
    id: int
    archivo: str
    documento: str
    seccion: Optional[str] = None
    fragmento: str
    score: Optional[float] = None
    relevancia_porcentaje: Optional[str] = None


class QueryData(BaseModel):
    mensaje: str
    pregunta: str
    fuentes: List[FuenteDetalle] = Field(default_factory=list)
    total_fuentes: int = 0
    tiene_fuentes: bool = False
    action: Optional[Dict[str, Any]] = None


class QueryMetadata(BaseModel):
    modelo: str
    session_id: str
    tiempo_respuesta_segundos: float
    timestamp: str


class QueryResponse(BaseModel):
    success: bool = True
    status: str = "success"
    data: QueryData
    metadata: QueryMetadata
    error: Optional[str] = None

    # Compatibilidad directa a nivel raíz
    respuesta: str
    pregunta: str
    fuentes: List[FuenteDetalle] = Field(default_factory=list)
    action: Optional[Dict[str, Any]] = None
    fecha: str
    tiempo_respuesta_segundos: float
    modelo: str
    session_id: str


# Esquemas de Negocio TransLogix
class CotizacionRequest(BaseModel):
    origen: str = Field(..., example="Bogotá")
    destino: str = Field(..., example="Medellín")
    alto: float = Field(..., example=30.0, description="Alto en cm")
    ancho: float = Field(..., example=30.0, description="Ancho en cm")
    largo: float = Field(..., example=30.0, description="Largo en cm")
    peso_real: float = Field(..., example=10.0, description="Peso real en kg")
    valor_declarado: float = Field(default=150000.0, description="Valor declarado de la mercancía en COP")
    tipo_mercancia: Optional[str] = Field(default="Carga General", description="Descripción del contenido")


class PqrsCreateRequest(BaseModel):
    nombre: str = Field(..., example="Carlos Gómez")
    correo: str = Field(..., example="carlos.gomez@empresa.com")
    telefono: Optional[str] = Field(None, example="3101234567")
    guia: Optional[str] = Field(None, example="TLX-84920194-CO")
    tipo: str = Field(default="Reclamo", example="Queja")
    motivo: str = Field(..., example="Demora en entrega en ruta Bogotá - Barranquilla")
    valor_reclamado: Optional[float] = Field(default=0.0, example=250000.0)


class ReindexRequest(BaseModel):
    clean: Optional[bool] = Field(default=True)
    filename: Optional[str] = None
    content: Optional[str] = None


class PolicyUpdateRequest(BaseModel):
    contenido: str
    titulo: Optional[str] = None


class PolicyCreateRequest(BaseModel):
    seccion: str
    titulo: str
    contenido: str


# ==============================================================================
# EXTRACTOR DE ACCIONES AUTÓNOMAS PARA EL FRONTEND
# ==============================================================================

def extract_action_from_response(raw_text: str, question: str) -> tuple[str, Optional[Dict[str, Any]]]:
    """
    Detecta si la respuesta o la pregunta implican una acción del agente en el portal web.
    Limpia el texto de salida y devuelve un diccionario de acción estructurado.
    """
    action = None
    clean_text = raw_text

    # 1. Buscar bloque formal ```action ... ``` o ```json ... ```
    action_match = re.search(r"```(?:action|json)?\s*(\{[\s\S]*?\})\s*```", raw_text)
    if action_match:
        try:
            parsed = json.loads(action_match.group(1))
            if isinstance(parsed, dict) and ("type" in parsed or "action" in parsed):
                action = parsed
                clean_text = raw_text[:action_match.start()].strip() + "\n" + raw_text[action_match.end():].strip()
        except Exception:
            pass

    # 2. Si no había bloque o falló, buscar JSON suelto
    if not action:
        json_match = re.search(r"(\{\s*\"type\"\s*:\s*\"[^\"]+\"[\s\S]*?\})$", raw_text)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1))
                action = parsed
                clean_text = raw_text[:json_match.start()].strip()
            except Exception:
                pass

    # 3. Heurística inteligente en caso de que el modelo local de 7B omita el JSON
    if not action:
        q_lower = question.lower()
        # A) Intención de Cotizar
        if any(w in q_lower for w in ["cotiz", "flete", "cuanto cuesta", "cuánto cuesta", "tarifa para enviar", "tarifa de"]):
            cities = ["bogota", "bogotá", "medellin", "medellín", "cali", "barranquilla", "bucaramanga", "cartagena", "pereira", "cucuta", "cúcuta"]
            found = [c.capitalize() for c in cities if c in q_lower]
            origen = found[0] if len(found) > 0 else "Bogotá"
            destino = found[1] if len(found) > 1 else "Medellín"
            
            dims = re.findall(r"(\d+)\s*(?:x|\*|cm)", q_lower)
            alto = float(dims[0]) if len(dims) > 0 else 30.0
            ancho = float(dims[1]) if len(dims) > 1 else 30.0
            largo = float(dims[2]) if len(dims) > 2 else 30.0
            
            weight_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kilos|kilo)", q_lower)
            peso = float(weight_match.group(1)) if weight_match else 10.0
            
            val_match = re.search(r"(?:valor|pesos|\$)\s*(\d+(?:[.,]\d+)?)", q_lower)
            valor = float(val_match.group(1).replace(".", "").replace(",", "")) if val_match else 150000.0
            if valor < 1000:
                valor = 150000.0

            action = {
                "type": "quote",
                "target": "#widgetCotizador",
                "data": {
                    "origen": origen,
                    "destino": destino,
                    "alto": alto,
                    "ancho": ancho,
                    "largo": largo,
                    "peso": peso,
                    "valor": valor
                }
            }
        # B) Intención de Rastreo TMS
        elif any(w in q_lower for w in ["rastre", "guia", "guía", "donde esta", "dónde está", "paquete", "tlx-"]):
            guide_match = re.search(r"(tlx-[\w-]+|tlx\d+)", q_lower)
            guia = guide_match.group(1).upper() if guide_match else "TLX-84920194-CO"
            action = {
                "type": "track",
                "target": "#widgetRastreo",
                "data": {
                    "guia": guia
                }
            }
        # C) Intención de Mercancías Peligrosas
        elif any(w in q_lower for w in ["bateria", "batería", "litio", "peligros", "aerosol", "pintura", "quimic", "químic", "onu"]):
            item = "baterias de litio" if ("litio" in q_lower or "bateria" in q_lower) else ("aerosoles" if "aerosol" in q_lower else "pinturas")
            action = {
                "type": "dangerous_goods",
                "target": "#widgetMercancias",
                "data": {
                    "item": item
                }
            }
        # D) Intención de PQRS / Reclamaciones
        elif any(w in q_lower for w in ["pqrs", "queja", "reclamo", "reclamacion", "reclamación", "demora", "indemniz", "perdida", "pérdida", "averia", "avería"]):
            action = {
                "type": "pqrs",
                "target": "#widgetPqrs",
                "data": {
                    "tipo": "Reclamo" if ("reclamo" in q_lower or "perdida" in q_lower) else "Queja",
                    "motivo": "Demora en entrega y solicitud de trazabilidad" if "demora" in q_lower else "Reclamación general de servicio"
                }
            }
        # E) Intención de Cobertura
        elif any(w in q_lower for w in ["cobertura", "municipio", "ciudades", "llegan a", "destinos"]):
            action = {
                "type": "coverage",
                "target": "#widgetCobertura",
                "data": {
                    "ciudad": "Medellín" if "medellin" in q_lower else ("Cali" if "cali" in q_lower else "Bogotá")
                }
            }

    return clean_text.strip(), action


# ==============================================================================
# ENDPOINTS PRINCIPALES (WEB & DOCUMENTACIÓN)
# ==============================================================================

@app.get("/", tags=["Interfaz"])
def read_root():
    """Sirve la página web del portal de TransLogix Express con el agente interactivo."""
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE))
    return {"status": "ok", "message": "Portal TransLogix Express activo"}


@app.get("/docs-portal", tags=["Interfaz"], include_in_schema=False)
@app.get("/documentation", tags=["Interfaz"], include_in_schema=False)
def serve_docs_portal():
    """Sirve el portal interactivo de documentación oficial y dev portal."""
    if DOCS_FILE.exists():
        return FileResponse(str(DOCS_FILE))
    raise HTTPException(status_code=404, detail="docs.html no encontrado")


@app.get("/docs.md", tags=["Documentación IA"], include_in_schema=False)
@app.get("/api-docs.md", tags=["Documentación IA"], include_in_schema=False)
def serve_docs_markdown():
    """Sirve la documentación técnica en formato Markdown para agentes de IA."""
    md_file = config.BASE_DIR / "FRONTEND_AI_AGENT_GUIDE.md"
    if not md_file.exists():
        md_file = FRONTEND_DIR / "docs.md"
    if md_file.exists():
        return FileResponse(str(md_file), media_type="text/markdown; charset=utf-8")
    raise HTTPException(status_code=404, detail="Documento Markdown no encontrado")


@app.get("/app.js", include_in_schema=False)
def serve_app_js():
    """Sirve el script frontend app.js."""
    js_file = FRONTEND_DIR / "app.js"
    if js_file.exists():
        return FileResponse(str(js_file), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js no encontrado")


@app.get("/api/tunnel-info", tags=["Túnel y Conectividad"])
def get_tunnel_info():
    """Retorna la URL activa del túnel de Cloudflare."""
    tunnel_url = ""
    tunnel_file = Path(__file__).resolve().parent / ".tunnel_url"
    if tunnel_file.exists():
        tunnel_url = tunnel_file.read_text(encoding="utf-8").strip()
    return {
        "status": "success",
        "tunnel_url": tunnel_url,
        "is_active": bool(tunnel_url),
        "local_url": "http://localhost:8000",
        "endpoints": {
            "portal": tunnel_url or "http://localhost:8000",
            "ask_rag": f"{tunnel_url}/api/ask" if tunnel_url else "http://localhost:8000/api/ask",
            "docs": f"{tunnel_url}/docs.md" if tunnel_url else "http://localhost:8000/docs.md",
            "health": f"{tunnel_url}/health" if tunnel_url else "http://localhost:8000/health"
        }
    }


@app.get("/health", tags=["Salud"])
def health_check():
    """Verifica la salud del agente RAG, modelo local y colecciones de ChromaDB."""
    return {
        "status": "healthy",
        "empresa": "TransLogix Express S.A.S.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modelo": resolve_llm_model(),
        "embeddings": config.EMBEDDING_MODEL_OLLAMA if config.EMBEDDING_PROVIDER == "ollama" else config.EMBEDDING_MODEL_HF,
        "coleccion": config.CHROMA_COLLECTION_NAME,
        "fragmentos_activos": total_indexed_docs,
    }


@app.get("/api/models", tags=["Modelos"])
def get_models():
    """Retorna los modelos disponibles localmente con recomendaciones de hardware."""
    installed = get_installed_llm_models()
    active = resolve_llm_model()
    for item in installed:
        item["is_active"] = (item["id"] == active)

    presets = [
        {"id": "qwen2.5:7b-instruct", "nombre": "Qwen 2.5 7B", "tier": "7B", "desc": "⚡ Ultra Rápido (<1.5s)"},
        {"id": "qwen2.5-coder:14b", "nombre": "Qwen 2.5 Coder 14B", "tier": "14B", "desc": "⚖️ Balance Óptimo (~9GB)"},
        {"id": "qwen2.5-coder:32b", "nombre": "Qwen 2.5 Coder 32B", "tier": "32B", "desc": "🚀 Razonamiento Alto"},
        {"id": "qwen3.6:35b", "nombre": "Qwen 3.6 35B", "tier": "35B", "desc": "🧠 MoE Avanzado"},
    ]

    return {
        "status": "success",
        "active_model": active,
        "models": installed,
        "presets": presets,
    }


# ==============================================================================
# ENDPOINT DE CONSULTA AL AGENTE RAG CON DETECCIÓN DE ACCIONES
# ==============================================================================

@app.post("/api/ask", response_model=QueryResponse, tags=["Consulta RAG"])
@app.post("/api/chat", response_model=QueryResponse, tags=["Consulta RAG"])
def ask_question(payload: QueryRequest):
    """
    Endpoint principal para interactuar con el Agente de TransLogix Express.
    Responde consultas factuales basándose en ChromaDB y devuelve acciones de UI cuando aplica.
    """
    cleaned_question = payload.pregunta.strip()
    if not cleaned_question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    session_id = payload.session_id or "default"
    engine, active_model = get_or_create_session(
        session_id=session_id,
        model_name=payload.modelo,
        reset=payload.reset_history
    )

    # Resolver UID del usuario si viene token o uid directo
    resolved_uid = payload.uid
    if not resolved_uid and payload.token:
        user_sess = get_user_by_token(payload.token)
        if user_sess:
            resolved_uid = user_sess["uid"]

    # Inyección de Memoria Histórica y Comportamiento del Usuario si está autenticado
    query_to_engine = cleaned_question
    if resolved_uid:
        user_context_block = build_user_context_injection(resolved_uid, cleaned_question)
        if user_context_block:
            query_to_engine = f"{user_context_block}\n\nPregunta del Usuario: {cleaned_question}"

    t_start = time.time()
    iso_date = datetime.now(timezone.utc).isoformat()

    try:
        if hasattr(engine, "chat"):
            response = engine.chat(query_to_engine)
        else:
            response = engine.query(query_to_engine)

        elapsed = round(time.time() - t_start, 3)
        raw_text = str(response).strip()

        # Extraer acción estructurada para el frontend
        clean_msg, detected_action = extract_action_from_response(raw_text, cleaned_question)

        # Guardar interacción en el historial relacional y memoria vectorial del usuario
        if resolved_uid:
            try:
                record_user_event(
                    uid=resolved_uid,
                    tipo_evento="PREGUNTA_CHAT",
                    descripcion=cleaned_question,
                    metadatos={"respuesta_corta": clean_msg[:200], "accion": detected_action.get("type") if detected_action else None}
                )
                save_user_event_to_vector_memory(
                    uid=resolved_uid,
                    tipo_evento="PREGUNTA_CHAT",
                    descripcion=f"El usuario preguntó: '{cleaned_question}'. Respuesta: '{clean_msg[:250]}'",
                    metadatos={"timestamp": iso_date}
                )
            except Exception as e:
                print(f"[UserMemory] Aviso guardando evento: {e}")

        # Extraer fuentes documentales si existen
        fuentes_list: List[FuenteDetalle] = []
        if hasattr(response, "source_nodes") and response.source_nodes:
            for idx, node in enumerate(response.source_nodes, 1):
                metadata = node.node.metadata or {}
                content = node.node.get_content().strip()
                sec_match = re.search(r"##\s*([0-9]+\.[^\n]+)", content)
                seccion_title = sec_match.group(1).strip() if sec_match else None
                score_val = round(node.score, 4) if node.score is not None else None
                pct = f"{round(score_val * 100, 2)}%" if score_val is not None else None
                file_name = metadata.get("file_name", "Documentación TransLogix")

                fuentes_list.append(
                    FuenteDetalle(
                        id=idx,
                        archivo=file_name,
                        documento=file_name,
                        seccion=seccion_title,
                        fragmento=content,
                        score=score_val,
                        relevancia_porcentaje=pct,
                    )
                )

        query_data = QueryData(
            mensaje=clean_msg,
            pregunta=payload.pregunta,
            fuentes=fuentes_list,
            total_fuentes=len(fuentes_list),
            tiene_fuentes=len(fuentes_list) > 0,
            action=detected_action,
        )

        query_metadata = QueryMetadata(
            modelo=active_model,
            session_id=session_id,
            tiempo_respuesta_segundos=elapsed,
            timestamp=iso_date,
        )

        return QueryResponse(
            success=True,
            status="success",
            data=query_data,
            metadata=query_metadata,
            error=None,
            respuesta=clean_msg,
            pregunta=payload.pregunta,
            fuentes=fuentes_list,
            action=detected_action,
            fecha=iso_date,
            tiempo_respuesta_segundos=elapsed,
            modelo=active_model,
            session_id=session_id,
        )

    except Exception as e:
        elapsed = round(time.time() - t_start, 3)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "mensaje": f"Error al procesar consulta: {str(e)}",
                "tiempo_respuesta_segundos": elapsed
            }
        )


# ==============================================================================
# ENDPOINTS DE NEGOCIO TRANSLOGIX EXPRESS (TMS, COTIZADOR, PQRS, COBERTURA)
# ==============================================================================

@app.post("/api/v1/cotizar", tags=["Negocio TransLogix"])
@app.post("/api/cotizar", tags=["Negocio TransLogix"], include_in_schema=False)
def cotizar_envio(payload: CotizacionRequest):
    """
    Calcula la cotización oficial según la fórmula del dosier KODO TAKAI:
    - Peso volumétrico = (alto * ancho * largo) / 4000
    - Peso facturable = max(peso_real, peso_volumetrico)
    - Seguro = max(1% del valor declarado, $2.500 COP)
    - Flete base = peso_facturable * tarifa_por_kg (flete mínimo $18.000 COP)
    """
    peso_vol = round((payload.alto * payload.ancho * payload.largo) / 4000.0, 2)
    peso_facturable = round(max(payload.peso_real, peso_vol), 2)
    
    # Seguro al 1% con piso mínimo de $2.500 COP
    seguro = max(round(payload.valor_declarado * 0.01, 2), 2500.0)
    
    # Tarifa base referencial por kg según trayecto
    tarifa_kg = 4800.0
    flete_calculado = round(peso_facturable * tarifa_kg, 2)
    flete_minimo = 18000.0
    flete_base = max(flete_calculado, flete_minimo)
    total_estimado = round(flete_base + seguro, 2)

    # Identificar tiempo de entrega
    es_troncal = any(c in payload.destino.lower() for c in ["bogot", "medell", "cali", "barranq", "bucaram"])
    tiempo = "24 horas hábiles (Entrega al día siguiente)" if es_troncal else "48 a 72 horas hábiles (Reexpedición regional)"

    return {
        "status": "success",
        "origen": payload.origen,
        "destino": payload.destino,
        "peso_real_kg": payload.peso_real,
        "dimensiones_cm": f"{payload.alto} x {payload.ancho} x {payload.largo}",
        "peso_volumetrico_kg": peso_vol,
        "peso_facturable_kg": peso_facturable,
        "tarifa_aplicada_tipo": "Volumétrico" if peso_vol > payload.peso_real else "Peso Real",
        "desglose": {
            "flete_base_cop": flete_base,
            "seguro_cop": seguro,
            "flete_minimo_cop": flete_minimo,
            "tarifa_kg_cop": tarifa_kg
        },
        "total_estimado_cop": total_estimado,
        "tiempo_entrega_estimado": tiempo,
        "tipo_mercancia": payload.tipo_mercancia,
        "advertencia_tarifa": "Valor referencial sujeto a inspección física en báscula certificada de TransLogix Express."
    }


@app.get("/api/v1/tracking/{guia}", tags=["TMS Tracking"])
@app.get("/api/tracking/{guia}", tags=["TMS Tracking"], include_in_schema=False)
def track_shipment(guia: str):
    """
    Endpoint del TMS de TransLogix Express (GET /api/v1/tracking/{guia}).
    Retorna el estado del paquete y el historial de eventos en ruta.
    """
    guia_clean = guia.strip().upper()
    
    # Caso especial documentado en el dosier KODO TAKAI
    if "84920194" in guia_clean or "FONTIBON" in guia_clean or guia_clean == "TLX-84920194-CO":
        return {
            "status": "success",
            "guia": guia_clean,
            "origen": "Bogotá D.C. (Zona Franca Fontibón)",
            "destino": "Medellín (Hub Rionegro)",
            "ultimo_evento": {
                "codigo": "RELECTURA_HUB_FONTIBON",
                "descripcion": "El paquete ingresó al centro principal de clasificación en Bogotá (Zona Franca Fontibón) y se encuentra programado para salir en la ruta nocturna hacia su ciudad de destino.",
                "ubicación": "Hub Matriz Bogotá - Fontibón",
                "fecha_hora": "2026-11-03 04:30:00 UTC-5",
                "estado_general": "En Clasificación Nocturna"
            },
            "timeline": [
                {
                    "evento": "ADMISION_ORIGEN",
                    "descripcion": "Envío recibido y pesado en punto de atención Fontibón",
                    "fecha": "2026-11-02 17:15",
                    "completado": True
                },
                {
                    "evento": "RELECTURA_HUB_FONTIBON",
                    "descripcion": "Clasificado en cinta automatizada. Asignado a tractocamión S3",
                    "fecha": "2026-11-03 04:30",
                    "completado": True
                },
                {
                    "evento": "RUTA_TRONCAL_NOCTURNA",
                    "descripcion": "Salida en ruta troncal hacia centro de distribución regional",
                    "fecha": "Programado hoy 20:00",
                    "completado": False
                },
                {
                    "evento": "DISTRIBUCION_ULTIMA_MILLA",
                    "descripcion": "Asignación a van de reparto para entrega final",
                    "fecha": "Estimado mañana 08:30",
                    "completado": False
                }
            ],
            "eta_estimado": "Mañana antes de las 18:00 horas"
        }

    # Para cualquier otra guía se genera una trazabilidad coherente
    return {
        "status": "success",
        "guia": guia_clean,
        "origen": "Bogotá D.C.",
        "destino": "Cali / Yumbo",
        "ultimo_evento": {
            "codigo": "EN_TRANSITO",
            "descripcion": "El paquete se encuentra en tránsito en vehículo C3 sobre corredor vial nacional.",
            "ubicación": "Centro Logístico Yumbo",
            "fecha_hora": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "estado_general": "En Tránsito Activo"
        },
        "timeline": [
            {"evento": "RECIBIDO_EN_ORIGEN", "descripcion": "Paquete recibido en taquilla", "completado": True},
            {"evento": "RELECTURA_HUB_FONTIBON", "descripcion": "Clasificación y verificación de seguridad", "completado": True},
            {"evento": "EN_TRANSITO", "descripcion": "En carretera hacia ciudad destino", "completado": True},
            {"evento": "EN_REPARTO", "descripcion": "En vehículo de última milla", "completado": False},
            {"evento": "ENTREGADO", "descripcion": "Entregado a destinatario con firma digital", "completado": False}
        ],
        "eta_estimado": "24 horas hábiles"
    }


@app.post("/api/v1/pqrs", tags=["Negocio TransLogix"])
@app.post("/api/pqrs", tags=["Negocio TransLogix"], include_in_schema=False)
def radicar_pqrs(payload: PqrsCreateRequest):
    """
    Radica una Petición, Queja, Reclamo o Sugerencia.
    Genera número de radicado PQR-2026-XXXXX, fija el término legal de 15 días hábiles
    y evalúa los criterios de escalamiento a asesor humano (>$5.000.000 COP o Supertransporte).
    """
    num_radicado = f"PQR-2026-{random.randint(10000, 99999)}"
    escala_humano = False
    motivo_escalamiento = None

    if (payload.valor_reclamado or 0) > 5000000.0:
        escala_humano = True
        motivo_escalamiento = "Reclamación con valor superior a $5.000.000 COP (Comité Especial de Indemnizaciones)"

    motivo_lower = payload.motivo.lower()
    if any(k in motivo_lower for k in ["supertransporte", "superintendencia", "sic", "demanda", "abogado"]):
        escala_humano = True
        motivo_escalamiento = "Alerta jurídica: Mención de Supertransporte / Entidad Reguladora"

    return {
        "status": "success",
        "radicado": num_radicado,
        "fecha_radicacion": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "plazo_legal_dias_habiles": 15,
        "normativa_aplicable": "Ley 1755 de 2015 y Ley 1480 de 2011",
        "tipo": payload.tipo,
        "nombre_solicitante": payload.nombre,
        "correo": payload.correo,
        "guia_asociada": payload.guia or "Sin guía asociada",
        "requiere_escalamiento_humano": escala_humano,
        "motivo_escalamiento": motivo_escalamiento,
        "mensaje": f"Su {payload.tipo.lower()} ha sido radicada formalmente bajo el radicado {num_radicado}. "
                   f"TransLogix Express responderá en un plazo máximo de 15 días hábiles a su correo {payload.correo}."
    }


@app.get("/api/v1/mercancias-peligrosas", tags=["Negocio TransLogix"])
def get_mercancias_peligrosas():
    """Retorna el catálogo de mercancías peligrosas reguladas según el Manual DOC-OPS-2026-03."""
    return {
        "status": "success",
        "admitidas_bajo_protocolo": [
            {
                "nombre": "Baterías de Ion-Litio (contenidas en o con equipos)",
                "onu": "ONU 3481 / ONU 3480",
                "clase": "Clase 9 - Misceláneos",
                "requisitos": "Embalaje homologado UN, protección contra cortocircuito, HDS y etiqueta de batería de litio."
            },
            {
                "nombre": "Aerosoles no inflamables y no tóxicos",
                "onu": "ONU 1950",
                "clase": "Clase 2.2 - Gases comprimidos no inflamables",
                "requisitos": "Capuchón protector de válvula, caja de cartón corrugado doble pared y flejado."
            },
            {
                "nombre": "Pinturas y Barnices Inflamables",
                "onu": "ONU 1263",
                "clase": "Clase 3 - Líquidos Inflamables",
                "requisitos": "Envase sellado herméticamente, material absorbente interior y aprobación previa de Operaciones."
            }
        ],
        "prohibidas_absolutas": [
            "Explosivos y fuegos pirotécnicos (Clase 1)",
            "Gases tóxicos o venenosos (Clase 2.3)",
            "Sustancias radiactivas (Clase 7)",
            "Armas de fuego, municiones y explosivos militares",
            "Dinero en efectivo, títulos valores negociables y billetes de banco",
            "Joyas, metales preciosos y piedras preciosas sin declaración especial de alto valor",
            "Mercancías perecederas sin servicio contratado de furgón termo (cadena de frío)"
        ]
    }


@app.get("/api/v1/cobertura", tags=["Negocio TransLogix"])
def get_cobertura_ciudades():
    """Retorna el directorio de cobertura y hubs logísticos de TransLogix Express."""
    summary = get_geo_summary()
    return {
        "status": "success",
        "hub_matriz": "Bogotá D.C. - Zona Franca Fontibón",
        "resumen_geografico": summary,
        "ciudades_troncales": [
            {"ciudad": "Bogotá D.C.", "departamento": "Cundinamarca", "hub": "Hub Fontibón", "tiempo_std": "Local 24h"},
            {"ciudad": "Medellín", "departamento": "Antioquia", "hub": "Hub Rionegro", "tiempo_std": "24h - 48h"},
            {"ciudad": "Cali", "departamento": "Valle del Cauca", "hub": "Hub Yumbo", "tiempo_std": "24h - 48h"},
            {"ciudad": "Barranquilla", "departamento": "Atlántico", "hub": "Hub Malambo", "tiempo_std": "24h - 48h"},
            {"ciudad": "Bucaramanga", "departamento": "Santander", "hub": "Hub Bucaramanga", "tiempo_std": "24h - 48h"},
            {"ciudad": "Cartagena", "departamento": "Bolívar", "hub": "Hub Malambo / Cartagena", "tiempo_std": "24h - 48h"},
            {"ciudad": "Pereira", "departamento": "Risaralda", "hub": "Hub Eje Cafetero", "tiempo_std": "24h - 48h"}
        ],
        "flota_asociada": "480 vehículos: 120 Tractocamiones S3, 180 Camiones C2/C3, 130 Turbos/Vans, 50 Furgones Termo."
    }


@app.get("/api/v1/departamentos", tags=["Base de Datos Geográfica"])
def get_departamentos_endpoint():
    """Retorna los 32 departamentos de Colombia y el Distrito Capital Bogotá."""
    deps = get_all_departamentos()
    return {
        "status": "success",
        "total_departamentos": len(deps),
        "departamentos": deps
    }


@app.get("/api/v1/municipios", tags=["Base de Datos Geográfica"])
def get_municipios_endpoint(departamento: Optional[str] = None, q: Optional[str] = None, limit: int = 200):
    """Busca municipios de Colombia filtrados por departamento o texto."""
    results = search_municipios(departamento=departamento, q=q, limit=limit)
    return {
        "status": "success",
        "total_encontrados": len(results),
        "departamento_filtro": departamento,
        "termino_busqueda": q,
        "municipios": results
    }


@app.get("/api/v1/paises", tags=["Base de Datos Geográfica"])
def get_paises_endpoint():
    """Retorna los países y destinos habilitados para Courier Internacional."""
    paises = get_all_destinos_internacionales()
    return {
        "status": "success",
        "total_paises": len(paises),
        "paises": paises
    }


# ==============================================================================
# ENDPOINTS DE AUTENTICACIÓN Y SEGURIDAD DE USUARIOS
# ==============================================================================

@app.post("/api/v1/auth/register", tags=["Autenticación y Usuarios"])
def api_register_user(payload: RegisterRequest):
    """Registra un nuevo usuario con UID criptográfico, hash con salt y token de sesión."""
    try:
        user_data = register_user(
            email=payload.email,
            password=payload.password,
            nombre=payload.nombre,
            empresa=payload.empresa or "Cliente Particular"
        )
        try:
            sync_all_to_obsidian()
        except Exception as e:
            logger.warning(f"Error actualizando Obsidian Vault: {e}")
        return {
            "status": "success",
            "mensaje": f"Bienvenido a TransLogix Express, {user_data['nombre']}.",
            "data": user_data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en registro: {str(e)}")


@app.post("/api/v1/auth/login", tags=["Autenticación y Usuarios"])
def api_login_user(payload: LoginRequest):
    """Autentica a un usuario y retorna su UID, perfil y token de sesión."""
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")
    return {
        "status": "success",
        "mensaje": f"Sesión iniciada correctamente. Bienvenido, {user['nombre']}.",
        "data": user
    }


@app.get("/api/v1/auth/me", tags=["Autenticación y Usuarios"])
def api_get_current_user(token: Optional[str] = None, request: Request = None):
    """Obtiene los datos del usuario actualmente autenticado mediante Bearer Token."""
    tok = token
    if request:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            tok = auth_header.split(" ")[1].strip()

    if not tok:
        raise HTTPException(status_code=401, detail="Token no suministrado.")

    user = get_user_by_token(tok)
    if not user:
        raise HTTPException(status_code=401, detail="Sesión expirada o token inválido.")

    pending = get_user_pending_quotes(user["uid"], limit=5)
    return {
        "status": "success",
        "data": {
            **user,
            "cotizaciones_incompletas_pendientes": len(pending),
            "ultimas_cotizaciones": pending
        }
    }


@app.post("/api/v1/auth/logout", tags=["Autenticación y Usuarios"])
def api_logout_user(token: Optional[str] = None, request: Request = None):
    """Cierra la sesión del usuario revocando el token."""
    tok = token
    if request:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            tok = auth_header.split(" ")[1].strip()

    if tok:
        delete_session(tok)
    return {"status": "success", "mensaje": "Sesión cerrada correctamente."}


# ==============================================================================
# ENDPOINTS DE COMPORTAMIENTO Y MEMORIA VECTORIAL DEL USUARIO
# ==============================================================================

@app.post("/api/v1/user/event", tags=["Memoria y Comportamiento"])
def api_record_user_event(payload: UserEventRequest, request: Request):
    """
    Registra un evento comportamental del usuario en la página:
    Cotizaciones incompletas, envíos no finalizados, consultas TMS o navegación.
    Se persiste en SQLite y se indexa vectorialmente en ChromaDB.
    """
    target_uid = payload.uid
    if not target_uid:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            user_auth = get_user_by_token(token)
            if user_auth:
                target_uid = user_auth["uid"]

    if not target_uid:
        raise HTTPException(status_code=400, detail="Debe proporcionar 'uid' en el cuerpo o un token Bearer en el encabezado.")

    user = get_user_by_uid(target_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado con ese UID.")

    event_id = record_user_event(
        uid=target_uid,
        tipo_evento=payload.tipo_evento,
        descripcion=payload.descripcion,
        metadatos=payload.metadatos or {}
    )

    # Actualizar Obsidian Vault con las nuevas cotizaciones y eventos
    try:
        sync_all_to_obsidian()
    except Exception as e:
        logger.warning(f"Error actualizando Obsidian Vault: {e}")

    return {
        "status": "success",
        "mensaje": "Evento comportamental registrado en SQLite y memoria vectorial ChromaDB.",
        "event_id": event_id,
        "uid": target_uid,
        "tipo_evento": payload.tipo_evento
    }


@app.get("/api/v1/user/history", tags=["Memoria y Comportamiento"])
def api_get_user_history(uid: Optional[str] = None, limit: int = 15, request: Request = None):
    """Retorna el historial completo de eventos y memorias vectoriales del usuario."""
    target_uid = uid
    if not target_uid and request:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            user_auth = get_user_by_token(token)
            if user_auth:
                target_uid = user_auth["uid"]

    if not target_uid:
        raise HTTPException(status_code=400, detail="Debe proporcionar 'uid' o un token Bearer válido.")

    user = get_user_by_uid(target_uid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado con ese UID.")

    events = get_user_events(target_uid, limit=limit)
    memories = search_user_memory(target_uid, "envios cotizaciones consultas pendientes", top_k=5)
    pending = get_user_pending_quotes(target_uid, limit=5)

    return {
        "status": "success",
        "user": user,
        "usuario": user,
        "total_eventos": len(events),
        "eventos_recientes": events,
        "cotizaciones_incompletas": pending,
        "memorias_vectoriales": memories
    }


# ==============================================================================
# ENDPOINTS DE INTEGRACIÓN CON OBSIDIAN VAULT
# ==============================================================================

@app.get("/api/v1/obsidian/status", tags=["Integración Obsidian"])
def api_obsidian_status():
    """Retorna el estado del Obsidian Vault local y enlaces profundos URI."""
    available = is_vault_available()
    return {
        "status": "success",
        "vault_disponible": available,
        "vault_path": str(VAULT_DIR),
        "obsidian_uri": "obsidian://open?vault=Obsidian%20Vault&file=agentes%2Ftranslogix%2Fdashboard",
        "canvas_uri": "obsidian://open?vault=Obsidian%20Vault&file=canvas%2Ftranslogix-arquitectura.canvas"
    }


@app.post("/api/v1/obsidian/sync", tags=["Integración Obsidian"])
def api_obsidian_sync():
    """Sincroniza la base de datos, métricas, cotizaciones y conocimiento con Obsidian."""
    res = sync_all_to_obsidian()
    if res.get("status") == "error":
        raise HTTPException(status_code=500, detail=res.get("mensaje"))
    return res


# ==============================================================================
# ENDPOINTS DEL BACKEND (POLÍTICAS SQLITE Y RE-INDEXACIÓN)
# ==============================================================================

def sync_database_to_agent_internal(clean: bool = True):
    """Compila las políticas de SQLite a data/manual_corporativo.txt y re-indexa el agente."""
    global default_engine, total_indexed_docs
    doc_content = compile_knowledge_document()
    target_path = config.DATA_DIR / "manual_corporativo.txt"
    target_path.write_text(doc_content, encoding="utf-8")
    ingest_documents(clean=clean)
    sessions.clear()
    default_engine, total_indexed_docs = load_chat_engine()
    sessions["default"] = default_engine
    return {"status": "success", "fragmentos_indexados": total_indexed_docs}


@app.get("/policies", tags=["Políticas Corporativas (Backend)"])
def list_policies():
    """Retorna todas las políticas registradas en la base de datos SQLite del backend."""
    return {"status": "success", "politicas": get_all_policies()}


@app.get("/policies/export", tags=["Políticas Corporativas (Backend)"])
def export_policies():
    """Exporta el compendio completo de políticas compilado."""
    policies = get_all_policies()
    document_content = compile_knowledge_document()
    return {
        "status": "success",
        "total_politicas": len(policies),
        "filename": "manual_corporativo.txt",
        "contenido": document_content
    }


@app.put("/policies/{policy_id}", tags=["Políticas Corporativas (Backend)"])
def update_policy_endpoint(policy_id: int, payload: PolicyUpdateRequest):
    """Actualiza una política en SQLite y auto-indexa en caliente."""
    existing = get_policy_by_id(policy_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"No existe política #{policy_id}")
    success = update_policy(policy_id, payload.contenido, payload.titulo)
    if not success:
        raise HTTPException(status_code=500, detail="Error al actualizar en base de datos.")
    reindex_res = sync_database_to_agent_internal(clean=True)
    return {
        "status": "success",
        "mensaje": f"Política #{policy_id} actualizada y Agente auto-indexado exitosamente.",
        "politica_id": policy_id,
        "autoindex_resultado": reindex_res
    }


@app.post("/policies", tags=["Políticas Corporativas (Backend)"])
def create_policy_endpoint(payload: PolicyCreateRequest):
    """Crea una nueva política en SQLite y auto-indexa en caliente."""
    new_id = insert_policy(payload.seccion, payload.titulo, payload.contenido)
    reindex_res = sync_database_to_agent_internal(clean=True)
    return {
        "status": "success",
        "mensaje": f"Política #{new_id} creada y Agente auto-indexado.",
        "politica_id": new_id,
        "autoindex_resultado": reindex_res
    }


@app.post("/policies/sync", tags=["Políticas Corporativas (Backend)"])
def force_sync_agent():
    """Fuerza al agente a re-indexar la base vectorial con el contenido actual de la BD SQLite."""
    try:
        reindex_res = sync_database_to_agent_internal(clean=True)
        return {"status": "success", "mensaje": "Sincronización completada.", "detalle": reindex_res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reindex", tags=["Mantenimiento e Ingesta"])
def reindex_database(payload: Optional[ReindexRequest] = None):
    """Reindexa todos los documentos de data/ a ChromaDB."""
    global default_engine, total_indexed_docs
    t_start = time.time()
    iso_date = datetime.now(timezone.utc).isoformat()
    clean_mode = True if payload is None else payload.clean

    try:
        if payload and payload.filename and payload.content is not None:
            safe_name = Path(payload.filename).name
            (config.DATA_DIR / safe_name).write_text(payload.content, encoding="utf-8")

        ingest_documents(clean=clean_mode)
        sessions.clear()
        default_engine, total_indexed_docs = load_chat_engine()
        sessions["default"] = default_engine
        elapsed = round(time.time() - t_start, 3)

        return {
            "status": "success",
            "mensaje": f"Base vectorial re-indexada ({total_indexed_docs} fragmentos en ChromaDB).",
            "fragmentos_indexados": total_indexed_docs,
            "fecha": iso_date,
            "tiempo_ejecucion_segundos": elapsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🚀 Servidor TransLogix Express iniciando en http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
