"""
config.py - Configuración centralizada para el pipeline RAG Local.
Control estricto de parámetros, rutas, modelos y directivas anti-alucinación.
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
CHROMA_COLLECTION_NAME = "local_rag_collection"

# Asegurar existencia de directorios clave
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# CONFIGURACIÓN DEL SERVIDOR OLLAMA Y MODELOS
# ==============================================================================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# LLM: Modelo local vía Ollama. Qwen 3.6 de 35B (MoE) para máxima capacidad de razonamiento
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3.6:35b")
LLM_TEMPERATURE = 0.0  # Determinismo absoluto para mitigar alucinaciones
REQUEST_TIMEOUT = 180.0  # Segundos de espera para inferencias locales

# EMBEDDINGS: BGE-M3 (Multilingüe, estado del arte)
# Opciones disponibles: 'ollama' (vía ollama pull bge-m3) o 'huggingface' (BAAI/bge-m3 local)
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
EMBEDDING_MODEL_OLLAMA = os.getenv("EMBEDDING_MODEL_OLLAMA", "bge-m3")
EMBEDDING_MODEL_HF = os.getenv("EMBEDDING_MODEL_HF", "BAAI/bge-m3")

# ==============================================================================
# PARÁMETROS DE INGESTIÓN Y CHUNKING
# ==============================================================================
CHUNK_SIZE = 512       # Tamaño del chunk en tokens/unidades semánticas
CHUNK_OVERLAP = 64     # Traslape para preservar coherencia contextual
SIMILARITY_TOP_K = 3   # Cantidad de fragmentos más relevantes a recuperar

# ==============================================================================
# PROTOCOLO CONVERSACIONAL Y ANTI-ALUCINACIONES (STRICT SCOPE & FACTUALITY)
# ==============================================================================
FALLBACK_MESSAGE = "No dispongo de esa información en la base de datos."

SYSTEM_PROMPT = (
    "Eres el asistente virtual documental de AgentLocalRag.\n"
    "Tu trato es conversacional, amable y profesional.\n\n"
    "REGLAS FUNDAMENTALES Y LÍMITES DE ALCANCE:\n"
    "1. INTERACCIÓN Y CORTESÍA: Saluda de forma natural, responde con amabilidad a la cortesía básica "
    "del usuario y explica claramente tu rol como asistente de consulta de las políticas y procedimientos "
    "internos de AgentLocalRag.\n"
    "2. CONSULTAS DOCUMENTALES: Cuando el usuario consulte sobre la organización o sus normativas, responde con "
    "precisión basándote de manera estricta y exclusiva en la información proporcionada en el contexto documental.\n"
    "3. FRENO ESTRICTO A TEMAS AJENOS (GUARDRAIL): Si el usuario intenta hablar de temas externos o ajenos a "
    "la organización (por ejemplo: cocina, deportes, entretenimiento, noticias, política, humor o cualquier asunto "
    "que no figure en los documentos de la organización), DEBES DETENER AL USUARIO cortésmente, indicándole con "
    "claridad que no dispones de información sobre ese tema y recordándole que tu función se limita únicamente a "
    "resolver consultas sobre las políticas y manuales internos de AgentLocalRag.\n"
    "4. CERO ALUCINACIONES: Jamás inventes políticas, cifras, contactos o reglas que no estén respaldadas por la "
    "documentación corporativa provista."
)

CHAT_CONTEXT_PROMPT = (
    "A continuación se presentan los fragmentos relevantes recuperados de los documentos internos:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Instrucción: Utiliza el contexto documental anterior para responder a la interacción del usuario. "
    "Sé conversacional, amable y claro, pero mantén un apego estricto a las reglas de alcance. Si el usuario pregunta "
    "o habla de cualquier tema ajeno a la empresa o no documentado, frénalo amablemente indicándole que no tienes "
    "información de eso."
)

# Template de pregunta-respuesta específico para LlamaIndex
QA_PROMPT_STR = (
    "A continuación se presenta información de contexto recuperada de la base de datos documental:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Con base exclusivamente en la información anterior, responde a la siguiente pregunta de forma directa y precisa.\n"
    f"Si la respuesta no se puede responder a partir del contexto provisto, responde exactamente: \"{FALLBACK_MESSAGE}\"\n\n"
    "Pregunta: {query_str}\n"
    "Respuesta factual: "
)

QA_PROMPT_TEMPLATE = PromptTemplate(QA_PROMPT_STR)
