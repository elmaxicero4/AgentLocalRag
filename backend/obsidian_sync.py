"""
backend/obsidian_sync.py - Sincronizador de Datos del Agente TransLogix con Obsidian Vault.
Conecta la base de conocimiento Markdown, las políticas en SQLite, los usuarios,
las cotizaciones incompletas y la memoria episódica vectorial directamente en Obsidian.
"""

import os
import json
import sqlite3
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from backend.db.database import get_connection

VAULT_DIR = Path(os.environ.get("OBSIDIAN_VAULT_PATH", "/Users/josearroyave/Documents/Obsidian Vault"))
TRANSLOGIX_VAULT_DIR = VAULT_DIR / "agentes" / "translogix"
CONOCIMIENTO_VAULT_DIR = TRANSLOGIX_VAULT_DIR / "conocimiento"
CANVAS_VAULT_DIR = VAULT_DIR / "canvas"


def is_vault_available() -> bool:
    """Verifica si el Obsidian Vault existe en el disco."""
    return VAULT_DIR.exists() and (VAULT_DIR / ".obsidian").exists()


def get_db_connection() -> sqlite3.Connection:
    return get_connection()


def sync_knowledge_docs() -> int:
    """Copia y enriquece los documentos de data/ a la carpeta conocimiento/ en Obsidian."""
    CONOCIMIENTO_VAULT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    # Leer archivos .md de data/
    for md_file in config.DATA_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        title = md_file.stem.replace("_", " ").title()

        # Enriquecer con frontmatter para Obsidian si no lo tiene
        if not content.startswith("---"):
            frontmatter = f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: knowledge-base
tags: [translogix, logistica, rfc, knowledge-base]
source: {md_file.name}
---

"""
            content = frontmatter + content

        # Reemplazar menciones a otros documentos con wikilinks de Obsidian
        # e.g., 04_cotizaciones_y_tarifas.md -> [[04_cotizaciones_y_tarifas]]
        target_file = CONOCIMIENTO_VAULT_DIR / md_file.name
        target_file.write_text(content, encoding="utf-8")
        count += 1

    return count


def generate_agent_config_md() -> str:
    """Genera agente-config.md con las especificaciones técnicas del agente."""
    tunnel_url = ""
    tunnel_file = Path(".tunnel_url")
    if tunnel_file.exists():
        tunnel_url = tunnel_file.read_text(encoding="utf-8").strip()

    return f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: agent-config
status: active
tags: [agent, rag, translogix, ai, ollama]
---

# 🚚 TransLogix Express Agent — Configuración

## Identidad del Agente
- **Nombre:** TransLogix Express Autonomous Web Agent
- **Propósito:** Agente copiloto factual y autónomo para operaciones logísticas, cotización volumétrica, rastreo TMS, verificación de mercancías peligrosas y radicación de PQRS.
- **Motor de Control:** Cursor Virtual Autónomo que opera formularios web en vivo en el DOM (60 FPS, interpolación Bézier).

## Modelo LLM & Embeddings (100% Local / Zero Cloud Leakage)
- **Modelo de Inferencia Principal:** `qwen2.5-coder:14b` (Balance / Producción)
- **Modelos Alternativos:** `qwen2.5:7b-instruct` (Ultra Rápido) | `qwen2.5-coder:32b` (Razonamiento Complejo)
- **Motor de Inferencia:** Ollama Local (`http://localhost:11434`)
- **Modelo de Embeddings:** `bge-m3` (Dense + Sparse retrieval, multilingüe)
- **Vector Database:** ChromaDB (`./chroma_db`)
  - Colección Base de Conocimiento: `translogix_rag_collection` (185 chunks indexados)
  - Colección Memoria Comportamental: `translogix_user_memory` (Episódica con UID)

## Conectividad & Endpoints
- **URL Local:** `http://localhost:8000`
- **Túnel Público Cloudflare:** [{tunnel_url or "No activo"}]({tunnel_url or "#"})
- **Portal de Documentación:** `http://localhost:8000/docs-portal`
- **Swagger / OpenAPI:** `http://localhost:8000/docs`

## Microservicios Logísticos
1. **Cotizador Oficial:** `POST /api/v1/cotizar` (Fórmula oficial divisor 4000 cm³/kg, seguro 1% mín $2.500 COP).
2. **Rastreo TMS:** `GET /api/v1/tracking/{{guia}}` (Estados TMS con timeline de escaneo en hubs).
3. **Radicación PQRS:** `POST /api/v1/pqrs` (Término legal 15 días hábiles, detector de escalamiento humano).
4. **Mercancías Peligrosas:** `GET /api/v1/mercancias-peligrosas` (Clases 1 a 9 ONU, Hoja de Seguridad HDS).
5. **Directorio Geográfico:** `GET /api/v1/municipios` & `GET /api/v1/departamentos` (32 departamentos, 173 municipios, 16 países).

## Memoria Comportamental Episódica
- **Identificador de Usuario (UID):** `usr_<hex>` inmutable.
- **Criptografía:** PBKDF2-HMAC-SHA256 con 100.000 iteraciones y sal criptográfica única.
- **Auto-tracking:** Captura de intentos de envío y cotizaciones incompletas con persistencia en SQLite y ChromaDB.

## Enlaces Rápidos en Obsidian
- [[dashboard]] — Dashboard y métricas en vivo del sistema
- [[usuarios-y-sesiones]] — Directorio de usuarios y sesiones activas
- [[cotizaciones-incompletas-y-memoria]] — Registro de cotizaciones no finalizadas y memorias
- [[directorio-geografico]] — Cobertura Colombia 32 departamentos y courier internacional
- [[../../canvas/translogix-arquitectura.canvas|Canvas de Arquitectura Visual]]
"""


def generate_dashboard_md() -> str:
    """Genera dashboard.md con estadísticas vivas de SQLite y el estado del sistema."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Consultar SQLite
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM usuario_eventos")
    total_eventos = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM usuario_eventos WHERE tipo_evento = 'COTIZACION_INCOMPLETA'")
    total_incompletas = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT departamento) FROM colombia_municipios")
    total_deptos = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM colombia_municipios")
    total_mpios = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM destinos_internacionales")
    total_paises = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM politicas")
    total_policies = c.fetchone()[0]

    # Últimos 5 eventos
    c.execute("SELECT e.tipo_evento, e.descripcion, e.timestamp, u.nombre FROM usuario_eventos e LEFT JOIN usuarios u ON e.uid = u.uid ORDER BY e.id DESC LIMIT 5")
    ultimos_eventos = c.fetchall()

    conn.close()

    tunnel_url = ""
    tunnel_file = Path(".tunnel_url")
    if tunnel_file.exists():
        tunnel_url = tunnel_file.read_text(encoding="utf-8").strip()

    eventos_table = ""
    for ev in ultimos_eventos:
        user_name = ev["nombre"] or "Anónimo"
        ts = ev["timestamp"][:19] if ev["timestamp"] else "--"
        eventos_table += f"| {ts} | `{ev['tipo_evento']}` | {user_name} | {ev['descripcion'][:65]}... |\n"

    if not eventos_table:
        eventos_table = "| -- | -- | -- | Sin eventos registrados aún |\n"

    return f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: dashboard
status: active
tags: [dashboard, metrics, translogix]
---

# 📊 TransLogix Express — Dashboard de Operaciones & IA

> [!info] Estado del Sistema
> **Última sincronización:** `{now_str}`  
> **Servidor Local:** [http://localhost:8000](http://localhost:8000)  
> **Túnel Cloudflare:** [{tunnel_url or "Inactivo"}]({tunnel_url or "#"})  
> **Estado:** 🟢 Operativo con Ollama & ChromaDB

---

## 📈 Métricas de la Base de Datos & Memoria

| Métrica | Valor | Descripción |
| :--- | :--- | :--- |
| **Usuarios Registrados** | `{total_usuarios}` | Cuentas activas con UID y hash PBKDF2 |
| **Eventos Comportamentales** | `{total_eventos}` | Actividad total registrada en SQLite |
| **Cotizaciones Incompletas** | `{total_incompletas}` | Envíos que el usuario abandonó y la IA recuerda |
| **Políticas Normativas** | `{total_policies}` | Módulos corporativos en SQLite |
| **Departamentos Colombia** | `{total_deptos}` | Cobertura en los 32 departamentos + D.C. |
| **Municipios y Cabeceras** | `{total_mpios}` | Red logística con tiempos y cadena de frío |
| **Países Courier** | `{total_paises}` | Destinos internacionales express con régimen DIAN |
| **Vector Chunks RAG** | `185` | Chunks indexados en ChromaDB con `bge-m3` |

---

## ⚡ Última Actividad de Usuarios (SQLite)

| Timestamp | Tipo Evento | Usuario | Detalle de la Acción |
| :--- | :--- | :--- | :--- |
{eventos_table}

---

## 🧭 Vistas y Secciones del Vault

- [[agente-config]] — Configuración de modelos Ollama, endpoints y arquitectura
- [[usuarios-y-sesiones]] — Directorio detallado de usuarios registrados y sesiones
- [[cotizaciones-incompletas-y-memoria]] — Envíos no completados guardados en la memoria episódica
- [[directorio-geografico]] — Red geográfica nacional (32 departamentos) e internacional
- [[../../canvas/translogix-arquitectura.canvas|Diagrama Visual Canvas]] — Diagrama de nodos y conexiones de la solución
- [[conocimiento/00_LEEME_INDICE|Base de Conocimiento Completa]] — Explorar los manuales y políticas de TransLogix
"""


def generate_usuarios_md() -> str:
    """Genera usuarios-y-sesiones.md con los usuarios y sesiones activas en SQLite."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT uid, email, nombre, empresa, fecha_registro, ultimo_login FROM usuarios ORDER BY fecha_registro DESC")
    usuarios = c.fetchall()

    c.execute("""
        SELECT s.token, s.fecha_creacion, s.fecha_expiracion, u.nombre, u.email 
        FROM usuario_sesiones s 
        JOIN usuarios u ON s.uid = u.uid 
        ORDER BY s.fecha_creacion DESC LIMIT 10
    """)
    sesiones = c.fetchall()
    conn.close()

    usuarios_rows = ""
    for u in usuarios:
        reg = u["fecha_registro"][:16] if u["fecha_registro"] else "--"
        log = u["ultimo_login"][:16] if u["ultimo_login"] else "--"
        usuarios_rows += f"| `{u['uid']}` | **{u['nombre']}** | `{u['email']}` | {u['empresa'] or 'Particular'} | {reg} | {log} |\n"

    if not usuarios_rows:
        usuarios_rows = "| -- | -- | -- | -- | -- | No hay usuarios registrados |\n"

    sesiones_rows = ""
    for s in sesiones:
        tok_preview = f"`{s['token'][:16]}...`"
        creado = s["fecha_creacion"][:16] if s["fecha_creacion"] else "--"
        expira = s["fecha_expiracion"][:16] if s["fecha_expiracion"] else "--"
        sesiones_rows += f"| {tok_preview} | {s['nombre']} (`{s['email']}`) | {creado} | {expira} |\n"

    if not sesiones_rows:
        sesiones_rows = "| -- | -- | -- | Sin sesiones activas |\n"

    return f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: users-directory
tags: [users, security, sessions, translogix]
---

# 👥 Directorio de Usuarios & Sesiones — TransLogix

## Cuentas de Usuario Registradas

> Cada usuario cuenta con un **UID inmutable**, sal criptográfica de 16 bytes y contraseña protegida con **PBKDF2-HMAC-SHA256**.

| UID | Nombre | Correo Electrónico | Empresa | Registro | Último Acceso |
| :--- | :--- | :--- | :--- | :--- | :--- |
{usuarios_rows}

---

## Sesiones Bearer Activas (Últimas 10)

| Token Bearer (Prefijo) | Usuario Asociado | Fecha Inicio | Expira |
| :--- | :--- | :--- | :--- |
{sesiones_rows}

---
- Volver al [[dashboard|Dashboard TransLogix]]
"""


def generate_cotizaciones_incompletas_md() -> str:
    """Genera cotizaciones-incompletas-y-memoria.md con los intentos no finalizados."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT e.id, e.uid, e.tipo_evento, e.descripcion, e.metadatos_json, e.timestamp, u.nombre, u.email
        FROM usuario_eventos e
        JOIN usuarios u ON e.uid = u.uid
        WHERE e.tipo_evento = 'COTIZACION_INCOMPLETA'
        ORDER BY e.id DESC
    """)
    incompletas = c.fetchall()
    conn.close()

    cards = ""
    for item in incompletas:
        meta = {}
        try:
            meta = json.loads(item["metadatos_json"] or "{}")
        except Exception:
            pass

        origen = meta.get("origen", "No especificado")
        destino = meta.get("destino", "No especificado")
        peso = meta.get("peso", 0)
        largo = meta.get("largo", 0)
        ancho = meta.get("ancho", 0)
        alto = meta.get("alto", 0)
        valor = meta.get("valor", 0)
        tipo = meta.get("tipo", "General")
        ts = item["timestamp"][:19] if item["timestamp"] else "--"

        cards += f"""### ⚠️ Intento #{item['id']} — {item['nombre']} (`{item['uid']}`)
- **Fecha:** `{ts}`
- **Ruta Cotizada:** `{origen}` ➔ `{destino}`
- **Carga:** {peso} kg — Dimensiones: {largo} x {ancho} x {alto} cm
- **Tipo de Mercancía:** {tipo}
- **Valor Declarado:** ${valor:,.0f} COP
- **Detalle Registrado:** {item['descripcion']}

```json
{json.dumps(meta, indent=2, ensure_ascii=False)}
```

---
"""

    if not cards:
        cards = "_No hay cotizaciones incompletas registradas en la base de datos._\n"

    return f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: user-memory
tags: [user-memory, quotes, episodic-memory, translogix]
---

# 📦 Cotizaciones Incompletas & Memoria Episódica

Este documento contiene los intentos de cotización capturados automáticamente por el sistema cuando un usuario autenticado digita datos en el cotizador del portal pero no presiona *Calcular Cotización*.

El Agente de IA (`qwen2.5-coder:14b`) consulta esta memoria tanto en **SQLite** como vectorialmente en **ChromaDB (`translogix_user_memory`)** para saludar al cliente por su nombre y ofrecerle continuar con su envío pendiente.

{cards}

- Volver al [[dashboard|Dashboard TransLogix]]
"""


def generate_directorio_geografico_md() -> str:
    """Genera directorio-geografico.md con los 32 departamentos y países."""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT DISTINCT departamento, region, count(*) as total_mpios FROM colombia_municipios GROUP BY departamento ORDER BY departamento ASC")
    deptos = c.fetchall()

    c.execute("SELECT codigo_iso, pais, continente, tiempo_entrega, hub_salida, regimen_aduanero FROM destinos_internacionales ORDER BY pais ASC")
    paises = c.fetchall()
    conn.close()

    deptos_rows = ""
    for d in deptos:
        deptos_rows += f"| **{d['departamento']}** | {d['region']} | {d['total_mpios']} municipios | Cobertura Troncal Oficial |\n"

    paises_rows = ""
    for p in paises:
        dept = p['regimen_aduanero'] or 'General DIAN'
        paises_rows += f"| `{p['codigo_iso']}` | **{p['pais']}** | {p['continente']} | {p['tiempo_entrega']} | {p['hub_salida']} | {dept} |\n"

    return f"""---
created: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
agent: translogix
type: geography-directory
tags: [geography, colombia, coverage, courier, translogix]
---

# 🗺️ Directorio Geográfico — Cobertura Colombia & Courier Internacional

## 🇨🇴 Los 32 Departamentos de Colombia + Bogotá D.C. (Descargados en SQLite)

| Departamento | Región Geográfica | Cabeceras Estratégicas | Tipo de Servicio |
| :--- | :--- | :--- | :--- |
{deptos_rows}

---

## ✈️ Red de Courier Internacional Express (16 Países Destino)

| Código ISO | País | Continente | Tiempo Estándar | Hub de Salida | Régimen Aduanero |
| :--- | :--- | :--- | :--- | :--- | :--- |
{paises_rows}

---
- Volver al [[dashboard|Dashboard TransLogix]]
"""


def generate_obsidian_canvas() -> str:
    """Genera translogix-arquitectura.canvas con el diagrama visual de nodos en Obsidian Canvas."""
    canvas_data = {
        "nodes": [
            {
                "id": "node_user",
                "x": -500,
                "y": -100,
                "width": 320,
                "height": 220,
                "type": "text",
                "text": "## 👤 Usuario / Cliente\n- Navega en el Portal Web\n- Inicia Sesión (UID con PBKDF2)\n- Interactúa en el Chat con IA\n- Digita datos en Cotizador, TMS o PQRS\n- Observa el **Cursor Virtual** en pantalla"
            },
            {
                "id": "node_frontend",
                "x": -100,
                "y": -150,
                "width": 340,
                "height": 300,
                "type": "text",
                "text": "## 💻 Portal Web Frontend (Shadcn + Tailwind)\n- `frontend/index.html` & `app.js`\n- Tema Blanco por Defecto + Dark Mode\n- 🖱️ **Motor de Cursor Virtual Autónomo** (60 FPS)\n- Widgets interactivos: Cotizador, TMS, PQRS\n- Debounce Tracker de cotizaciones incompletas\n- Deep link a Obsidian: `obsidian://open?...`"
            },
            {
                "id": "node_fastapi",
                "x": 340,
                "y": -150,
                "width": 340,
                "height": 300,
                "type": "text",
                "text": "## 🌐 API Unificada FastAPI (Puerto 8000)\n- `api.py` (CORS activo, Cloudflare Tunnel)\n- `POST /api/ask`: Orquestación RAG + Memory\n- Microservicios: `/cotizar`, `/tracking`, `/pqrs`\n- Autenticación: `/api/v1/auth/*`\n- Memoria Comportamental: `/api/v1/user/*`\n- Sincronizador Obsidian: `/api/v1/obsidian/*`"
            },
            {
                "id": "node_rag_agent",
                "x": 780,
                "y": -280,
                "width": 340,
                "height": 260,
                "type": "text",
                "text": "## 🧠 Agente IA & LlamaIndex\n- Modelos: `qwen2.5-coder:14b` / `7b`\n- Ollama Local (`localhost:11434`)\n- Inyección Contextual Episódica de Usuario\n- Generación de JSON `action` para el cursor\n- Zero Hallucination Factual Protocol"
            },
            {
                "id": "node_chromadb",
                "x": 1200,
                "y": -280,
                "width": 340,
                "height": 240,
                "type": "text",
                "text": "## 🧬 ChromaDB Vector Store (`bge-m3`)\n- `translogix_rag_collection`: 185 chunks de normativa, tarifas, embalaje y PQRS\n- `translogix_user_memory`: Fragmentos semánticos de comportamiento y cotizaciones por UID"
            },
            {
                "id": "node_sqlite",
                "x": 780,
                "y": 60,
                "width": 340,
                "height": 280,
                "type": "text",
                "text": "## 🗄️ Base de Datos SQLite (`database.sqlite`)\n- `usuarios`: Credenciales seguras (salt + hash)\n- `usuario_sesiones`: Tokens Bearer activos\n- `usuario_eventos`: Historial cronológico de navegación\n- `departamentos`: 32 departamentos Colombia\n- `municipios`: 173 cabeceras con tiempos y frío\n- `paises_internacional`: 16 países courier"
            },
            {
                "id": "node_obsidian",
                "x": 1200,
                "y": 60,
                "width": 340,
                "height": 280,
                "type": "text",
                "text": "## 🟣 Obsidian Vault Integration\n- Vault: `José's Agent Vault`\n- Carpeta: `agentes/translogix/`\n- `dashboard.md`: Métricas en vivo\n- `agente-config.md`: Parámetros y modelo\n- `usuarios-y-sesiones.md`: Directorio vivo\n- `cotizaciones-incompletas-y-memoria.md`\n- `conocimiento/`: Manuales y reglas en .md"
            }
        ],
        "edges": [
            { "id": "e1", "fromNode": "node_user", "fromSide": "right", "toNode": "node_frontend", "toSide": "left", "label": "Interacción visual" },
            { "id": "e2", "fromNode": "node_frontend", "fromSide": "right", "toNode": "node_fastapi", "toSide": "left", "label": "HTTP REST / Bearer" },
            { "id": "e3", "fromNode": "node_fastapi", "fromSide": "right", "toNode": "node_rag_agent", "toSide": "left", "label": "Prompt + User Context" },
            { "id": "e4", "fromNode": "node_rag_agent", "fromSide": "right", "toNode": "node_chromadb", "toSide": "left", "label": "Búsqueda vectorial bge-m3" },
            { "id": "e5", "fromNode": "node_fastapi", "fromSide": "right", "toNode": "node_sqlite", "toSide": "left", "label": "CRUD Políticas, Usuarios & Geo" },
            { "id": "e6", "fromNode": "node_fastapi", "fromSide": "bottom", "toNode": "node_obsidian", "toSide": "left", "label": "Sync Live Markdown & Metrics" },
            { "id": "e7", "fromNode": "node_frontend", "fromSide": "bottom", "toNode": "node_obsidian", "toSide": "bottom", "label": "obsidian://open link en 1 clic" }
        ]
    }
    return json.dumps(canvas_data, indent=2, ensure_ascii=False)


def update_vault_index() -> bool:
    """Actualiza el INDEX.md y sistema/arquitectura-de-agentes.md del Obsidian Vault para incluir TransLogix."""
    index_file = VAULT_DIR / "INDEX.md"
    if not index_file.exists():
        return False

    content = index_file.read_text(encoding="utf-8")
    translogix_block = """### TransLogix Agent
- [[agentes/translogix/dashboard]] — Dashboard y métricas vivas de operaciones e IA
- [[agentes/translogix/agente-config]] — Configuración del agente, modelos Ollama y microservicios
- [[agentes/translogix/usuarios-y-sesiones]] — Usuarios registrados, sesiones seguras y UIDs
- [[agentes/translogix/cotizaciones-incompletas-y-memoria]] — Cotizaciones pendientes y memoria episódica
- [[agentes/translogix/directorio-geografico]] — Cobertura Colombia 32 departamentos y courier internacional
- [[canvas/translogix-arquitectura.canvas|Canvas Visual de Arquitectura TransLogix]]
"""

    if "agentes/translogix" not in content:
        # Insertar bajo ## Agentes activos
        if "## Agentes activos" in content:
            content = content.replace("## Agentes activos\n\n", f"## Agentes activos\n\n{translogix_block}\n")
        else:
            content += f"\n\n## TransLogix Agent\n\n{translogix_block}\n"
        index_file.write_text(content, encoding="utf-8")

    # Actualizar también arquitectura-de-agentes.md
    arq_file = VAULT_DIR / "sistema" / "arquitectura-de-agentes.md"
    if arq_file.exists():
        arq_content = arq_file.read_text(encoding="utf-8")
        if "TransLogix Express" not in arq_content:
            translogix_arq_block = """### 5. TransLogix Express Agent
- **Función**: Agente Web Autónomo de operaciones logísticas, cotización volumétrica, tracking TMS y radicación PQRS.
- **Backend**: FastAPI Local (`http://localhost:8000`) + Ollama (`qwen2.5-coder:14b` & `bge-m3`).
- **Cursor Virtual**: Opera en vivo formularios web en el DOM a 60 FPS.
- **Reglas**:
  - Zero-hallucination sobre normativas y fletes.
  - Memoria episódica de usuarios y cotizaciones incompletas.
- **Estado**: ✅ Conectado — Base RAG de 185 chunks, 32 departamentos, 173 municipios.
- **Notas**: [[agentes/translogix/dashboard]] | [[agentes/translogix/agente-config]]
"""
            if "## Persistencia" in arq_content:
                arq_content = arq_content.replace("## Persistencia", f"{translogix_arq_block}\n## Persistencia")
            else:
                arq_content += f"\n\n{translogix_arq_block}\n"
            arq_file.write_text(arq_content, encoding="utf-8")

    return True


def sync_all_to_obsidian() -> Dict[str, Any]:
    """Ejecuta la sincronización completa del sistema con el Vault de Obsidian."""
    if not is_vault_available():
        return {
            "status": "error",
            "mensaje": f"El Obsidian Vault no fue encontrado en '{VAULT_DIR}'.",
            "vault_dir": str(VAULT_DIR)
        }

    TRANSLOGIX_VAULT_DIR.mkdir(parents=True, exist_ok=True)
    CANVAS_VAULT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Escribir agente-config.md
    (TRANSLOGIX_VAULT_DIR / "agente-config.md").write_text(generate_agent_config_md(), encoding="utf-8")

    # 2. Escribir dashboard.md
    (TRANSLOGIX_VAULT_DIR / "dashboard.md").write_text(generate_dashboard_md(), encoding="utf-8")

    # 3. Escribir usuarios-y-sesiones.md
    (TRANSLOGIX_VAULT_DIR / "usuarios-y-sesiones.md").write_text(generate_usuarios_md(), encoding="utf-8")

    # 4. Escribir cotizaciones-incompletas-y-memoria.md
    (TRANSLOGIX_VAULT_DIR / "cotizaciones-incompletas-y-memoria.md").write_text(generate_cotizaciones_incompletas_md(), encoding="utf-8")

    # 5. Escribir directorio-geografico.md
    (TRANSLOGIX_VAULT_DIR / "directorio-geografico.md").write_text(generate_directorio_geografico_md(), encoding="utf-8")

    # 6. Sincronizar documentos de conocimiento .md
    docs_count = sync_knowledge_docs()

    # 7. Crear/Actualizar Canvas de Arquitectura Visual
    canvas_file = CANVAS_VAULT_DIR / "translogix-arquitectura.canvas"
    canvas_file.write_text(generate_obsidian_canvas(), encoding="utf-8")

    # 8. Actualizar INDEX.md y arquitectura-de-agentes.md
    update_vault_index()

    return {
        "status": "success",
        "mensaje": "Sincronización completa con Obsidian Vault exitosa.",
        "vault_path": str(VAULT_DIR),
        "translogix_folder": str(TRANSLOGIX_VAULT_DIR),
        "documentos_conocimiento_sincronizados": docs_count,
        "canvas_generado": str(canvas_file),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    result = sync_all_to_obsidian()
    print(json.dumps(result, indent=2, ensure_ascii=False))
