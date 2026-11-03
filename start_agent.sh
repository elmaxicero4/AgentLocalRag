#!/usr/bin/env bash
# start_agent.sh - Inicia el Agente RAG, genera el túnel público y abre el portal interactivo de documentación
set -e

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ejecutar el lanzador del agente
python3 run_agent.py "$@"

