# 💻 Frontend - AgentLocalRag (AI Chat & Auto-Indexación en Vivo)

Interfaz web moderna, reactiva y desacoplada para interactuar con el **Agente RAG Local (Puerto 8000)** y el **Backend de Base de Datos (Puerto 5001)**.

---

## 🌟 Características Principales

1. **💬 Chat Conversacional Factual**:
   - Conexión directa vía HTTP REST con `POST http://localhost:8000/api/ask`.
   - Renderizado dinámico de respuestas en Markdown con citas textuales.
   - Visualización de fuentes documentales consultadas (nombre de archivo, fragmento y score de similitud).
   - Metadatos en tiempo real: modelo activo (`qwen3.6:35b`), tiempo exacto de inferencia (segundos) y hora UTC.
   - Memoria conversacional por sesión.

2. **📋 Panel de Políticas en Base de Datos**:
   - Conexión con `GET http://localhost:5001/policies` del Backend.
   - Muestra las normativas almacenadas en SQLite (`backend/db/agent_local_rag.db`).
   - Permite hacer clic en cualquier política para cargarla en el editor.

3. **➕ Modal de Modificación de Base de Datos**:
   - Selector para crear nueva política o modificar una existente.
   - `<textarea>` de texto enriquecido para redactar políticas, horarios o montos.
   - Botón de acción: **"Guardar en BD y Auto-Indexar"**.

4. **⏳ Modal de Carga con Barra de Progreso ("Subiendo e Indexando")**:
   - Al pulsar guardar, se abre una modal de progreso animada con 4 etapas:
     1. `[✔] 1. Guardar en Base de Datos SQLite (Backend)`
     2. `[✔] 2. Backend notifica re-indexación vía API`
     3. `[✔] 3. Agente regenera embeddings con BGE-M3`
     4. `[✔] 4. Base Vectorial ChromaDB lista en caliente`
   - La barra avanza de 0% a 100%. Al recibir la confirmación de éxito (`status: "success"` del agente), muestra el check verde y **se cierra automáticamente**.
   - En el chat se inserta una tarjeta de confirmación notificando que el agente ya aprendió la nueva información.

---

## 🚀 Cómo Ejecutar la Interfaz

### Método 1: Directo desde el Servidor del Agente (Recomendado)
El servidor del agente (`api.py` / `app.py`) tiene la interfaz web montada en la ruta raíz.

1. Inicia el Agente:
   ```bash
   python app.py
   ```
2. En otra terminal, inicia el Backend:
   ```bash
   python backend/server.py
   ```
3. Abre tu navegador en:
   👉 **`http://localhost:8000`**

---

### Método 2: Servidor Estático Independiente (Puerto 3000)
Si deseas correr el frontend de manera completamente aislada:

```bash
python -m http.server 3000 --directory frontend
```
Abre en tu navegador:
👉 **`http://localhost:3000`**

---

### Método 3: Doble Clic
También puedes abrir directamente el archivo `frontend/index.html` en tu navegador favorito (Chrome, Safari, Edge, Firefox). Gracias al middleware de CORS configurado en ambos servidores, funcionará perfectamente.

---

## 🛠️ Guía de Arquitectura para Construirlo en React / Vue / Next.js

Si deseas migrar esta interfaz a componentes en **React / Vite / Next.js**, a continuación se detalla la arquitectura de estado y los hooks recomendados:

### Estructura de Componentes Sugerida:
```text
src/
├── components/
│   ├── Header.tsx              # Badges de conexión (Agente:8000 y Backend:5000)
│   ├── SidebarPolicies.tsx     # Lista de políticas desde Backend
│   ├── ChatContainer.tsx       # Historial de mensajes y fuentes
│   ├── ChatInput.tsx           # Input con botón de envío
│   ├── PolicyModal.tsx         # Modal con textarea para crear/editar
│   └── LoadingModal.tsx        # Modal con progress bar de auto-indexación
├── services/
│   ├── agentApi.ts             # fetch a http://localhost:8000
│   └── backendApi.ts           # fetch a http://localhost:5000
└── App.tsx
```

### 1. Servicio del Agente (`services/agentApi.ts`):
```typescript
export async function askAgent(pregunta: string, sessionId: string = "default") {
  const res = await fetch("http://localhost:8000/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pregunta, session_id: sessionId })
  });
  if (!res.ok) throw new Error("Error consultando al agente");
  return await res.json();
}
```

### 2. Servicio del Backend (`services/backendApi.ts`):
```typescript
export async function savePolicyAndAutoIndex(policy: { seccion: string; titulo: string; contenido: string }, id?: number) {
  const url = id ? `http://localhost:5000/policies/${id}` : `http://localhost:5000/policies`;
  const method = id ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(policy)
  });
  if (!res.ok) throw new Error("Error guardando política");
  return await res.json();
}
```

### 3. Hook para la barra de carga de Auto-Indexación:
```typescript
const [progress, setProgress] = useState(0);
const [stepText, setStepText] = useState("");
const [isLoading, setIsLoading] = useState(false);

async function handleSavePolicy(data) {
  setIsLoading(true);
  setProgress(25);
  setStepText("Guardando en Base de Datos SQLite...");

  setTimeout(() => { setProgress(60); setStepText("Notificando al Agente RAG vía API..."); }, 400);
  setTimeout(() => { setProgress(85); setStepText("Agente regenerando vectores con BGE-M3..."); }, 800);

  try {
    const result = await savePolicyAndAutoIndex(data);
    setProgress(100);
    setStepText("¡Auto-indexación completada!");
    
    // Cerrar modal automáticamente
    setTimeout(() => {
      setIsLoading(false);
    }, 1200);
  } catch (error) {
    setIsLoading(false);
    alert(error.message);
  }
}
```
