"""
backend/demo_sync.py - Demostración en vivo del flujo de auto-indexación.

Demuestra:
1. Consulta inicial al Agente RAG.
2. Cambio de un valor en la Base de Datos SQLite del Backend.
3. El Backend notifica a la API del Agente para que auto-indexe por sí solo.
4. Consulta posterior: El Agente responde con la nueva información actualizada sin reiniciar nada.
"""

import time
import sys
from pathlib import Path

# Agregar directorio actual al sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from service import (
    get_policy_by_id,
    update_policy_and_autoindex,
    ask_agent_through_backend
)


def run_demo():
    print("=" * 70)
    print("🧪 DEMOSTRACIÓN: CAMBIO EN BD -> AUTO-INDEXACIÓN EN EL AGENTE RAG")
    print("=" * 70)

    pregunta = "¿Cuánto es el subsidio mensual de conectividad e internet para colaboradores remotos?"

    # 1. Consulta inicial
    print("\n[Paso 1] Consultando al Agente RAG antes del cambio...")
    resp1 = ask_agent_through_backend(pregunta)
    print(f"👉 Respuesta del Agente:")
    print(f"   {resp1['respuesta']}\n")

    # 2. Modificar el valor en la Base de Datos (Política #4: Reembolso de Gastos)
    print("[Paso 2] Modificando el valor del subsidio en la Base de Datos SQLite del Backend...")
    politica_original = get_policy_by_id(4)
    contenido_original = politica_original["contenido"]

    # Cambiar de 45 USD a 95 USD
    nuevo_contenido = contenido_original.replace("45 USD netos", "95 USD netos (Incrementado por acuerdo sindical)")

    # Esta función actualiza SQLite y automáticamente llama a POST /api/reindex del Agente
    resultado_sync = update_policy_and_autoindex(
        policy_id=4,
        nuevo_contenido=nuevo_contenido
    )
    print(f"✔ Base de datos actualizada: {resultado_sync['mensaje']}")
    print(f"✔ Fragmentos re-indexados por el Agente: {resultado_sync['autoindex_resultado']['fragmentos_indexados']}")
    print(f"✔ Tiempo de re-indexación: {resultado_sync['autoindex_resultado']['tiempo_ejecucion_segundos']}s\n")

    # 3. Consulta posterior al Agente
    print("[Paso 3] Consultando al Agente RAG tras la auto-indexación...")
    resp2 = ask_agent_through_backend(pregunta)
    print(f"👉 Nueva Respuesta del Agente:")
    print(f"   {resp2['respuesta']}\n")

    # 4. Restaurar el valor original
    print("[Paso 4] Restaurando el valor original (45 USD) en la Base de Datos...")
    update_policy_and_autoindex(policy_id=4, nuevo_contenido=contenido_original)
    print("✔ Valor original restaurado y base re-indexada.\n")

    print("=" * 70)
    print("🎉 Demostración completada con éxito. El agente aprendió el nuevo dato automáticamente.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()

