# 🏢 Backend de Negocio - AgentLocalRag

Este directorio contiene el backend desacoplado que gestiona la base de datos empresarial y se comunica con el **Agente RAG Local** vía API HTTP.

---

## 📁 Estructura

- **`db/database.py`**: Gestión de la base de datos SQLite (`agent_local_rag.db`). Contiene las políticas y funciones CRUD.
- **`agent_client.py`**: Cliente HTTP que consume la API del Agente (`http://localhost:8000`), tanto para consultar (`/api/ask`) como para ordenar la re-indexación (`/api/reindex`).
- **`service.py`**: Lógica de sincronización. Al modificar una política en la BD, invoca automáticamente la auto-indexación en el Agente RAG.
- **`server.py`**: Servidor API REST del backend en el puerto `5001` (FastAPI).
- **`demo_sync.py`**: Script de prueba automatizada del ciclo completo (Modificación en BD -> Auto-indexación -> Verificación de respuesta en Agente).

---

## 🚀 Ejecución del Backend

Para iniciar el servidor backend empresarial:

```bash
python backend/server.py
```

- **URL:** `http://localhost:5001`
- **Swagger Docs:** `http://localhost:5001/docs`

---

## 🧪 Demostración del Flujo de Auto-Indexación

Con el agente corriendo (`python app.py` en el puerto 8000), ejecuta:

```bash
python backend/demo_sync.py
```

