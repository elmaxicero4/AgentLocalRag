"""
backend/db/database.py - Base de datos corporativa independiente (SQLite).
Almacena y gestiona las políticas, normativas y registros de AgentLocalRag.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional

DB_DIR = Path(__file__).resolve().parent
DB_FILE = DB_DIR / "agent_local_rag.db"


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a la base de datos SQLite con formato de fila diccionario."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias y siembra los datos iniciales si está vacía."""
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

        # Verificar si ya tiene registros
        cursor.execute("SELECT COUNT(*) as count FROM politicas")
        count = cursor.fetchone()["count"]

        if count == 0:
            print("[Backend DB] Inicializando base de datos con políticas base...")
            now = datetime.now(timezone.utc).isoformat()
            initial_data = [
                (
                    "1. JORNADA LABORAL Y HORARIOS",
                    "Horarios y Turnos",
                    "1.1. La jornada ordinaria de trabajo es de lunes a viernes en horario flexible, con presencia requerida entre las 10:00 y las 16:00 horas (Zona Horaria GMT-5).\n1.2. El equipo de soporte técnico opera en turnos rotativos continuos de 8 horas: Turno Matutino (06:00 a 14:00), Turno Vespertino (14:00 a 22:00) y Turno Nocturno (22:00 a 06:00).\n1.3. La pausa para el almuerzo tiene una duración de exactamente 60 minutos y debe tomarse entre las 12:00 y las 14:30.",
                    now
                ),
                (
                    "2. POLÍTICA DE VACACIONES Y PERMISOS",
                    "Vacaciones y Licencias",
                    "2.1. Todo empleado contratado a término indefinido tiene derecho a 15 días hábiles remunerados de vacaciones por cada año completo de servicio.\n2.2. Las solicitudes de vacaciones deben radicarse en el portal interno con un mínimo de 20 días calendario de antelación.\n2.3. Se conceden hasta 3 días hábiles de permiso remunerado por motivos de mudanza, aplicable máximo una vez cada dos años.\n2.4. En caso de matrimonio del colaborador, se otorga una licencia remunerada especial de 5 días hábiles continuos.",
                    now
                ),
                (
                    "3. SEGURIDAD DE LA INFORMACIÓN Y EQUIPAMIENTO",
                    "Seguridad y Ciberseguridad",
                    "3.1. Todos los ordenadores corporativos deben contar con cifrado de disco completo (FileVault en macOS o BitLocker en Windows).\n3.2. La longitud mínima obligatoria de las contraseñas maestras es de 16 caracteres, combinando mayúsculas, minúsculas, números y caracteres especiales.\n3.3. Las contraseñas expiran cada 90 días calendario y no se pueden reutilizar las últimas 5 contraseñas anteriores.\n3.4. Es obligatorio el uso de autenticación de dos factores (2FA) basada en aplicaciones TOTP (1Password o Google Authenticator); los SMS no están autorizados como método 2FA.\n3.5. Queda terminantemente prohibido almacenar contraseñas o credenciales de producción en archivos de texto plano, notas adhesivas o repositorios de código sin cifrar.",
                    now
                ),
                (
                    "4. POLÍTICA DE REEMBOLSO DE GASTOS",
                    "Subsidios y Reembolsos",
                    "4.1. El límite mensual para gastos de formación continua y libros técnicos es de 150 USD por empleado, previa aprobación del líder de área.\n4.2. El subsidio mensual de conectividad e internet para colaboradores en modalidad 100% remota es de 45 USD netos.\n4.3. Las facturas y comprobantes de gasto deben presentarse antes del día 25 de cada mes fiscal. Los recibos extemporáneos se liquidarán en el ciclo siguiente.",
                    now
                ),
                (
                    "5. CONTACTOS CLAVE Y ESCALAMIENTO",
                    "Contactos y Soporte",
                    "5.1. El área de Talento Humano se contacta vía talento@agentlocalrag.internal.\n5.2. Los incidentes de ciberseguridad clasificados como SEV-1 deben notificarse de inmediato al canal de Slack #soc-urgent y al correo secops@agentlocalrag.internal.\n5.3. El Oficial de Privacidad y Cumplimiento de Datos es el Licenciado Roberto Morales.",
                    now
                ),
            ]
            cursor.executemany("""
                INSERT INTO politicas (seccion, titulo, contenido, fecha_actualizacion)
                VALUES (?, ?, ?, ?)
            """, initial_data)
            conn.commit()
            print("[Backend DB] Base de datos sembrada con 5 secciones corporativas.")


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
    """Actualiza el contenido de una política existente."""
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
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


def insert_policy(seccion: str, titulo: str, contenido: str) -> int:
    """Inserta una nueva política en la base de datos y retorna su ID."""
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO politicas (seccion, titulo, contenido, fecha_actualizacion)
            VALUES (?, ?, ?, ?)
        """, (seccion, titulo, contenido, now))
        conn.commit()
        return cursor.lastrowid


def compile_knowledge_document() -> str:
    """
    Compila todas las políticas actuales de la base de datos en un solo
    documento estructurado en Markdown listo para ser indexado por el agente.
    """
    policies = get_all_policies()
    lines = [
        "# MANUAL DE POLÍTICAS Y PROCEDIMIENTOS INTERNOS - AGENTLOCALRAG",
        f"# Exportado desde la Base de Datos Central el: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        ""
    ]

    for p in policies:
        lines.append(f"## {p['seccion']}")
        lines.append(p['contenido'].strip())
        lines.append("")

    return "\n".join(lines)


# Inicializar la base de datos al importar el módulo
init_db()

