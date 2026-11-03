"""
backend/db/database.py - Base de datos corporativa de TransLogix Express (SQLite).
Almacena y gestiona las políticas, normativas, rutas y registros de TransLogix Express S.A.S.
"""

import sqlite3
import hashlib
import secrets
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional, Tuple

DB_DIR = Path(__file__).resolve().parent
DB_FILE = DB_DIR / "agent_local_rag.db"


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a la base de datos SQLite con formato de fila diccionario."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


TRANSLOGIX_SEED_DATA = [
    (
        "1. IDENTIFICACIÓN Y CANALES CORPORATIVOS",
        "Información Corporativa de TransLogix Express",
        "1.1. Razón social: TransLogix Colombia S.A.S. Nombre comercial: TransLogix Express. NIT: 901.684.329-8. Matrícula mercantil: 00385921 de la Cámara de Comercio de Bogotá.\n"
        "1.2. Sede Principal y Hub Matriz: Calle 26 # 96J-15, Zona Franca Fontibón, Bogotá D.C.\n"
        "1.3. Hubs Logísticos Nacionales: Bogotá (Zona Franca Fontibón), Rionegro (asociado a Medellín), Yumbo (asociado a Cali) y Malambo (asociado a Barranquilla).\n"
        "1.4. Flota activa (480 unidades): 120 tractocamiones S3 (carga masiva), 180 camiones C2/C3 (troncales intermunicipales), 130 turbos/vans (distribución de última milla) y 50 furgones termo (cadena de frío).\n"
        "1.5. Canales de atención: WhatsApp Business API (60% de interacciones), Web Chat (25%) y PBX telefónico (15%). Más de 45.000 despachos mensuales con OTIF del 92,4%."
    ),
    (
        "2. PORTAFOLIO DE SERVICIOS LOGÍSTICOS",
        "Servicios de Envíos y Soluciones Corporativas",
        "2.1. Express Nacional: Servicio prioritario de paquetería y mensajería especializada puerta a puerta con entrega en 24 a 48 horas en las principales ciudades del país.\n"
        "2.2. Carga Masiva: Transporte de cupo completo en vehículos pesados (S3, C2, C3) para volúmenes industriales y líneas de producción interdepartamentales.\n"
        "2.3. Courier Internacional: Envíos de exportación e importación rápida con trámite y liberación aduanera DIAN en aeropuertos El Dorado y Rionegro.\n"
        "2.4. Almacenamiento & Fulfillment: Almacén central en Zona Franca Fontibón con sistema WMS, recepción, picking, packing y control de inventarios.\n"
        "2.5. Logística Inversa: Gestión de devoluciones comerciales, recolección de garantías y retorno de mercancías con trazabilidad completa."
    ),
    (
        "3. REGLAS OFICIALES DE COTIZACIÓN Y FLETES",
        "Cálculo Volumétrico y Tarifas de Envíos",
        "3.1. Datos obligatorios para cotizar: Ciudad de origen, Ciudad de destino, Dimensiones en cm (alto, ancho, largo), Peso real en kg y Valor declarado en COP.\n"
        "3.2. Fórmula oficial de peso volumétrico: peso_volumetrico_kg = (alto_cm * ancho_cm * largo_cm) / 4000.\n"
        "3.3. Peso facturable: Se calcula como el mayor valor entre el peso real y el peso volumétrico (max(peso_real, peso_volumetrico)).\n"
        "3.4. Seguro del envío: Se liquida al 1% del valor declarado, con una tarifa mínima de seguro de $2.500 COP.\n"
        "3.5. Flete total referencial: Corresponde al flete base liquidado por el peso facturable más el valor del seguro obligatorio. Si la ruta registra flete mínimo en la matriz, se aplicará el valor que resulte mayor."
    ),
    (
        "4. COBERTURA REGIONAL Y TIEMPOS DE ENTREGA",
        "Directorio de Municipios y Tiempos de Tránsito",
        "4.1. Ciudades Troncales Principales: Bogotá D.C., Medellín / Rionegro, Cali / Yumbo, Barranquilla / Malambo, Bucaramanga, Cartagena, Pereira, Manizales y Cúcuta.\n"
        "4.2. Tiempos de entrega estándar: 24 horas hábiles entre ciudades troncales principales conectadas de forma directa.\n"
        "4.3. Rutas con reexpedición regional o destinos secundarios: Tiempo de tránsito estimado de 48 a 72 horas hábiles.\n"
        "4.4. Envíos hacia zonas especiales o insulares (San Andrés): Tiempo de entrega de 5 a 8 días hábiles sujeto a itinerarios aéreos y marítimos."
    ),
    (
        "5. MERCANCÍAS PELIGROSAS Y RESTRICCIONES",
        "Sustancias ONU y Protocolos de Seguridad DOC-OPS-2026-03",
        "5.1. Mercancías peligrosas admitidas bajo protocolo estricto: Baterías de ion-litio embaladas con o contenidas en equipos (ONU 3481 / ONU 3480), aerosoles clase 2 (ONU 1950) y pinturas o barnices líquidos inflamables clase 3 (ONU 1263).\n"
        "5.2. Requisitos obligatorios para admitir mercancías peligrosas: Hoja de Datos de Seguridad (HDS/MSDS) en 16 secciones no mayor a 3 años, embalaje homologado UN y rotulado reglamentario.\n"
        "5.3. Mercancías terminantemente prohibidas: Explosivos clase 1, gases tóxicos clase 2.3, sustancias radiactivas clase 7, armas de fuego, dinero en efectivo, títulos valores, joyas y animales vivos.\n"
        "5.4. Cualquier caso no documentado o dudoso debe transferirse de inmediato al área de Operaciones Especiales."
    ),
    (
        "6. NORMAS DE EMBALAJE Y ROTULACIÓN",
        "Guía de Embalaje Seguro para Paquetería y Carga",
        "6.1. Contenedores exteriores: Es obligatorio el uso de cajas de cartón corrugado nuevo de doble pared o guacales de madera tratada para piezas frágiles o pesadas.\n"
        "6.2. Amortiguación interna: Debe dejarse un espacio mínimo de 5 cm entre el producto y las paredes de la caja relleno con burbuja de polietileno de alta densidad o esquineros.\n"
        "6.3. Sellado hermético: Se debe aplicar cinta de embalaje reforzada de al menos 50 mm de ancho siguiendo el patrón de 'H' en las solapas superiores e inferiores.\n"
        "6.4. Bultos pesados: Todo paquete que supere 25 kg de peso bruto debe incorporar flejes de polipropileno cruzados y etiqueta indicativa de manipulación pesada."
    ),
    (
        "7. RASTREO TMS Y EVENTOS DE GUÍA",
        "Seguimiento en Tiempo Real y Estados de Guía",
        "7.1. Identificador de envío: Guía numérica con formato TLX-XXXXXXXX-CO (ejemplo: TLX-84920194-CO).\n"
        "7.2. Consulta directa de estado: Integración con el sistema TMS mediante el endpoint GET /api/v1/tracking/{guia}.\n"
        "7.3. Significado del estado RELECTURA_HUB_FONTIBON: El paquete ingresó al centro principal de clasificación en Bogotá (Zona Franca Fontibón) y se encuentra programado para salir en la ruta nocturna hacia su ciudad de destino.\n"
        "7.4. Otros estados documentados: RECIBIDO_EN_ORIGEN, EN_TRANSITO, EN_CENTRO_DISTRIBUCION, EN_REPARTO, ENTREGADO y NOVEDAD_EN_RUTA."
    ),
    (
        "8. PQRS Y TÉRMINOS LEGALES DE RESPUESTA",
        "Gestión de Peticiones, Quejas, Reclamos y Recursos",
        "8.1. Radicación de PQRS: Se genera de forma automática un código de radicado formal PQR-2026-XXXX accesible para trazabilidad.\n"
        "8.2. Término legal perentorio de respuesta: Máximo 15 días hábiles contados a partir del día siguiente a la radicación, en estricto cumplimiento de la Ley 1755 de 2015 y la Ley 1480 de 2011.\n"
        "8.3. Reclamaciones por pérdida total o avería: Requieren copia de la guía, factura comercial de compra y registro fotográfico de embalaje. La indemnización procederá hasta el 100% del valor declarado verificado.\n"
        "8.4. Ni el chatbot ni el agente virtual tienen potestad para dictar indemnizaciones sin validación del comité de seguros."
    ),
    (
        "9. PROTOCOLO DE ESCALAMIENTO HUMANO INMEDIATO",
        "Criterios de Derivación a Asesores Humanos",
        "9.1. El agente virtual transferirá la conversación de manera inmediata y obligatoria a un asesor humano en cualquiera de los siguientes escenarios:\n"
        "a) Reclamaciones o PQRS con valor declarado superior a cinco millones de pesos ($5.000.000 COP).\n"
        "b) Amenazas directas de escalamiento a la Superintendencia de Transporte o Superintendencia de Industria y Comercio (SIC).\n"
        "c) Solicitudes provenientes de Clientes Corporativos categorizados como Key Account / VIP.\n"
        "d) Índice de confianza de recuperación RAG inferior a 0.75 o ambigüedades documentales irresolubles.\n"
        "9.2. Al transferir, el sistema genera un resumen estructurado del caso para el agente humano receptor."
    )
]


def init_db(force_refresh: bool = False):
    """Crea las tablas necesarias y siembra los datos corporativos de TransLogix Express."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS politicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seccion TEXT NOT NULL,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL
            )
        """)

        cursor.execute("SELECT COUNT(*) as count FROM politicas")
        count = cursor.fetchone()["count"]

        # Si se fuerza o si la BD tiene las políticas viejas de AgentLocalRag, refrescar con TransLogix
        cursor.execute("SELECT seccion FROM politicas WHERE seccion LIKE '%JORNADA LABORAL%' LIMIT 1")
        has_old_data = cursor.fetchone() is not None

        if count == 0 or force_refresh or has_old_data:
            print("[Backend DB] Sembrando base de datos con políticas oficiales de TransLogix Express...")
            cursor.execute("DELETE FROM politicas")
            now = datetime.now(timezone.utc).isoformat()
            
            records = [
                (sec, tit, cont, now) for sec, tit, cont in TRANSLOGIX_SEED_DATA
            ]
            cursor.executemany("""
                INSERT INTO politicas (seccion, titulo, contenido, fecha_actualizacion)
                VALUES (?, ?, ?, ?)
            """, records)
            conn.commit()
            print(f"[Backend DB] Base de datos actualizada con {len(records)} módulos oficiales de TransLogix.")

        # Verificar y asegurar que las tablas geográficas de Colombia y Destinos Internacionales existan
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='colombia_municipios'")
        has_geo = cursor.fetchone()[0] > 0
        if not has_geo:
            try:
                from backend.db.seed_geo import init_geo_db
                init_geo_db()
            except Exception as e:
                print(f"[Backend DB] Error inicializando datos geográficos: {e}")

        # TABLAS DE SEGURIDAD, AUTENTICACIÓN Y MEMORIA COMPORTAMENTAL DEL USUARIO
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                uid TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                empresa TEXT DEFAULT 'Cliente Particular',
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                fecha_registro TEXT NOT NULL,
                ultimo_login TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_sesiones (
                token TEXT PRIMARY KEY,
                uid TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                fecha_expiracion TEXT NOT NULL,
                FOREIGN KEY (uid) REFERENCES usuarios(uid)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                tipo_evento TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                metadatos_json TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (uid) REFERENCES usuarios(uid)
            )
        """)

        # Índices de Alto Rendimiento e Integridad Referencial
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sesiones_token ON usuario_sesiones(token);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sesiones_uid ON usuario_sesiones(uid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_eventos_uid ON usuario_eventos(uid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_eventos_tipo ON usuario_eventos(tipo_evento);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_eventos_uid_tipo ON usuario_eventos(uid, tipo_evento);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_municipios_depto ON colombia_municipios(departamento);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_municipios_nombre ON colombia_municipios(municipio);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_paises_iso ON destinos_internacionales(codigo_iso);")
        conn.commit()


def get_all_policies() -> List[Dict]:
    """Obtiene todas las políticas almacenadas en la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM politicas ORDER BY id ASC")
        return [dict(row) for row in cursor.fetchall()]


def get_policy_by_id(policy_id: int) -> Optional[Dict]:
    """Obtiene una política por su ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM politicas WHERE id = ?", (policy_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_policy(policy_id: int, contenido: str, titulo: Optional[str] = None) -> bool:
    """Actualiza el contenido y fecha de una política existente."""
    with get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        if titulo:
            cursor.execute("""
                UPDATE politicas 
                SET contenido = ?, titulo = ?, fecha_actualizacion = ?
                WHERE id = ?
            """, (contenido, titulo, now, policy_id))
        else:
            cursor.execute("""
                UPDATE politicas 
                SET contenido = ?, fecha_actualizacion = ?
                WHERE id = ?
            """, (contenido, now, policy_id))
        conn.commit()
        return cursor.rowcount > 0


def add_policy(seccion: str, titulo: str, contenido: str) -> int:
    """Añade una nueva política a la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO politicas (seccion, titulo, contenido, fecha_actualizacion)
            VALUES (?, ?, ?, ?)
        """, (seccion, titulo, contenido, now))
        conn.commit()
        return cursor.lastrowid


def compile_knowledge_document() -> str:
    """Compila todas las políticas registradas en un texto plano para re-indexación."""
    policies = get_all_policies()
    lines = [
        "==================================================================",
        "MANUAL CORPORATIVO Y OPERATIVO TRANSLOGIX EXPRESS S.A.S.",
        f"Compilado automáticamente desde Base de Datos el {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "==================================================================\n"
    ]
    for p in policies:
        lines.append(f"## {p['seccion']}")
        lines.append(f"Título: {p['titulo']}")
        lines.append(p["contenido"])
        lines.append("\n" + "-" * 50 + "\n")
    return "\n".join(lines)


# ==============================================================================
# CONSULTAS DE LA BASE DE DATOS GEOGRÁFICA (COLOMBIA & INTERNACIONAL)
# ==============================================================================

def get_all_departamentos() -> List[str]:
    """Retorna la lista de todos los departamentos registrados de Colombia."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT departamento FROM colombia_municipios ORDER BY departamento ASC")
        return [row[0] for row in cursor.fetchall()]


def search_municipios(departamento: Optional[str] = None, q: Optional[str] = None, limit: int = 200) -> List[Dict]:
    """Busca municipios por departamento o término de búsqueda."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM colombia_municipios WHERE 1=1"
        params = []

        if departamento:
            query += " AND (LOWER(departamento) = LOWER(?) OR LOWER(departamento) LIKE LOWER(?))"
            params.extend([departamento, f"%{departamento}%"])

        if q:
            query += " AND (LOWER(municipio) LIKE LOWER(?) OR codigo_dane LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%"])

        query += " ORDER BY departamento ASC, municipio ASC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_all_destinos_internacionales() -> List[Dict]:
    """Retorna los países y destinos oficiales de Courier Internacional."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destinos_internacionales WHERE activo = 1 ORDER BY pais ASC")
        return [dict(row) for row in cursor.fetchall()]


def get_geo_summary() -> Dict:
    """Retorna un resumen cuantitativo de la base de datos geográfica descargada."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(DISTINCT departamento) FROM colombia_municipios")
        total_dep = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM colombia_municipios")
        total_mun = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM destinos_internacionales WHERE activo = 1")
        total_paises = cursor.fetchone()[0]

        return {
            "total_departamentos": total_dep,
            "total_municipios": total_mun,
            "total_paises_internacionales": total_paises,
            "hubs_principales": [
                "Hub Central Zona Franca Fontibón (Bogotá D.C.)",
                "Hub Regional Itagüí / Rionegro (Medellín)",
                "Hub Regional Yumbo (Cali)",
                "Hub Regional Malambo (Barranquilla)",
                "Hub Bucaramanga",
                "Hub Regional Eje Cafetero (Pereira / Manizales)",
                "Hub Villavicencio (Orinoquía)"
            ]
        }


# ==============================================================================
# SEGURIDAD, AUTENTICACIÓN Y SESIONES DE USUARIO
# ==============================================================================

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Genera hash seguro PBKDF2-HMAC-SHA256 con salt."""
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return pw_hash, salt


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Verifica la contraseña contra el hash almacenado usando tiempo constante."""
    pw_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(pw_hash, expected_hash)


def register_user(email: str, password: str, nombre: str, empresa: str = "Cliente Particular") -> Dict:
    """Registra un nuevo usuario con UID criptográfico, hash con salt y sesión activa."""
    email_clean = email.strip().lower()
    uid = "usr_" + secrets.token_hex(8)
    pw_hash, salt = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM usuarios WHERE email = ?", (email_clean,))
        if cursor.fetchone():
            raise ValueError(f"El correo '{email_clean}' ya se encuentra registrado.")

        cursor.execute("""
            INSERT INTO usuarios (uid, email, nombre, empresa, password_hash, salt, fecha_registro, ultimo_login)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, email_clean, nombre.strip(), empresa.strip(), pw_hash, salt, now, now))
        conn.commit()

    token = create_session(uid)
    record_user_event(
        uid=uid,
        tipo_evento="REGISTRO_USUARIO",
        descripcion=f"Usuario {nombre} registrado exitosamente.",
        metadatos={"email": email_clean, "empresa": empresa}
    )

    return {
        "uid": uid,
        "email": email_clean,
        "nombre": nombre,
        "empresa": empresa,
        "token": token
    }


def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Valida credenciales de usuario y genera un nuevo token de sesión."""
    email_clean = email.strip().lower()
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email_clean,))
        row = cursor.fetchone()
        if not row:
            return None

        user = dict(row)
        if not verify_password(password, user["salt"], user["password_hash"]):
            return None

        cursor.execute("UPDATE usuarios SET ultimo_login = ? WHERE uid = ?", (now, user["uid"]))
        conn.commit()

    token = create_session(user["uid"])
    record_user_event(
        uid=user["uid"],
        tipo_evento="LOGIN_USUARIO",
        descripcion=f"Inicio de sesión correcto para {user['nombre']}.",
        metadatos={"email": email_clean}
    )

    return {
        "uid": user["uid"],
        "email": user["email"],
        "nombre": user["nombre"],
        "empresa": user["empresa"],
        "token": token
    }


def create_session(uid: str, days_valid: int = 30) -> str:
    """Crea una sesión persistente en SQLite con token aleatorio."""
    token = "tlx_tok_" + secrets.token_hex(24)
    now = datetime.now(timezone.utc)
    expires = (now + timedelta(days=days_valid)).isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario_sesiones (token, uid, fecha_creacion, fecha_expiracion)
            VALUES (?, ?, ?, ?)
        """, (token, uid, now.isoformat(), expires))
        conn.commit()
    return token


def get_user_by_token(token: str) -> Optional[Dict]:
    """Obtiene el usuario asociado a un token de sesión activo."""
    if not token:
        return None
    token_clean = token.replace("Bearer ", "").strip()
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.uid, u.email, u.nombre, u.empresa, u.fecha_registro, u.ultimo_login
            FROM usuario_sesiones s
            JOIN usuarios u ON s.uid = u.uid
            WHERE s.token = ? AND s.fecha_expiracion > ?
        """, (token_clean, now))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_uid(uid: str) -> Optional[Dict]:
    """Obtiene los datos públicos de un usuario por su UID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT uid, email, nombre, empresa, fecha_registro, ultimo_login FROM usuarios WHERE uid = ?", (uid,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_session(token: str) -> bool:
    """Cierra la sesión de un usuario eliminando el token."""
    token_clean = token.replace("Bearer ", "").strip()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario_sesiones WHERE token = ?", (token_clean,))
        conn.commit()
        return cursor.rowcount > 0


# ==============================================================================
# HISTORIAL COMPORTAMENTAL DEL USUARIO (COTIZACIONES INCOMPLETAS, RASTREO, ETC.)
# ==============================================================================

def record_user_event(uid: str, tipo_evento: str, descripcion: str, metadatos: Optional[dict] = None) -> int:
    """Registra una acción, consulta o intento de envío en el historial del usuario."""
    now = datetime.now(timezone.utc).isoformat()
    meta_str = json.dumps(metadatos or {}, ensure_ascii=False)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario_eventos (uid, tipo_evento, descripcion, metadatos_json, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (uid, tipo_evento, descripcion, meta_str, now))
        conn.commit()
        event_id = cursor.lastrowid

    # Sincronizar en caliente hacia la memoria vectorial de ChromaDB
    try:
        from backend.user_memory import save_user_event_to_vector_memory
        save_user_event_to_vector_memory(uid, tipo_evento, descripcion, metadatos or {})
    except Exception as e:
        print(f"[UserMemory] Aviso sincronización vectorial: {e}")

    return event_id


def get_user_events(uid: str, limit: int = 15) -> List[Dict]:
    """Retorna los eventos y comportamientos más recientes de un usuario."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, uid, tipo_evento, descripcion, metadatos_json, timestamp
            FROM usuario_eventos
            WHERE uid = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (uid, limit))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d["metadatos"] = json.loads(d["metadatos_json"])
            except Exception:
                d["metadatos"] = {}
            result.append(d)
        return result


def get_user_pending_quotes(uid: str, limit: int = 5) -> List[Dict]:
    """Retorna las cotizaciones iniciadas pero no completadas por el usuario."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, uid, tipo_evento, descripcion, metadatos_json, timestamp
            FROM usuario_eventos
            WHERE uid = ? AND tipo_evento = 'COTIZACION_INCOMPLETA'
            ORDER BY timestamp DESC
            LIMIT ?
        """, (uid, limit))
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d["metadatos"] = json.loads(d["metadatos_json"])
            except Exception:
                d["metadatos"] = {}
            result.append(d)
        return result


# Inicializar la base de datos si se importa o ejecuta
init_db()
