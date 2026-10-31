"""
app.py - Punto de entrada para levantar la API REST de AgentLocalRag.
"""

from api import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Levantando servidor API en http://localhost:8000")
    print("📖 Swagger UI disponible en http://localhost:8000/docs")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
