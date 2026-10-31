"""
backend/agent_client.py - Cliente HTTP para consumir la API del Agente RAG (AgentLocalRag).
Permite consultar al agente y notificarle que debe auto-indexar cuando cambien los datos.
"""

import httpx
from typing import Dict, Any, Optional, List


class AgentClient:
    """Cliente para comunicarse con el servidor del Agente RAG Local."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 60.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def ask(self, pregunta: str, session_id: str = "default", reset_history: bool = False) -> Dict[str, Any]:
        """
        Envía una pregunta al agente y retorna la respuesta en formato JSON.
        Incluye la respuesta natural, fuentes consultadas, fecha y tiempo de ejecución.
        """
        url = f"{self.base_url}/api/ask"
        payload = {
            "pregunta": pregunta,
            "session_id": session_id,
            "reset_history": reset_history,
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    def notify_reindex(
        self,
        clean: bool = True,
        filename: Optional[str] = None,
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Le solicita al agente que ejecute la re-indexación de la base vectorial.
        Opcionalmente puede enviarle el archivo o contenido nuevo compilado desde la BD.
        """
        url = f"{self.base_url}/api/reindex"
        payload = {
            "clean": clean,
            "filename": filename,
            "content": content,
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            return response.json()

    def get_health(self) -> Dict[str, Any]:
        """Verifica el estado de salud del agente y modelos activos."""
        url = f"{self.base_url}/health"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def list_documents(self) -> Dict[str, Any]:
        """Lista los documentos que el agente tiene actualmente cargados."""
        url = f"{self.base_url}/api/documents"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

