/**
 * frontend/app.js - Lógica interactiva del Frontend para AgentLocalRag.
 * Conecta con el Agente RAG (puerto 8000) y el Backend empresarial (puerto 5001).
 */

const AGENT_API_URL = "http://localhost:8000";
const BACKEND_API_URL = "http://localhost:5001";
const SESSION_ID = "frontend_session_" + Math.random().toString(36).substring(2, 9);

let currentPolicies = [];

// Elementos del DOM
const agentStatusDot = document.getElementById("agentStatusDot");
const agentStatusText = document.getElementById("agentStatusText");
const backendStatusDot = document.getElementById("backendStatusDot");
const backendStatusText = document.getElementById("backendStatusText");
const lblModelName = document.getElementById("lblModelName");

// Selector de modelos y Badges
const selectModel = document.getElementById("selectModel");
const modelTierBadge = document.getElementById("modelTierBadge");

// Modal de Benchmark
const btnOpenBenchmark = document.getElementById("btnOpenBenchmark");
const benchmarkModal = document.getElementById("benchmarkModal");
const btnCloseBenchmarkModal = document.getElementById("btnCloseBenchmarkModal");
const selectBenchModelA = document.getElementById("selectBenchModelA");
const selectBenchModelB = document.getElementById("selectBenchModelB");
const inputBenchQuestion = document.getElementById("inputBenchQuestion");
const btnRunBenchmark = document.getElementById("btnRunBenchmark");
const benchNameA = document.getElementById("benchNameA");
const benchTimeA = document.getElementById("benchTimeA");
const benchBodyA = document.getElementById("benchBodyA");
const benchNameB = document.getElementById("benchNameB");
const benchTimeB = document.getElementById("benchTimeB");
const benchBodyB = document.getElementById("benchBodyB");
const benchSummaryBanner = document.getElementById("benchSummaryBanner");
const benchSummaryText = document.getElementById("benchSummaryText");
const benchSpeedDiffBadge = document.getElementById("benchSpeedDiffBadge");

const policiesList = document.getElementById("policiesList");
const btnRefreshPolicies = document.getElementById("btnRefreshPolicies");
const btnForceSync = document.getElementById("btnForceSync");

const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const inputQuestion = document.getElementById("inputQuestion");
const btnSendMessage = document.getElementById("btnSendMessage");
const btnClearChat = document.getElementById("btnClearChat");

// Modales
const policyModal = document.getElementById("policyModal");
const btnOpenPolicyModal = document.getElementById("btnOpenPolicyModal");
const btnClosePolicyModal = document.getElementById("btnClosePolicyModal");
const btnCancelPolicyModal = document.getElementById("btnCancelPolicyModal");
const btnSubmitPolicy = document.getElementById("btnSubmitPolicy");

const selectPolicyAction = document.getElementById("selectPolicyAction");
const inputPolicySection = document.getElementById("inputPolicySection");
const inputPolicyTitle = document.getElementById("inputPolicyTitle");
const textareaPolicyContent = document.getElementById("textareaPolicyContent");

// Loading Modal y Barra de Progreso
const loadingModal = document.getElementById("loadingModal");
const loadingSpinner = document.getElementById("loadingSpinner");
const successCheck = document.getElementById("successCheck");
const loadingTitle = document.getElementById("loadingTitle");
const loadingSubtitle = document.getElementById("loadingSubtitle");
const progressBar = document.getElementById("progressBar");
const loadingStepText = document.getElementById("loadingStepText");
const loadingPercentageText = document.getElementById("loadingPercentageText");
const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const step4 = document.getElementById("step4");


// ==============================================================================
// 1. INICIALIZACIÓN Y VERIFICACIÓN DE ESTADO
// ==============================================================================

async function checkHealth() {
  // 1. Verificar Agente RAG y listar modelos
  try {
    const res = await fetch(`${AGENT_API_URL}/health`);
    if (res.ok) {
      const data = await res.json();
      agentStatusDot.className = "w-2.5 h-2.5 rounded-full bg-emerald-400";
      agentStatusText.textContent = "Conectado";
      agentStatusText.className = "text-emerald-400 font-medium";
      if (lblModelName) lblModelName.textContent = data.modelo || "qwen3.6:35b";
      await loadAvailableModels(data.modelo);
    } else {
      throw new Error();
    }
  } catch (e) {
    agentStatusDot.className = "w-2.5 h-2.5 rounded-full bg-red-400";
    agentStatusText.textContent = "Sin conexión (puerto 8000)";
    agentStatusText.className = "text-red-400 font-medium";
  }

  // 2. Verificar Backend BD
  try {
    const res = await fetch(`${BACKEND_API_URL}/policies`);
    if (res.ok) {
      backendStatusDot.className = "w-2.5 h-2.5 rounded-full bg-emerald-400";
      backendStatusText.textContent = "Conectado";
      backendStatusText.className = "text-emerald-400 font-medium";
      await loadPolicies();
    } else {
      throw new Error();
    }
  } catch (e) {
    backendStatusDot.className = "w-2.5 h-2.5 rounded-full bg-red-400";
    backendStatusText.textContent = "Sin conexión (puerto 5001)";
    backendStatusText.className = "text-red-400 font-medium";
    policiesList.innerHTML = `
      <div class="text-center p-4 text-xs text-red-400 bg-red-950/20 border border-red-900/40 rounded-xl">
        Backend no detectado en el puerto 5001.<br>
        Inícialo con: <code class="text-slate-300">python backend/server.py</code>
      </div>
    `;
  }
}

let availableModelsList = [];

async function loadAvailableModels(activeModelName) {
  try {
    const res = await fetch(`${AGENT_API_URL}/api/models`);
    if (!res.ok) return;
    const data = await res.json();
    availableModelsList = data.models || [];
    const active = activeModelName || data.active_model;

    // Presets esenciales si no están en la lista
    const basePresets = [
      { id: "qwen2.5:7b-instruct", label: "⚡ Qwen 2.5 7B (Ultra Rápido)", tier: "7B" },
      { id: "qwen2.5-coder:14b", label: "⚖️ Qwen 2.5 Coder 14B (Equilibrado)", tier: "14B" },
      { id: "qwen2.5-coder:32b", label: "🚀 Qwen 2.5 Coder 32B (Razonamiento Alto)", tier: "32B" },
      { id: "qwen3.6:35b", label: "🧠 Qwen 3.6 35B (MoE Profundo)", tier: "35B" },
    ];

    // Construir opciones del dropdown principal
    const optionsHtml = basePresets.map(p => {
      const isSelected = (p.id === active || (active && active.startsWith(p.id)));
      return `<option value="${p.id}" ${isSelected ? "selected" : ""}>${p.label}</option>`;
    }).join("") + (availableModelsList.filter(m => !basePresets.some(bp => bp.id === m.id)).map(m => `
      <option value="${m.id}">${m.id} (${m.size_gb} GB - ${m.tier})</option>
    `).join(""));

    if (selectModel) {
      selectModel.innerHTML = optionsHtml;
      updateModelBadge();
    }

    if (selectBenchModelA) {
      selectBenchModelA.innerHTML = optionsHtml;
      selectBenchModelA.value = "qwen2.5:7b-instruct";
    }

    if (selectBenchModelB) {
      selectBenchModelB.innerHTML = optionsHtml;
      selectBenchModelB.value = "qwen2.5-coder:32b";
    }

  } catch (err) {
    console.warn("No se pudieron cargar modelos dinámicos:", err);
  }
}

function updateModelBadge() {
  if (!selectModel || !modelTierBadge) return;
  const val = selectModel.value;
  if (val.includes("7b") || val.includes("8b")) {
    modelTierBadge.textContent = "⚡ 7B • Ultra Rápido (<1.5s)";
    modelTierBadge.className = "bg-emerald-950/70 border border-emerald-800 text-emerald-300 text-[10px] px-2 py-0.5 rounded-full font-mono";
  } else if (val.includes("14b")) {
    modelTierBadge.textContent = "⚖️ 14B • Balance Calidad/Velocidad";
    modelTierBadge.className = "bg-blue-950/70 border border-blue-800 text-blue-300 text-[10px] px-2 py-0.5 rounded-full font-mono";
  } else if (val.includes("32b")) {
    modelTierBadge.textContent = "🚀 32B • Razonamiento Alto";
    modelTierBadge.className = "bg-cyan-950/70 border border-cyan-800 text-cyan-300 text-[10px] px-2 py-0.5 rounded-full font-mono";
  } else if (val.includes("35b")) {
    modelTierBadge.textContent = "🧠 35B • MoE Avanzado";
    modelTierBadge.className = "bg-purple-950/70 border border-purple-800 text-purple-300 text-[10px] px-2 py-0.5 rounded-full font-mono";
  } else {
    modelTierBadge.textContent = "🤖 Modelo Local";
    modelTierBadge.className = "bg-slate-800 border border-slate-700 text-slate-300 text-[10px] px-2 py-0.5 rounded-full font-mono";
  }
}

if (selectModel) {
  selectModel.addEventListener("change", () => {
    updateModelBadge();
  });
}


// ==============================================================================
// 2. GESTIÓN DE POLÍTICAS EN EL PANEL LATERAL
// ==============================================================================

async function loadPolicies() {
  try {
    const res = await fetch(`${BACKEND_API_URL}/policies`);
    if (!res.ok) return;
    const data = await res.json();
    currentPolicies = data.politicas || [];

    if (currentPolicies.length === 0) {
      policiesList.innerHTML = `<div class="text-center text-xs text-slate-500 py-4">No hay políticas en BD.</div>`;
      return;
    }

    policiesList.innerHTML = currentPolicies.map(p => `
      <div class="p-3 bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 rounded-xl transition cursor-pointer group" onclick="openEditPolicy(${p.id})">
        <div class="flex items-center justify-between mb-1">
          <span class="text-[11px] font-bold text-cyan-400 group-hover:text-cyan-300 transition truncate max-w-[190px]">
            ${escapeHtml(p.seccion)}
          </span>
          <span class="text-[10px] text-slate-500 bg-slate-900 px-1.5 py-0.5 rounded">#${p.id}</span>
        </div>
        <p class="text-xs font-medium text-slate-200 mb-1 line-clamp-1">${escapeHtml(p.titulo)}</p>
        <p class="text-[11px] text-slate-400 line-clamp-2 font-mono">${escapeHtml(p.contenido)}</p>
      </div>
    `).join("");

    updatePolicySelectOptions();

  } catch (e) {
    console.error("Error al cargar políticas:", e);
  }
}

function updatePolicySelectOptions() {
  selectPolicyAction.innerHTML = `
    <option value="new">➕ Crear Nueva Política en Base de Datos</option>
    <optgroup label="Editar Política Existente">
      ${currentPolicies.map(p => `
        <option value="${p.id}">Editar: #${p.id} - ${escapeHtml(p.seccion)}</option>
      `).join("")}
    </optgroup>
  `;
}


// ==============================================================================
// 3. CHAT CON EL AGENTE RAG
// ==============================================================================

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = inputQuestion.value.trim();
  if (!question) return;

  const chosenModel = selectModel ? selectModel.value : null;

  // 1. Agregar mensaje del usuario en el chat
  appendUserMessage(question);
  inputQuestion.value = "";
  inputQuestion.focus();

  // 2. Mostrar burbuja de carga / pensando
  const loadingBubbleId = appendAgentLoadingMessage(chosenModel);

  try {
    const res = await fetch(`${AGENT_API_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pregunta: question,
        session_id: SESSION_ID,
        modelo: chosenModel,
      })
    });

    if (!res.ok) {
      throw new Error(`Error en servidor del Agente: ${res.status}`);
    }

    const data = await res.json();
    replaceLoadingWithResponse(loadingBubbleId, data);

  } catch (error) {
    replaceLoadingWithError(loadingBubbleId, error.message);
  }
});

function appendUserMessage(text) {
  const div = document.createElement("div");
  div.className = "flex items-start justify-end space-x-3";
  div.innerHTML = `
    <div class="bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-2xl text-sm shadow-md">
      <p class="leading-relaxed whitespace-pre-wrap">${escapeHtml(text)}</p>
    </div>
    <div class="w-8 h-8 rounded-lg bg-slate-700 flex items-center justify-center shrink-0 text-slate-300">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
      </svg>
    </div>
  `;
  chatContainer.appendChild(div);
  scrollToBottom();
}

function appendAgentLoadingMessage(modelLabel) {
  const id = "loading_" + Date.now();
  const div = document.createElement("div");
  div.id = id;
  div.className = "flex items-start space-x-3 max-w-3xl";
  const label = modelLabel || (selectModel ? selectModel.value : "modelo local");
  div.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shrink-0 shadow-md animate-pulse">
      <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
      </svg>
    </div>
    <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 shadow-sm text-sm text-slate-300 flex items-center space-x-3">
      <svg class="w-4 h-4 text-cyan-400 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-slate-400 text-xs">Consultando base de datos y razonando con <strong>${escapeHtml(label)}</strong>...</span>
    </div>
  `;
  chatContainer.appendChild(div);
  scrollToBottom();
  return id;
}

function replaceLoadingWithResponse(bubbleId, data) {
  const loadingElem = document.getElementById(bubbleId);
  if (!loadingElem) return;

  const htmlResponse = marked.parse(data.respuesta || "");
  const timeFormatted = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const sec = data.tiempo_respuesta_segundos;

  let speedBadge = "";
  if (sec < 2.0) {
    speedBadge = `<span class="bg-emerald-950/80 text-emerald-300 border border-emerald-800 text-[10px] px-2 py-0.5 rounded-full font-mono">⚡ ${sec}s • Ultra Rápido</span>`;
  } else if (sec < 6.0) {
    speedBadge = `<span class="bg-cyan-950/80 text-cyan-300 border border-cyan-800 text-[10px] px-2 py-0.5 rounded-full font-mono">⚖️ ${sec}s • Equilibrado</span>`;
  } else {
    speedBadge = `<span class="bg-purple-950/80 text-purple-300 border border-purple-800 text-[10px] px-2 py-0.5 rounded-full font-mono">🧠 ${sec}s • Razonamiento Profundo</span>`;
  }

  // Renderizar acordeón de fuentes si existen
  let fuentesHtml = "";
  if (data.fuentes && data.fuentes.length > 0) {
    const fuentesListHtml = data.fuentes.map((f, i) => `
      <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 mb-2 last:mb-0 text-xs">
        <div class="flex items-center justify-between text-[11px] mb-1">
          <span class="font-bold text-yellow-400 font-mono">📄 ${escapeHtml(f.archivo)}</span>
          <span class="text-emerald-400 bg-emerald-950/60 border border-emerald-900 px-1.5 py-0.2 rounded font-mono">
            Score: ${f.score !== null ? f.score.toFixed(4) : "N/A"}
          </span>
        </div>
        <p class="text-slate-300 font-mono text-[11px] leading-relaxed whitespace-pre-wrap">${escapeHtml(f.fragmento)}</p>
      </div>
    `).join("");

    fuentesHtml = `
      <div class="mt-3 pt-3 border-t border-slate-800">
        <details class="group cursor-pointer">
          <summary class="text-xs font-semibold text-slate-400 hover:text-cyan-400 transition flex items-center space-x-1 select-none">
            <svg class="w-3.5 h-3.5 text-cyan-400 transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
            <span>📚 Fuentes y Nodos Recuperados (${data.fuentes.length})</span>
          </summary>
          <div class="mt-2 pl-4">
            ${fuentesListHtml}
          </div>
        </details>
      </div>
    `;
  }

  loadingElem.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shrink-0 shadow-md">
      <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
      </svg>
    </div>
    <div class="flex-1 bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 shadow-sm text-sm text-slate-200">
      
      <!-- Barra superior de benchmark del mensaje -->
      <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800/80 text-[11px]">
        <div class="flex items-center space-x-1.5">
          <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
          <span class="font-mono text-cyan-300 font-bold">${escapeHtml(data.modelo)}</span>
        </div>
        ${speedBadge}
      </div>

      <!-- Contenido de respuesta -->
      <div class="prose prose-invert prose-sm max-w-none leading-relaxed">
        ${htmlResponse}
      </div>

      <!-- Fuentes -->
      ${fuentesHtml}

      <!-- Metadatos de inferencia en el pie -->
      <div class="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-500">
        <span>Sesión: <code class="text-slate-400">${escapeHtml(data.session_id || "default")}</code></span>
        <div class="flex items-center space-x-3">
          <span>Tiempo: <strong class="text-cyan-400">${data.tiempo_respuesta_segundos}s</strong></span>
          <span>${timeFormatted}</span>
        </div>
      </div>

    </div>
  `;
  scrollToBottom();
}

function replaceLoadingWithError(bubbleId, errMsg) {
  const loadingElem = document.getElementById(bubbleId);
  if (!loadingElem) return;
  loadingElem.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center shrink-0 text-white shadow-md">
      !
    </div>
    <div class="flex-1 bg-red-950/30 border border-red-900/50 rounded-2xl rounded-tl-none p-4 text-sm text-red-200">
      <p class="font-bold text-red-400 mb-1">Error al consultar al Agente</p>
      <p class="text-xs text-red-300">${escapeHtml(errMsg)}</p>
    </div>
  `;
  scrollToBottom();
}

function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

btnClearChat.addEventListener("click", () => {
  chatContainer.innerHTML = `
    <div class="text-center text-xs text-slate-500 py-4">
      Conversación reiniciada. Puedes formular una nueva pregunta.
    </div>
  `;
});


// ==============================================================================
// 4. MODAL DE ALIMENTAR / MODIFICAR BASE DE DATOS
// ==============================================================================

btnOpenPolicyModal.addEventListener("click", () => {
  selectPolicyAction.value = "new";
  onActionChange();
  policyModal.classList.remove("hidden");
});

btnClosePolicyModal.addEventListener("click", () => policyModal.classList.add("hidden"));
btnCancelPolicyModal.addEventListener("click", () => policyModal.classList.add("hidden"));

selectPolicyAction.addEventListener("change", onActionChange);

function onActionChange() {
  const val = selectPolicyAction.value;
  if (val === "new") {
    inputPolicySection.value = "";
    inputPolicyTitle.value = "";
    textareaPolicyContent.value = "";
    inputPolicySection.disabled = false;
  } else {
    const policy = currentPolicies.find(p => p.id === parseInt(val));
    if (policy) {
      inputPolicySection.value = policy.seccion;
      inputPolicyTitle.value = policy.titulo;
      textareaPolicyContent.value = policy.contenido;
      inputPolicySection.disabled = true; // No modificar nombre de sección en edición
    }
  }
}

function openEditPolicy(id) {
  selectPolicyAction.value = id.toString();
  onActionChange();
  policyModal.classList.remove("hidden");
}


// ==============================================================================
// 5. FLUJO DE CARGA Y AUTO-INDEXACIÓN: SUBIENDO E INDEXANDO
// ==============================================================================

btnSubmitPolicy.addEventListener("click", async () => {
  const action = selectPolicyAction.value;
  const section = inputPolicySection.value.trim();
  const title = inputPolicyTitle.value.trim();
  const content = textareaPolicyContent.value.trim();

  if (!section || !title || !content) {
    alert("Por favor completa todos los campos del formulario.");
    return;
  }

  // 1. Cerrar modal de edición y abrir modal de progreso
  policyModal.classList.add("hidden");
  startLoadingModal();

  try {
    // FASE 1: Guardar en Base de Datos (Backend puerto 5000)
    updateLoadingStep(1, 25, "1. Guardando cambio en Base de Datos SQLite...");
    
    let url = `${BACKEND_API_URL}/policies`;
    let method = "POST";
    let body = { seccion: section, titulo: title, contenido: content };

    if (action !== "new") {
      url = `${BACKEND_API_URL}/policies/${action}`;
      method = "PUT";
      body = { contenido: content, titulo: title };
    }

    // FASE 2: Backend notifica al agente
    setTimeout(() => {
      updateLoadingStep(2, 55, "2. Backend notificando al Agente RAG vía API...");
    }, 400);

    // FASE 3: Agente generando embeddings
    setTimeout(() => {
      updateLoadingStep(3, 80, "3. Agente regenerando embeddings BGE-M3 en ChromaDB...");
    }, 800);

    const res = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || `Error en Backend: ${res.status}`);
    }

    const result = await res.json();

    // FASE 4: Completado
    updateLoadingStep(4, 100, "4. ¡Base Vectorial ChromaDB lista en caliente!");
    showLoadingSuccess(result);

    // Recargar lista lateral de políticas
    await loadPolicies();

    // Notificar en el chat sobre la nueva información disponible
    appendSystemNotificationInChat(section, title);

  } catch (err) {
    showLoadingError(err.message);
  }
});

// Forzar auto-indexación manual
btnForceSync.addEventListener("click", async () => {
  startLoadingModal();
  updateLoadingStep(2, 50, "Solicitando al Agente re-indexar con la BD...");
  try {
    const res = await fetch(`${BACKEND_API_URL}/policies/sync`, { method: "POST" });
    if (!res.ok) throw new Error("Error en sincronización");
    const data = await res.json();
    updateLoadingStep(4, 100, "¡Sincronización completada!");
    showLoadingSuccess(data);
  } catch (e) {
    showLoadingError(e.message);
  }
});

function startLoadingModal() {
  loadingModal.classList.remove("hidden");
  loadingSpinner.classList.remove("hidden");
  successCheck.classList.add("hidden");
  loadingTitle.textContent = "Subiendo e Indexando...";
  loadingSubtitle.textContent = "Conectando con Backend empresarial y Agente RAG...";
  progressBar.style.width = "5%";
  progressBar.className = "bg-gradient-to-r from-cyan-500 via-blue-500 to-emerald-400 h-full transition-all duration-300 rounded-full";
  
  [step1, step2, step3, step4].forEach(s => {
    s.className = "text-slate-500 flex items-center space-x-2";
    s.children[0].textContent = "○";
  });
}

function updateLoadingStep(stepNum, percent, text) {
  progressBar.style.width = `${percent}%`;
  loadingPercentageText.textContent = `${percent}%`;
  loadingStepText.textContent = text;

  const steps = [step1, step2, step3, step4];
  for (let i = 0; i < stepNum; i++) {
    steps[i].className = "text-emerald-400 flex items-center space-x-2";
    steps[i].children[0].textContent = "✔";
  }
  if (stepNum <= 4) {
    steps[stepNum - 1].className = "text-cyan-400 font-bold flex items-center space-x-2 animate-pulse";
    steps[stepNum - 1].children[0].textContent = "⏳";
  }
}

function showLoadingSuccess(result) {
  loadingSpinner.classList.add("hidden");
  successCheck.classList.remove("hidden");
  loadingTitle.textContent = "¡Indexación Completada!";
  loadingSubtitle.textContent = "El Agente ya tiene acceso inmediato a la nueva información.";

  // Salir de la modal automáticamente tras 1.2 segundos como se solicitó
  setTimeout(() => {
    loadingModal.classList.add("hidden");
  }, 1300);
}

function showLoadingError(errMsg) {
  loadingSpinner.classList.add("hidden");
  loadingTitle.textContent = "Error en el proceso";
  loadingSubtitle.textContent = errMsg;
  progressBar.className = "bg-red-500 h-full w-full rounded-full";
  setTimeout(() => {
    loadingModal.classList.add("hidden");
    alert("Error: " + errMsg);
  }, 2000);
}

function appendSystemNotificationInChat(section, title) {
  const div = document.createElement("div");
  div.className = "p-3 bg-cyan-950/40 border border-cyan-800/60 rounded-xl text-xs text-cyan-300 text-center my-3 max-w-2xl mx-auto shadow-sm";
  div.innerHTML = `
    🎉 <strong>Base de Datos Actualizada:</strong> Se almacenó e indexó <em>"${escapeHtml(section)}"</em>.
    <br><span class="text-slate-400">El Agente RAG ya aprendió este contenido y puedes preguntarle sobre él.</span>
  `;
  chatContainer.appendChild(div);
  scrollToBottom();
}

btnRefreshPolicies.addEventListener("click", () => {
  btnRefreshPolicies.classList.add("animate-spin");
  checkHealth().finally(() => {
    setTimeout(() => btnRefreshPolicies.classList.remove("animate-spin"), 500);
  });
});

// ==============================================================================
// 5. LABORATORIO DE BENCHMARKING DE MODELOS
// ==============================================================================

if (btnOpenBenchmark) {
  btnOpenBenchmark.addEventListener("click", () => {
    if (benchmarkModal) benchmarkModal.classList.remove("hidden");
  });
}

if (btnCloseBenchmarkModal) {
  btnCloseBenchmarkModal.addEventListener("click", () => {
    if (benchmarkModal) benchmarkModal.classList.add("hidden");
  });
}

// Botones de preguntas sugeridas para el benchmark
document.querySelectorAll(".btn-bench-suggest").forEach(btn => {
  btn.addEventListener("click", () => {
    if (inputBenchQuestion) {
      const txt = btn.textContent.trim();
      if (txt.includes("Turno nocturno")) {
        inputBenchQuestion.value = "¿Cuál es la duración y horario del turno nocturno de soporte técnico?";
      } else if (txt.includes("contraseñas")) {
        inputBenchQuestion.value = "¿Cuál es la longitud mínima de las contraseñas maestras y cada cuánto expiran?";
      } else if (txt.includes("internet")) {
        inputBenchQuestion.value = "¿Cuál es el valor del subsidio mensual de conectividad e internet?";
      } else if (txt.includes("vacaciones")) {
        inputBenchQuestion.value = "¿Cuántos días de vacaciones anuales remuneradas corresponden y con cuánta antelación deben solicitarse?";
      } else {
        inputBenchQuestion.value = txt;
      }
    }
  });
});

if (btnRunBenchmark) {
  btnRunBenchmark.addEventListener("click", async () => {
    const modelA = selectBenchModelA.value;
    const modelB = selectBenchModelB.value;
    const question = inputBenchQuestion.value.trim();
    if (!question) return;

    benchNameA.textContent = modelA;
    benchNameB.textContent = modelB;
    benchTimeA.textContent = "⏱️ Evaluando...";
    benchTimeB.textContent = "⏱️ Evaluando...";
    benchBodyA.innerHTML = `<div class="p-4 text-center text-cyan-400 animate-pulse text-xs">⏳ Generando respuesta con ${escapeHtml(modelA)}...</div>`;
    benchBodyB.innerHTML = `<div class="p-4 text-center text-amber-400 animate-pulse text-xs">⏳ Generando respuesta con ${escapeHtml(modelB)}...</div>`;
    benchSummaryBanner.classList.add("hidden");
    btnRunBenchmark.disabled = true;
    btnRunBenchmark.classList.add("opacity-50");

    try {
      // Lanzar ambas consultas concurrentemente
      const callA = fetch(`${AGENT_API_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: question, session_id: "bench_session_a", modelo: modelA })
      }).then(r => r.json());

      const callB = fetch(`${AGENT_API_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta: question, session_id: "bench_session_b", modelo: modelB })
      }).then(r => r.json());

      const [resA, resB] = await Promise.all([callA, callB]);

      // Renderizar resultados del Modelo A
      const timeA = resA.tiempo_respuesta_segundos || 0;
      benchTimeA.textContent = `⏱️ ${timeA}s`;
      benchBodyA.innerHTML = marked.parse(resA.respuesta || "Sin respuesta");

      // Renderizar resultados del Modelo B
      const timeB = resB.tiempo_respuesta_segundos || 0;
      benchTimeB.textContent = `⏱️ ${timeB}s`;
      benchBodyB.innerHTML = marked.parse(resB.respuesta || "Sin respuesta");

      // Comparativa y cálculo de velocidad
      benchSummaryBanner.classList.remove("hidden");
      if (timeA <= timeB) {
        const ratio = (timeB / (timeA || 0.001)).toFixed(1);
        const diff = (timeB - timeA).toFixed(2);
        benchSummaryText.textContent = `⚡ ${modelA} fue ${ratio}x más rápido que ${modelB}`;
        benchSpeedDiffBadge.textContent = `Diferencia: ${diff}s a favor de Modelo A`;
      } else {
        const ratio = (timeA / (timeB || 0.001)).toFixed(1);
        const diff = (timeA - timeB).toFixed(2);
        benchSummaryText.textContent = `⚡ ${modelB} fue ${ratio}x más rápido que ${modelA}`;
        benchSpeedDiffBadge.textContent = `Diferencia: ${diff}s a favor de Modelo B`;
      }

    } catch (err) {
      alert("Error ejecutando el benchmark: " + err.message);
    } finally {
      btnRunBenchmark.disabled = false;
      btnRunBenchmark.classList.remove("opacity-50");
    }
  });
}

function escapeHtml(text) {
  if (!text) return "";
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Iniciar al cargar la ventana
window.addEventListener("DOMContentLoaded", checkHealth);
