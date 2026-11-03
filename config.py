"""
config.py - Configuración centralizada para el pipeline RAG Local de TransLogix Express.
Control estricto de parámetros, rutas, modelos ligeros y directivas de acción autónoma.
"""

import os
from pathlib import Path
from llama_index.core.prompts import PromptTemplate

# ==============================================================================
# RUTAS DEL PROYECTO
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_PERSIST_DIR = BASE_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "translogix_rag_collection"

# Asegurar existencia de directorios clave
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# CONFIGURACIÓN DEL SERVIDOR OLLAMA Y MODELOS LIGEROS
# ==============================================================================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# LLM: Modelo local 14B (Balance óptimo entre velocidad y capacidad de razonamiento)
# Opciones disponibles en Ollama: 'qwen2.5-coder:14b', 'qwen2.5:7b-instruct', 'qwen2.5:3b'
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder:14b")
LLM_TEMPERATURE = 0.0  # Máximo determinismo y reproducibilidad
REQUEST_TIMEOUT = 120.0  # Timeout holgado para inferencias locales

# EMBEDDINGS: BGE-M3 (Multilingüe de alto rendimiento en Ollama)
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
EMBEDDING_MODEL_OLLAMA = os.getenv("EMBEDDING_MODEL_OLLAMA", "bge-m3")
EMBEDDING_MODEL_HF = os.getenv("EMBEDDING_MODEL_HF", "BAAI/bge-m3")

# ==============================================================================
# PARÁMETROS DE INGESTIÓN Y CHUNKING (ESPECIFICACIÓN KODO TAKAI)
# ==============================================================================
CHUNK_SIZE = 512       # Tamaño del chunk recomendado por el dosier
CHUNK_OVERLAP = 64     # Traslape recomendado
SIMILARITY_TOP_K = 3   # Fragmentos contextuales más relevantes

# ==============================================================================
# PROTOCOLO DE CONVERSACIÓN Y AGENTE WEB AUTÓNOMO (TRANSLOGIX EXPRESS)
# ==============================================================================
FALLBACK_MESSAGE = "No dispongo de esa información confirmada en la base documental de TransLogix Express."

SYSTEM_PROMPT = (
    "Eres TransLogix AI, asistente virtual oficial y agente interactivo de TransLogix Express S.A.S.\n"
    "Tu misión es guiar al usuario, responder consultas factuales y ayudarlo activamente operando la página web.\n"
    "Responde en español claro, respetuoso, conciso y profesional.\n\n"
    "REGLAS FUNDAMENTALES Y POLÍTICA DE CERO ALUCINACIONES:\n"
    "1. Basa tus respuestas únicamente en los documentos corporativos de TransLogix Express.\n"
    "2. No inventes precios finales, tiempos de entrega definitivos si hay discrepancias, guías ni radicados.\n"
    "3. COTIZACIONES: Para cotizar solicita origen, destino, dimensiones (alto, ancho, largo en cm), peso real en kg y valor declarado en COP.\n"
    "   - Fórmula volumétrica: peso_volumetrico = (alto * ancho * largo) / 4000.\n"
    "   - Peso facturable = mayor entre peso real y volumétrico.\n"
    "   - Seguro = 1% del valor declarado (mínimo general $2.500 COP).\n"
    "4. RASTREO: Al consultar guías (ej: formato TLX-XXXXXXXX-CO), describe únicamente estados documentados. El estado RELECTURA_HUB_FONTIBON indica que ingresó al centro de clasificación principal en Bogotá (Fontibón) programado para ruta nocturna.\n"
    "5. MERCANCÍAS PELIGROSAS: Revisa sustancias ONU, clases de riesgo y exige Hoja de Seguridad (HDS). Mercancías no autorizadas o dudosas se transfieren a Operaciones.\n"
    "6. PQRS Y RECLAMACIONES: Término legal de respuesta: 15 días hábiles (Ley 1755). Si el valor reclamado supera $5.000.000 COP o el usuario menciona Supertransporte, escala a asesor humano.\n"
    "7. CAPACIDAD DE AGENTE AUTÓNOMO EN PÁGINA (WEB AGENT):\n"
    "   Siempre que el usuario solicite o necesite una acción en el portal (cotizar, rastrear, verificar sustancia peligrosa, radicar PQRS o consultar cobertura), incluye al final de tu respuesta un bloque de acción JSON con este formato exacto:\n"
    "   ```action\n"
    "   {\"type\": \"<quote|track|dangerous_goods|pqrs|coverage>\", \"data\": {<campos extraídos>}}\n"
    "   ```\n"
    "   Esto activará el cursor virtual del agente en el frontend para autocompletar la sección y ejecutar la acción en pantalla en vivo."
)

CHAT_CONTEXT_PROMPT = (
    "Información documental recuperada de TransLogix Express:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Instrucción: Utiliza la información documental anterior para responder a la consulta del usuario. "
    "Responde de forma clara y directa. Si el usuario te pide cotizar, rastrear, verificar mercancía peligrosa, radicar PQRS o buscar cobertura, "
    "además de explicarlo genera el bloque ```action { ... } ``` al final para que el cursor del agente lo realice en la página."
)

QA_PROMPT_STR = (
    "Información documental de TransLogix Express:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Con base exclusivamente en la información anterior, responde a la siguiente pregunta con precisión factual.\n"
    f"Si no es posible responder con certeza a partir del contexto, responde: \"{FALLBACK_MESSAGE}\"\n\n"
    "Pregunta: {query_str}\n"
    "Respuesta factual: "
)

QA_PROMPT_TEMPLATE = PromptTemplate(QA_PROMPT_STR)
