/**
 * frontend/app.js - Controlador del Portal TransLogix Express & Agente Web Autónomo.
 * Conecta con el Agente RAG Local (puerto 8000), el TMS de rastreo y la base de datos empresarial.
 * Incluye el motor de Cursor Virtual Autónomo que opera los componentes de la página en vivo.
 */

const API_BASE_URL = (typeof window !== "undefined" && window.location.origin.startsWith("http"))
  ? window.location.origin
  : "http://localhost:8000";

const SESSION_ID = "tlx_session_" + Math.random().toString(36).substring(2, 9);
let currentPolicies = [];

// Elementos del Agente & Chat
const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const inputQuestion = document.getElementById("inputQuestion");
const btnSendMessage = document.getElementById("btnSendMessage");
const btnClearChat = document.getElementById("btnClearChat");
const selectModel = document.getElementById("selectModel");

// Elementos de Autenticación & Memoria del Usuario
let currentUser = null;
let currentAuthToken = localStorage.getItem("tlx_auth_token") || "";
let uncompletedQuoteTimer = null;
let lastTrackedQuotePayload = null;

// Elementos del Cursor Virtual del Agente
const agentVirtualCursor = document.getElementById("agentVirtualCursor");
const agentCursorLabel = document.getElementById("agentCursorLabel");
const cursorRipple = document.getElementById("cursorRipple");

// Indicadores de Estado
const agentStatusDot = document.getElementById("agentStatusDot");
const agentStatusText = document.getElementById("agentStatusText");
const backendStatusDot = document.getElementById("backendStatusDot");
const backendStatusText = document.getElementById("backendStatusText");

// Modales de Administración de BD
const policyModal = document.getElementById("policyModal");
const btnOpenPolicyModal = document.getElementById("btnOpenPolicyModal");
const btnClosePolicyModal = document.getElementById("btnClosePolicyModal");
const btnCancelPolicyModal = document.getElementById("btnCancelPolicyModal");
const btnSubmitPolicy = document.getElementById("btnSubmitPolicy");
const selectPolicyAction = document.getElementById("selectPolicyAction");
const inputPolicySection = document.getElementById("inputPolicySection");
const inputPolicyTitle = document.getElementById("inputPolicyTitle");
const textareaPolicyContent = document.getElementById("textareaPolicyContent");

// Variables de la Base de Datos Geográfica (Colombia & Internacional)
let cachedDepartamentos = [];
let cachedMunicipios = [];
let cachedPaises = [];


// ==============================================================================
// 1. INICIALIZACIÓN Y SALUD DE LOS SERVICIOS
// ==============================================================================

let activeTunnelUrl = "";

async function checkTunnelStatus() {
  const badgeContainer = document.getElementById("tunnelBadgeContainer");
  const badgeLink = document.getElementById("tunnelBadgeLink");
  try {
    const res = await fetch(`${API_BASE_URL}/api/tunnel-info`);
    if (res.ok) {
      const data = await res.json();
      if (data.is_active && data.tunnel_url) {
        activeTunnelUrl = data.tunnel_url;
        if (badgeLink) {
          badgeLink.href = data.tunnel_url;
          badgeLink.textContent = data.tunnel_url.replace("https://", "");
        }
        if (badgeContainer) badgeContainer.classList.remove("hidden");
      }
    }
  } catch (e) {
    console.warn("[Tunnel] Error verificando túnel:", e);
  }
}

function copyTunnelUrl() {
  if (!activeTunnelUrl) {
    activeTunnelUrl = window.location.origin;
  }
  navigator.clipboard.writeText(activeTunnelUrl).then(() => {
    const btn = document.getElementById("btnCopyTunnel");
    if (btn) {
      btn.innerHTML = `<span class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400">¡Copiado!</span>`;
      setTimeout(() => {
        btn.innerHTML = `<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>`;
      }, 1800);
    }
  }).catch(() => {
    prompt("Copia la URL del túnel:", activeTunnelUrl);
  });
}

async function checkHealth() {
  checkTunnelStatus();
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (res.ok) {
      const data = await res.json();
      if (agentStatusDot) agentStatusDot.className = "w-2 h-2 rounded-full bg-emerald-500";
      if (agentStatusText) agentStatusText.textContent = `En Línea (${data.modelo || "7B"})`;
    }
  } catch (e) {
    if (agentStatusDot) agentStatusDot.className = "w-2 h-2 rounded-full bg-red-500";
    if (agentStatusText) agentStatusText.textContent = "Sin conexión (puerto 8000)";
  }

  try {
    const res = await fetch(`${API_BASE_URL}/policies`);
    if (res.ok) {
      const data = await res.json();
      currentPolicies = data.politicas || [];
      if (backendStatusDot) backendStatusDot.className = "w-2 h-2 rounded-full bg-emerald-500";
      if (backendStatusText) backendStatusText.textContent = `En Línea (${currentPolicies.length} módulos)`;
      updatePolicyModalOptions();
    }
  } catch (e) {
    if (backendStatusDot) backendStatusDot.className = "w-2 h-2 rounded-full bg-amber-500";
    if (backendStatusText) backendStatusText.textContent = "BD no inicializada";
  }
}

function updatePolicyModalOptions() {
  if (!selectPolicyAction) return;
  selectPolicyAction.innerHTML = `
    <option value="new">➕ Crear Nueva Política en Base de Datos</option>
    <optgroup label="Editar Políticas Existentes de TransLogix">
      ${currentPolicies.map(p => `
        <option value="${p.id}">#${p.id} - ${escapeHtml(p.seccion)}</option>
      `).join("")}
    </optgroup>
  `;
}


// ==============================================================================
// 2. CHAT CON EL AGENTE TRANSLOGIX & DISPARADOR DE ACCIONES
// ==============================================================================

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = inputQuestion.value.trim();
  if (!question) return;

  const chosenModel = selectModel ? selectModel.value : null;

  // 1. Añadir mensaje del usuario en el chat
  appendUserMessage(question);
  inputQuestion.value = "";
  inputQuestion.focus();

  // 2. Añadir burbuja de pensamiento del agente
  const loadingBubbleId = appendAgentLoadingMessage(chosenModel);

  try {
    const headers = { "Content-Type": "application/json" };
    if (currentAuthToken) {
      headers["Authorization"] = `Bearer ${currentAuthToken}`;
    }

    const payload = {
      pregunta: question,
      session_id: SESSION_ID,
      modelo: chosenModel,
    };
    if (currentUser && currentUser.uid) {
      payload.uid = currentUser.uid;
      payload.token = currentAuthToken;
    }

    const res = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      throw new Error(`Error en servidor del Agente: ${res.status}`);
    }

    const data = await res.json();
    replaceLoadingWithResponse(loadingBubbleId, data);

    // 3. DETECTAR Y EJECUTAR ACCIÓN AUTÓNOMA DEL AGENTE EN LA PÁGINA
    const action = data.action || (data.data && data.data.action);
    if (action) {
      console.log("[TransLogix Agent] Acción detectada:", action);
      executeAgentAutonomousAction(action);
    }

  } catch (error) {
    replaceLoadingWithError(loadingBubbleId, error.message);
  }
});

function appendUserMessage(text) {
  const div = document.createElement("div");
  div.className = "flex items-start justify-end gap-3 max-w-[85%] ml-auto";
  div.innerHTML = `
    <div class="bg-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-900 rounded-2xl rounded-tr-sm px-4 py-3 text-[13px] shadow-xs border border-zinc-800 dark:border-zinc-200 leading-relaxed">
      <p class="whitespace-pre-wrap font-normal">${escapeHtml(text)}</p>
    </div>
    <div class="w-8 h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 flex items-center justify-center shrink-0 text-zinc-700 dark:text-zinc-300 text-xs font-semibold shadow-xs mt-0.5">
      Tú
    </div>
  `;
  chatContainer.appendChild(div);
  scrollToBottom();
}

function appendAgentLoadingMessage(modelLabel) {
  const id = "loading_" + Date.now();
  const div = document.createElement("div");
  div.id = id;
  div.className = "flex items-start gap-3 max-w-full";
  const label = modelLabel || (selectModel ? selectModel.value : "7B");
  div.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-zinc-950 text-white dark:bg-zinc-100 dark:text-zinc-950 flex items-center justify-center shrink-0 text-xs font-bold shadow-xs mt-0.5">
      R
    </div>
    <div class="flex-1 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl rounded-tl-sm p-4 shadow-xs text-xs text-zinc-600 dark:text-zinc-400 flex items-center space-x-3">
      <svg class="w-4 h-4 text-zinc-900 dark:text-zinc-100 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span>Consultando base TransLogix con <strong>${escapeHtml(label)}</strong>...</span>
    </div>
  `;
  chatContainer.appendChild(div);
  scrollToBottom();
  return id;
}

function replaceLoadingWithResponse(bubbleId, data) {
  const loadingElem = document.getElementById(bubbleId);
  if (!loadingElem) return;

  const msgText = (data.data && data.data.mensaje) ? data.data.mensaje : (data.respuesta || "");
  const htmlResponse = marked.parse(msgText);
  const timeFormatted = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const sec = (data.metadata && data.metadata.tiempo_respuesta_segundos) ? data.metadata.tiempo_respuesta_segundos : (data.tiempo_respuesta_segundos || 0);

  // Insignia de Acción si el agente operó la página
  let actionBadge = "";
  const act = data.action || (data.data && data.data.action);
  if (act) {
    let actName = "Intervención en Portal";
    if (act.type === "quote" || act.type === "COTIZAR") actName = "Cotización Autocompletada";
    else if (act.type === "track" || act.type === "RASTREAR") actName = "Rastreo TMS Ejecutado";
    else if (act.type === "dangerous_goods" || act.type === "VERIFICAR_MERCANCIA") actName = "Verificación Mercancía Peligrosa";
    else if (act.type === "pqrs" || act.type === "PQRS") actName = "Formulario PQRS Preparado";
    else if (act.type === "coverage" || act.type === "CONSULTAR_COBERTURA") actName = "Consulta de Cobertura Troncal";

    actionBadge = `
      <div class="mt-3.5 mb-2 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-800/70 border border-zinc-200 dark:border-zinc-700 text-xs flex items-center justify-between font-mono">
        <span class="flex items-center gap-1.5 text-zinc-800 dark:text-zinc-200 font-semibold">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> ⚡ Acción del Agente: ${actName}
        </span>
        <span class="text-zinc-400 text-[11px]">En pantalla ↗</span>
      </div>
    `;
  }

  // Acordeón de fuentes
  let fuentesHtml = "";
  const fuentesList = (data.data && data.data.fuentes) ? data.data.fuentes : (data.fuentes || []);
  if (fuentesList && fuentesList.length > 0) {
    const listHtml = fuentesList.map(f => `
      <div class="bg-zinc-50 dark:bg-zinc-950 p-3 rounded-lg border border-zinc-200 dark:border-zinc-800 mb-2 last:mb-0 text-xs">
        <div class="flex items-center justify-between font-mono mb-1">
          <span class="font-bold text-zinc-900 dark:text-zinc-100">📄 ${escapeHtml(f.archivo || "Doc")}</span>
          <span class="text-zinc-500 text-[10px]">Score: ${f.score ? f.score.toFixed(3) : "OK"}</span>
        </div>
        ${f.seccion ? `<div class="text-[11px] font-medium text-zinc-600 dark:text-zinc-400 mb-1">${escapeHtml(f.seccion)}</div>` : ''}
        <p class="text-zinc-600 dark:text-zinc-400 font-mono text-[11px] line-clamp-3 leading-relaxed">${escapeHtml(f.fragmento || "")}</p>
      </div>
    `).join("");

    fuentesHtml = `
      <div class="mt-3.5 pt-3 border-t border-zinc-100 dark:border-zinc-800">
        <details class="group cursor-pointer">
          <summary class="text-xs font-semibold text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 transition flex items-center space-x-1.5 select-none">
            <svg class="w-3.5 h-3.5 transition-transform group-open:rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            <span>Fuentes Documentales Consultadas (${fuentesList.length})</span>
          </summary>
          <div class="mt-2.5 space-y-1.5">
            ${listHtml}
          </div>
        </details>
      </div>
    `;
  }

  loadingElem.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-zinc-950 text-white dark:bg-zinc-100 dark:text-zinc-950 flex items-center justify-center shrink-0 text-xs font-bold shadow-xs mt-0.5">
      R
    </div>
    <div class="flex-1 bg-white dark:bg-zinc-900 border border-zinc-200/90 dark:border-zinc-800 rounded-2xl rounded-tl-sm p-4 sm:p-5 shadow-xs text-zinc-900 dark:text-zinc-100 max-w-full">
      <div class="flex items-center justify-between pb-2.5 mb-3.5 border-b border-zinc-100 dark:border-zinc-800 text-[11px] font-mono text-zinc-500">
        <div class="flex items-center space-x-2">
          <span class="text-zinc-800 dark:text-zinc-200 font-semibold">${escapeHtml(data.modelo || "qwen2.5:7b-instruct")}</span>
          <span class="inline-flex items-center rounded-full bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 text-[10px] font-medium text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1 animate-pulse"></span> En Línea
          </span>
        </div>
        <span class="text-zinc-400 font-mono">⏱️ ${sec}s</span>
      </div>

      <div class="chat-markdown text-[13px] leading-relaxed text-zinc-700 dark:text-zinc-300">
        ${htmlResponse}
      </div>

      ${actionBadge}
      ${fuentesHtml}

      <div class="mt-3.5 pt-2 border-t border-zinc-100 dark:border-zinc-800 text-[10px] text-zinc-400 flex justify-between font-mono">
        <span>TransLogix AI</span>
        <span>${timeFormatted}</span>
      </div>
    </div>
  `;
  scrollToBottom();
}

function replaceLoadingWithError(bubbleId, errMsg) {
  const loadingElem = document.getElementById(bubbleId);
  if (!loadingElem) return;
  loadingElem.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-red-600 text-white flex items-center justify-center shrink-0 font-bold text-xs shadow-xs mt-0.5">!</div>
    <div class="flex-1 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 rounded-2xl rounded-tl-sm p-4 text-xs text-red-800 dark:text-red-300">
      <p class="font-bold text-sm">Error en consulta</p>
      <p class="text-xs mt-1 leading-relaxed">${escapeHtml(errMsg)}</p>
    </div>
  `;
  scrollToBottom();
}

function scrollToBottom() {
  if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
}

if (btnClearChat) {
  btnClearChat.addEventListener("click", () => {
    chatContainer.innerHTML = `
      <div class="text-center text-xs text-zinc-400 dark:text-zinc-500 py-6">
        Conversación reiniciada. Puedes formular una nueva consulta o pedirle al agente que actúe en la página.
      </div>
    `;
  });
}


// ==============================================================================
// 3. MOTOR DEL CURSOR VIRTUAL AUTÓNOMO ("EL AGENTE TOMA EL MANDO")
// ==============================================================================

async function executeAgentAutonomousAction(action) {
  if (!agentVirtualCursor) return;

  const type = action.type;
  const data = action.data || {};

  // 1. Despertar el cursor virtual
  agentVirtualCursor.classList.remove("opacity-0");
  agentVirtualCursor.classList.add("opacity-100");
  if (agentCursorLabel) agentCursorLabel.textContent = "🤖 Agente TransLogix Operando...";

  try {
    if (type === "quote") {
      await runAgentQuoteAction(data);
    } else if (type === "track") {
      await runAgentTrackAction(data);
    } else if (type === "dangerous_goods") {
      await runAgentDangerousGoodsAction(data);
    } else if (type === "pqrs") {
      await runAgentPqrsAction(data);
    } else if (type === "coverage") {
      await runAgentCoverageAction(data);
    }
  } catch (err) {
    console.warn("Fallo en animación del cursor:", err);
  } finally {
    setTimeout(() => {
      agentVirtualCursor.classList.remove("opacity-100");
      agentVirtualCursor.classList.add("opacity-0");
    }, 1800);
  }
}

// Acción: Autocompletar y calcular cotización
async function runAgentQuoteAction(data) {
  const widget = document.getElementById("widgetCotizador");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 3000);
  }

  // Normalizar datos en español o inglés
  const origenVal = data.origen || data.origin || "Bogotá";
  const destinoVal = data.destino || data.destination || "Medellín";
  const altoVal = data.alto || (data.dimensions && data.dimensions.height) || 30;
  const anchoVal = data.ancho || (data.dimensions && data.dimensions.width) || 30;
  const largoVal = data.largo || (data.dimensions && data.dimensions.length) || 30;
  const pesoVal = data.peso || data.weight || data.peso_real || 10;
  const valorVal = data.valor || data.declared_value || data.valor_declarado || 150000;

  // Mover cursor a Origen
  const origenElem = document.getElementById("cotizOrigen");
  if (origenElem) {
    await moveCursorToElement(origenElem, "Configurando origen...");
    // Buscar si coincide parcialmente con las opciones
    for (const opt of origenElem.options) {
      if (opt.value.toLowerCase().includes(origenVal.toLowerCase()) || origenVal.toLowerCase().includes(opt.value.toLowerCase())) {
        origenElem.value = opt.value;
        break;
      }
    }
    await triggerInputFeedback(origenElem);
  }

  // Mover cursor a Destino
  const destinoElem = document.getElementById("cotizDestino");
  if (destinoElem) {
    await moveCursorToElement(destinoElem, "Configurando destino...");
    for (const opt of destinoElem.options) {
      if (opt.value.toLowerCase().includes(destinoVal.toLowerCase()) || destinoVal.toLowerCase().includes(opt.value.toLowerCase())) {
        destinoElem.value = opt.value;
        break;
      }
    }
    await triggerInputFeedback(destinoElem);
  }

  // Mover a dimensiones
  const altoElem = document.getElementById("cotizAlto");
  if (altoElem) {
    await moveCursorToElement(altoElem, "Ingresando medidas...");
    altoElem.value = altoVal;
    await triggerInputFeedback(altoElem);
  }
  const anchoElem = document.getElementById("cotizAncho");
  if (anchoElem) anchoElem.value = anchoVal;
  const largoElem = document.getElementById("cotizLargo");
  if (largoElem) largoElem.value = largoVal;

  // Mover a peso real
  const pesoElem = document.getElementById("cotizPeso");
  if (pesoElem) {
    await moveCursorToElement(pesoElem, "Ingresando peso real...");
    pesoElem.value = pesoVal;
    await triggerInputFeedback(pesoElem);
  }

  // Mover a valor declarado
  const valorElem = document.getElementById("cotizValor");
  if (valorElem) {
    valorElem.value = valorVal;
  }

  // Mover al botón de calcular y hacer clic
  const btnCalc = document.getElementById("btnEjecutarCotizacion");
  if (btnCalc) {
    await moveCursorToElement(btnCalc, "Calculando cotización oficial...");
    await simulateCursorClick(btnCalc);
    handleManualCotizacion(new Event("submit"));
    if (agentCursorLabel) agentCursorLabel.textContent = "✔ ¡Cotización completada!";
  }
}

// Acción: Autocompletar y consultar guía en el TMS
async function runAgentTrackAction(data) {
  const widget = document.getElementById("widgetRastreo");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 3000);
  }

  const guiaVal = data.guia || data.tracking_number || data.guide || "TLX-84920194-CO";
  const inputGuia = document.getElementById("inputGuia");
  if (inputGuia) {
    await moveCursorToElement(inputGuia, "Ingresando guía en TMS...");
    inputGuia.value = guiaVal;
    await triggerInputFeedback(inputGuia);
  }

  const btnTrack = document.getElementById("btnEjecutarRastreo");
  if (btnTrack) {
    await moveCursorToElement(btnTrack, "Consultando estado TMS...");
    await simulateCursorClick(btnTrack);
    handleManualRastreo(new Event("submit"));
    if (agentCursorLabel) agentCursorLabel.textContent = "✔ ¡Rastreo obtenido del TMS!";
  }
}

// Acción: Navegar y enfocar mercancías peligrosas
async function runAgentDangerousGoodsAction(data) {
  const widget = document.getElementById("widgetMercancias");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    await moveCursorToElement(widget, "Verificando normativa ONU...");
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 2500);
    if (agentCursorLabel) agentCursorLabel.textContent = "✔ Requisitos ONU verificados";
  }
}

// Acción: Preparar formulario de PQRS
async function runAgentPqrsAction(data) {
  const widget = document.getElementById("widgetPqrs");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 2500);
  }

  const tipoElem = document.getElementById("pqrsTipo");
  if (tipoElem && data.tipo) tipoElem.value = data.tipo;

  const motivoElem = document.getElementById("pqrsMotivo");
  if (motivoElem && data.motivo) {
    await moveCursorToElement(motivoElem, "Diligenciando hechos...");
    motivoElem.value = data.motivo;
    await triggerInputFeedback(motivoElem);
  }

  if (agentCursorLabel) agentCursorLabel.textContent = "✔ Formulario PQRS preparado";
}

// Acción: Cobertura
async function runAgentCoverageAction(data) {
  const widget = document.getElementById("widgetCobertura");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    await moveCursorToElement(widget, "Consultando red troncal...");
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 2500);
  }
}

// Utilidades de animación del Cursor
function moveCursorToElement(element, labelText) {
  return new Promise((resolve) => {
    if (!agentVirtualCursor || !element) {
      resolve();
      return;
    }

    if (labelText && agentCursorLabel) {
      agentCursorLabel.textContent = labelText;
    }

    const rect = element.getBoundingClientRect();
    const targetX = rect.left + rect.width / 2;
    const targetY = rect.top + rect.height / 2;

    agentVirtualCursor.style.transform = `translate3d(${targetX}px, ${targetY}px, 0)`;
    setTimeout(resolve, 600);
  });
}

function simulateCursorClick(element) {
  return new Promise((resolve) => {
    if (cursorRipple) {
      cursorRipple.classList.remove("hidden");
      cursorRipple.classList.add("click-ripple");
      setTimeout(() => {
        cursorRipple.classList.add("hidden");
        cursorRipple.classList.remove("click-ripple");
      }, 500);
    }
    if (element) {
      element.classList.add("scale-95");
      setTimeout(() => element.classList.remove("scale-95"), 150);
    }
    setTimeout(resolve, 350);
  });
}

function triggerInputFeedback(element) {
  return new Promise((resolve) => {
    if (!element) { resolve(); return; }
    element.classList.add("ring-2", "ring-zinc-950", "dark:ring-zinc-100");
    setTimeout(() => {
      element.classList.remove("ring-2", "ring-zinc-950", "dark:ring-zinc-100");
      resolve();
    }, 300);
  });
}


// ==============================================================================
// 4. CONTROLADORES DE LOS FORMULARIOS DEL PORTAL
// ==============================================================================

async function handleManualCotizacion(e) {
  if (e && e.preventDefault) e.preventDefault();

  clearTimeout(uncompletedQuoteTimer);

  const origen = document.getElementById("cotizOrigen").value;
  const destino = document.getElementById("cotizDestino").value;
  const alto = parseFloat(document.getElementById("cotizAlto").value) || 30;
  const ancho = parseFloat(document.getElementById("cotizAncho").value) || 30;
  const largo = parseFloat(document.getElementById("cotizLargo").value) || 30;
  const peso = parseFloat(document.getElementById("cotizPeso").value) || 10;
  const valor = parseFloat(document.getElementById("cotizValor").value) || 150000;
  const tipo = document.getElementById("cotizTipo").value || "General";

  const resBox = document.getElementById("resCotizacion");
  const btn = document.getElementById("btnEjecutarCotizacion");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/cotizar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origen, destino, alto, ancho, largo,
        peso_real: peso,
        valor_declarado: valor,
        tipo_mercancia: tipo
      })
    });

    const data = await res.json();
    if (resBox) {
      resBox.classList.remove("hidden");
      document.getElementById("lblPesoReal").textContent = `${data.peso_real_kg} kg`;
      document.getElementById("lblPesoVol").textContent = `${data.peso_volumetrico_kg} kg`;
      document.getElementById("lblPesoFact").textContent = `${data.peso_facturable_kg} kg`;
      document.getElementById("lblSeguro").textContent = `$${data.desglose.seguro_cop.toLocaleString()} COP`;
      document.getElementById("lblTotalEstimado").textContent = `$${data.total_estimado_cop.toLocaleString()} COP`;
      document.getElementById("lblTiempoEstimado").textContent = data.tiempo_entrega_estimado;
      document.getElementById("badgeTarifaTipo").textContent = `Flete: ${data.tarifa_aplicada_tipo}`;
    }

    // Registrar evento de cotización completada si el usuario está autenticado
    if (currentAuthToken) {
      fetch(`${API_BASE_URL}/api/v1/user/event`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${currentAuthToken}`
        },
        body: JSON.stringify({
          tipo_evento: "COTIZACION_COMPLETADA",
          descripcion: `Cotización oficial calculada: de ${origen} a ${destino}, ${peso}kg (${largo}x${ancho}x${alto}cm), total $${data.total_estimado_cop.toLocaleString()} COP`,
          metadatos: { origen, destino, peso, largo, ancho, alto, valor, tipo, total: data.total_estimado_cop }
        })
      }).catch(err => console.warn(err));
    }

  } catch (err) {
    alert("Error calculando cotización: " + err.message);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function handleManualRastreo(e) {
  if (e && e.preventDefault) e.preventDefault();

  const guia = document.getElementById("inputGuia").value.trim();
  if (!guia) return;

  const resBox = document.getElementById("resRastreo");
  const btn = document.getElementById("btnEjecutarRastreo");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/tracking/${encodeURIComponent(guia)}`);
    const data = await res.json();

    if (resBox && data.ultimo_evento) {
      resBox.classList.remove("hidden");
      document.getElementById("lblRastreoGuia").textContent = data.guia;
      document.getElementById("badgeRastreoEstado").textContent = `● ${data.ultimo_evento.codigo}`;
      document.getElementById("lblUltimoEventoDesc").textContent = data.ultimo_evento.descripcion;
      document.getElementById("lblUbicacionEvento").textContent = `Ubicación: ${data.ultimo_evento.ubicación}`;
      document.getElementById("lblFechaEvento").textContent = `Fecha: ${data.ultimo_evento.fecha_hora}`;

      // Renderizar Timeline de eventos
      const timelineSteps = document.getElementById("timelineSteps");
      if (timelineSteps && data.timeline) {
        timelineSteps.innerHTML = data.timeline.map(item => `
          <div class="flex items-center space-x-2 text-[11px] font-mono">
            <span class="${item.completado ? 'text-emerald-500 font-bold' : 'text-zinc-400'}">${item.completado ? '✔' : '○'}</span>
            <span class="${item.completado ? 'text-zinc-800 dark:text-zinc-200 font-medium' : 'text-zinc-500'}">${escapeHtml(item.evento)}:</span>
            <span class="text-zinc-500 truncate">${escapeHtml(item.descripcion)}</span>
          </div>
        `).join("");
      }

      // Registrar evento de rastreo si está logueado
      if (currentAuthToken) {
        fetch(`${API_BASE_URL}/api/v1/user/event`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${currentAuthToken}`
          },
          body: JSON.stringify({
            tipo_evento: "CONSULTA_RASTREO",
            descripcion: `Consulta de rastreo de la guía ${guia}: estado ${data.ultimo_evento.codigo}`,
            metadatos: { guia, estado: data.ultimo_evento.codigo }
          })
        }).catch(err => console.warn(err));
      }
    }
  } catch (err) {
    alert("Error consultando TMS: " + err.message);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function handleManualPqrs(e) {
  if (e && e.preventDefault) e.preventDefault();

  const nombre = document.getElementById("pqrsNombre").value;
  const correo = document.getElementById("pqrsCorreo").value;
  const tipo = document.getElementById("pqrsTipo").value;
  const guia = document.getElementById("pqrsGuia").value;
  const valor = parseFloat(document.getElementById("pqrsValor").value) || 0;
  const motivo = document.getElementById("pqrsMotivo").value;

  const resBox = document.getElementById("resPqrs");
  const btn = document.getElementById("btnEjecutarPqrs");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/pqrs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre, correo, tipo, guia,
        valor_reclamado: valor,
        motivo
      })
    });

    const data = await res.json();
    if (resBox) {
      resBox.classList.remove("hidden");
      document.getElementById("lblPqrsRadicado").textContent = data.radicado;
      document.getElementById("lblPqrsMensaje").textContent = data.mensaje;

      const boxEscala = document.getElementById("boxPqrsEscalamiento");
      if (data.requiere_escalamiento_humano) {
        boxEscala.classList.remove("hidden");
        document.getElementById("lblPqrsMotivoEscalamiento").textContent = data.motivo_escalamiento;
      } else {
        boxEscala.classList.add("hidden");
      }

      // Registrar evento de PQRS si está logueado
      if (currentAuthToken) {
        fetch(`${API_BASE_URL}/api/v1/user/event`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${currentAuthToken}`
          },
          body: JSON.stringify({
            tipo_evento: "RADICACION_PQRS",
            descripcion: `Radicación de ${tipo} radicado ${data.radicado}: ${motivo.substring(0, 80)}`,
            metadatos: { radicado: data.radicado, tipo, guia, valor }
          })
        }).catch(err => console.warn(err));
      }
    }
  } catch (err) {
    alert("Error radicando PQRS: " + err.message);
  } finally {
    if (btn) btn.disabled = false;
  }
}


// ==============================================================================
// 5. HELPER ACTIONS PARA EL USUARIO
// ==============================================================================

function askAgentPrompt(text) {
  if (inputQuestion) {
    inputQuestion.value = text;
    chatForm.dispatchEvent(new Event("submit"));
  }
}

function askAgentToDemoAction(actionType) {
  if (actionType === "cotizar") {
    askAgentPrompt("Cotízame un envío de Bogotá a Medellín de 10 kilos y medidas 30x30x30 con valor de 200.000 COP");
  } else if (actionType === "rastrear") {
    askAgentPrompt("Rastrea la guía TLX-84920194-CO en el TMS y explícame su estado");
  }
}

function promptAgentForCurrentWidget(widgetName) {
  if (widgetName === "cotizador") {
    askAgentPrompt("Por favor cotiza un paquete de Bogotá a Cali de 5kg medidas 20x20x20 con valor de 100.000 pesos");
  } else if (widgetName === "rastreo") {
    askAgentPrompt("Rastrea la guía TLX-84920194-CO");
  }
}

function setGuiaQuick(guia) {
  const inputGuia = document.getElementById("inputGuia");
  if (inputGuia) {
    inputGuia.value = guia;
    handleManualRastreo(new Event("submit"));
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
}


// ==============================================================================
// 6. MODAL DE ALIMENTAR BASE DE DATOS SQLITE (BACKEND EN CALIENTE)
// ==============================================================================

if (btnOpenPolicyModal) {
  btnOpenPolicyModal.addEventListener("click", () => {
    selectPolicyAction.value = "new";
    onActionChange();
    policyModal.classList.remove("hidden");
  });
}

if (btnClosePolicyModal) btnClosePolicyModal.addEventListener("click", () => policyModal.classList.add("hidden"));
if (btnCancelPolicyModal) btnCancelPolicyModal.addEventListener("click", () => policyModal.classList.add("hidden"));
if (selectPolicyAction) selectPolicyAction.addEventListener("change", onActionChange);

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
      inputPolicySection.disabled = true;
    }
  }
}

if (btnSubmitPolicy) {
  btnSubmitPolicy.addEventListener("click", async () => {
    const action = selectPolicyAction.value;
    const section = inputPolicySection.value.trim();
    const title = inputPolicyTitle.value.trim();
    const content = textareaPolicyContent.value.trim();

    if (!section || !title || !content) {
      alert("Por favor completa todos los campos.");
      return;
    }

    try {
      let url = `${API_BASE_URL}/policies`;
      let method = "POST";
      let body = { seccion: section, titulo: title, contenido: content };

      if (action !== "new") {
        url = `${API_BASE_URL}/policies/${action}`;
        method = "PUT";
        body = { contenido: content, titulo: title };
      }

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!res.ok) throw new Error("Error en servidor");
      policyModal.classList.add("hidden");
      alert("¡Base de Datos actualizada y Agente auto-indexado en caliente!");
      await checkHealth();
    } catch (err) {
      alert("Error: " + err.message);
    }
  });
}

// ==============================================================================
// 7. BASE DE DATOS GEOGRÁFICA (32 DEPARTAMENTOS, MUNICIPIOS Y PAÍSES)
// ==============================================================================

async function loadGeoDatabase() {
  try {
    const [depRes, munRes, paisRes] = await Promise.all([
      fetch(`${API_BASE_URL}/api/v1/departamentos`),
      fetch(`${API_BASE_URL}/api/v1/municipios?limit=300`),
      fetch(`${API_BASE_URL}/api/v1/paises`)
    ]);

    if (depRes.ok) {
      const depData = await depRes.json();
      cachedDepartamentos = depData.departamentos || [];
      populateDepartamentosDropdown();
    }

    if (munRes.ok) {
      const munData = await munRes.json();
      cachedMunicipios = munData.municipios || [];
    }

    if (paisRes.ok) {
      const paisData = await paisRes.json();
      cachedPaises = paisData.paises || [];
    }

    populateCotizadorSelects();
    renderGeoResults(cachedMunicipios);
  } catch (err) {
    console.warn("[GeoDB] Error cargando base de datos geográfica:", err);
  }
}

function populateDepartamentosDropdown() {
  const select = document.getElementById("selectGeoDepartamento");
  if (!select) return;
  select.innerHTML = `<option value="">Todos los Departamentos (32 + D.C.)</option>` +
    cachedDepartamentos.map(d => `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`).join("");
}

function populateCotizadorSelects() {
  const selOrigen = document.getElementById("cotizOrigen");
  const selDestino = document.getElementById("cotizDestino");
  if (!selOrigen || !selDestino) return;

  const troncales = [
    "Bogotá D.C. (Hub Fontibón)",
    "Medellín (Hub Rionegro)",
    "Cali (Hub Yumbo)",
    "Barranquilla (Hub Malambo)",
    "Bucaramanga",
    "Cartagena",
    "Pereira",
    "Manizales"
  ];

  const htmlTroncales = troncales.map(t => `<option value="${t}">${t}</option>`).join("");
  const htmlMunicipios = cachedMunicipios.map(m => 
    `<option value="${m.municipio} (${m.departamento})">${m.municipio} - ${m.departamento}</option>`
  ).join("");
  const htmlPaises = cachedPaises.map(p => 
    `<option value="${p.pais} (Courier Internacional)">✈️ ${p.pais} [${p.codigo_iso}]</option>`
  ).join("");

  const fullHtml = `
    <optgroup label="Ciudades Troncales Principales">
      ${htmlTroncales}
    </optgroup>
    <optgroup label="Municipios y Cabeceras de Colombia (32 Departamentos)">
      ${htmlMunicipios}
    </optgroup>
    <optgroup label="Destinos Internacionales (Courier Express)">
      ${htmlPaises}
    </optgroup>
  `;

  selOrigen.innerHTML = fullHtml;
  selDestino.innerHTML = fullHtml;

  // Defaults
  selOrigen.selectedIndex = 0;
  selDestino.selectedIndex = 1;
}

function filterGeoDirectorio() {
  const inputSearch = document.getElementById("inputGeoSearch");
  const selectDep = document.getElementById("selectGeoDepartamento");
  const q = (inputSearch ? inputSearch.value.trim().toLowerCase() : "");
  const selectedDep = (selectDep ? selectDep.value.trim().toLowerCase() : "");

  let filteredMun = cachedMunicipios;
  if (selectedDep) {
    filteredMun = filteredMun.filter(m => m.departamento.toLowerCase() === selectedDep);
  }
  if (q) {
    filteredMun = filteredMun.filter(m => 
      m.municipio.toLowerCase().includes(q) ||
      m.departamento.toLowerCase().includes(q) ||
      (m.codigo_dane && m.codigo_dane.includes(q))
    );
  }

  // Filtrar también países internacionales si no se especificó un departamento
  let filteredPaises = [];
  if (!selectedDep && q) {
    filteredPaises = cachedPaises.filter(p => 
      p.pais.toLowerCase().includes(q) ||
      p.codigo_iso.toLowerCase().includes(q) ||
      p.continente.toLowerCase().includes(q)
    );
  }

  renderGeoResults(filteredMun, filteredPaises);
}

function renderGeoResults(municipios, paises = []) {
  const container = document.getElementById("geoResultsContainer");
  const lblResultados = document.getElementById("lblGeoResultados");
  if (!container) return;

  const total = municipios.length + paises.length;
  if (lblResultados) {
    lblResultados.textContent = `Mostrando ${total} registros de la base geográfica descargada:`;
  }

  if (total === 0) {
    container.innerHTML = `
      <div class="p-3 text-center text-xs text-zinc-400 bg-zinc-50 dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800">
        No se encontraron registros en la base de datos descargada para ese criterio.
      </div>
    `;
    return;
  }

  const munCards = municipios.map(m => `
    <div class="p-2.5 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 flex items-center justify-between hover:border-zinc-300 dark:hover:border-zinc-700 transition">
      <div>
        <div class="flex items-center space-x-2">
          <strong class="font-semibold text-zinc-900 dark:text-zinc-100 text-xs">${escapeHtml(m.municipio)}</strong>
          <span class="text-[10px] text-zinc-500 font-mono">DANE ${escapeHtml(m.codigo_dane)}</span>
          <span class="text-[10px] bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 px-1.5 py-0.5 rounded">${escapeHtml(m.departamento)}</span>
        </div>
        <div class="text-[11px] text-zinc-500 flex items-center space-x-2 mt-0.5">
          <span>Hub: ${escapeHtml(m.hub_asignado)}</span>
          <span>•</span>
          <span class="text-emerald-600 dark:text-emerald-400 font-medium">${escapeHtml(m.tiempo_entrega_std)}</span>
          <span>•</span>
          <span>${m.servicio_refrigerado ? '❄️ Termo' : 'Sin frío'}</span>
        </div>
      </div>
      <button type="button" onclick="selectGeoForCotizar('${escapeHtml(m.municipio)}')" class="shrink-0 text-[11px] font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-950 dark:hover:text-zinc-100 px-2 py-1 rounded bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 transition">
        Cotizar ↗
      </button>
    </div>
  `).join("");

  const paisCards = paises.map(p => `
    <div class="p-2.5 rounded-lg border border-indigo-200 dark:border-indigo-900/60 bg-indigo-50/30 dark:bg-indigo-950/20 flex items-center justify-between">
      <div>
        <div class="flex items-center space-x-2">
          <strong class="font-semibold text-indigo-950 dark:text-indigo-200 text-xs">✈️ ${escapeHtml(p.pais)}</strong>
          <span class="text-[10px] bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 px-1.5 py-0.5 rounded font-mono">${escapeHtml(p.codigo_iso)}</span>
          <span class="text-[10px] text-indigo-600 dark:text-indigo-400">${escapeHtml(p.continente)}</span>
        </div>
        <div class="text-[11px] text-zinc-500 flex items-center space-x-2 mt-0.5">
          <span>Tiempo: ${escapeHtml(p.tiempo_entrega)}</span>
          <span>•</span>
          <span>Salida: ${escapeHtml(p.hub_salida)}</span>
        </div>
      </div>
      <button type="button" onclick="askAgentPrompt('¿Cuáles son los requisitos de aduana y tarifas para enviar un paquete a ${escapeHtml(p.pais)}?')" class="shrink-0 text-[11px] font-medium text-indigo-700 dark:text-indigo-300 hover:text-indigo-950 px-2 py-1 rounded bg-indigo-100/70 dark:bg-indigo-900/40 border border-indigo-300 dark:border-indigo-800 transition">
        Consultar IA ↗
      </button>
    </div>
  `).join("");

  container.innerHTML = paisCards + munCards;
}

function selectGeoForCotizar(municipio) {
  const selDestino = document.getElementById("cotizDestino");
  if (selDestino) {
    for (const opt of selDestino.options) {
      if (opt.value.toLowerCase().includes(municipio.toLowerCase())) {
        selDestino.value = opt.value;
        break;
      }
    }
  }
  const widget = document.getElementById("widgetCotizador");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 1500);
  }
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

// ==============================================================================
// 8. AUTENTICACIÓN SEGURA Y GESTIÓN DE MEMORIA COMPORTAMENTAL (UID)
// ==============================================================================

function openAuthModal() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.remove("hidden");
  const errLogin = document.getElementById("loginErrorMsg");
  const errReg = document.getElementById("regErrorMsg");
  if (errLogin) errLogin.classList.add("hidden");
  if (errReg) errReg.classList.add("hidden");
}

function closeAuthModal() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.add("hidden");
}

function switchAuthTab(tab) {
  const formLogin = document.getElementById("formLogin");
  const formReg = document.getElementById("formRegister");
  const tabLogin = document.getElementById("tabAuthLogin");
  const tabReg = document.getElementById("tabAuthRegister");
  const title = document.getElementById("authModalTitle");

  if (tab === "login") {
    if (formLogin) formLogin.classList.remove("hidden");
    if (formReg) formReg.classList.add("hidden");
    if (tabLogin) {
      tabLogin.className = "py-1.5 rounded-md bg-white dark:bg-zinc-900 text-zinc-950 dark:text-zinc-50 shadow-xs transition";
    }
    if (tabReg) {
      tabReg.className = "py-1.5 rounded-md text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition";
    }
    if (title) title.textContent = "Iniciar Sesión";
  } else {
    if (formLogin) formLogin.classList.add("hidden");
    if (formReg) formReg.classList.remove("hidden");
    if (tabReg) {
      tabReg.className = "py-1.5 rounded-md bg-white dark:bg-zinc-900 text-zinc-950 dark:text-zinc-50 shadow-xs transition";
    }
    if (tabLogin) {
      tabLogin.className = "py-1.5 rounded-md text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition";
    }
    if (title) title.textContent = "Crear Cuenta Segura";
  }
}

async function handleAuthLogin(e) {
  if (e && e.preventDefault) e.preventDefault();
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;
  const errBox = document.getElementById("loginErrorMsg");
  const btn = document.getElementById("btnLoginSubmit");

  if (errBox) errBox.classList.add("hidden");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Credenciales incorrectas");
    }

    currentAuthToken = data.token;
    currentUser = data.user;
    localStorage.setItem("tlx_auth_token", currentAuthToken);

    updateAuthUI();
    closeAuthModal();

    console.log(`[Auth] Sesión iniciada con éxito para ${currentUser.nombre} (UID: ${currentUser.uid})`);
  } catch (err) {
    if (errBox) {
      errBox.textContent = err.message;
      errBox.classList.remove("hidden");
    }
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function handleAuthRegister(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nombre = document.getElementById("regNombre").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const empresa = document.getElementById("regEmpresa").value.trim();
  const password = document.getElementById("regPassword").value;
  const errBox = document.getElementById("regErrorMsg");
  const btn = document.getElementById("btnRegisterSubmit");

  if (errBox) errBox.classList.add("hidden");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, email, password, empresa })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error en el registro");
    }

    currentAuthToken = data.token;
    currentUser = data.user;
    localStorage.setItem("tlx_auth_token", currentAuthToken);

    updateAuthUI();
    closeAuthModal();

    console.log(`[Auth] Usuario registrado con éxito: ${currentUser.nombre} (UID: ${currentUser.uid})`);
  } catch (err) {
    if (errBox) {
      errBox.textContent = err.message;
      errBox.classList.remove("hidden");
    }
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function checkAuthStatus() {
  if (!currentAuthToken) {
    updateAuthUI();
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      headers: { "Authorization": `Bearer ${currentAuthToken}` }
    });

    if (res.ok) {
      const data = await res.json();
      currentUser = data.user;
      currentUser.cotizaciones_incompletas_count = data.cotizaciones_incompletas_count || 0;
      updateAuthUI();
    } else {
      currentAuthToken = "";
      currentUser = null;
      localStorage.removeItem("tlx_auth_token");
      updateAuthUI();
    }
  } catch (err) {
    console.warn("[Auth] No se pudo validar sesión:", err);
    updateAuthUI();
  }
}

function updateAuthUI() {
  const btnOpen = document.getElementById("btnOpenAuthModal");
  const userBar = document.getElementById("userProfileBar");
  const userName = document.getElementById("userDisplayName");
  const userAvatar = document.getElementById("userAvatarInitials");
  const userBadge = document.getElementById("userPendingBadge");

  if (currentUser && currentAuthToken) {
    if (btnOpen) btnOpen.classList.add("hidden");
    if (userBar) {
      userBar.classList.remove("hidden");
      userBar.classList.add("flex");
    }
    if (userName) userName.textContent = currentUser.nombre || "Usuario";
    if (userAvatar) {
      const initials = (currentUser.nombre || "US").split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
      userAvatar.textContent = initials;
    }
    if (userBadge) {
      const cnt = currentUser.cotizaciones_incompletas_count || 0;
      if (cnt > 0) {
        userBadge.textContent = `${cnt} pendiente${cnt > 1 ? 's' : ''}`;
        userBadge.classList.remove("hidden");
      } else {
        userBadge.classList.add("hidden");
      }
    }
  } else {
    if (btnOpen) btnOpen.classList.remove("hidden");
    if (userBar) {
      userBar.classList.add("hidden");
      userBar.classList.remove("flex");
    }
  }
}

async function handleLogout() {
  if (currentAuthToken) {
    try {
      await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${currentAuthToken}` }
      });
    } catch (e) {}
  }
  currentAuthToken = "";
  currentUser = null;
  localStorage.removeItem("tlx_auth_token");
  updateAuthUI();
  closeUserHistoryModal();
}

async function openUserHistoryModal() {
  if (!currentAuthToken) {
    openAuthModal();
    return;
  }
  const modal = document.getElementById("userHistoryModal");
  if (!modal) return;
  modal.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/user/history`, {
      headers: { "Authorization": `Bearer ${currentAuthToken}` }
    });

    if (!res.ok) {
      if (res.status === 401) {
        handleLogout();
        return;
      }
      throw new Error(`Error ${res.status}`);
    }

    const data = await res.json();
    const user = data.user;
    currentUser = user;

    document.getElementById("histModalName").textContent = user.nombre || "Usuario";
    document.getElementById("histModalEmail").textContent = user.email || "";
    document.getElementById("histModalUid").textContent = `UID: ${user.uid || "--"}`;
    const initials = (user.nombre || "US").split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
    document.getElementById("histModalAvatar").textContent = initials;

    // 1. Cotizaciones incompletas
    const pendingList = document.getElementById("userPendingList");
    const pendingCount = (data.cotizaciones_incompletas || []).length;
    document.getElementById("lblPendingCount").textContent = `${pendingCount} guardadas`;

    if (pendingCount === 0) {
      pendingList.innerHTML = `<div class="p-3 rounded-lg border border-dashed border-zinc-200 dark:border-zinc-800 text-zinc-400 dark:text-zinc-500 text-center text-[11px]">No tienes cotizaciones incompletas pendientes.</div>`;
    } else {
      pendingList.innerHTML = data.cotizaciones_incompletas.map(item => {
        const meta = item.metadatos || {};
        const fecha = item.creado_en ? new Date(item.creado_en).toLocaleString() : "";
        const origen = meta.origen || "Bogotá D.C. (Cundinamarca)";
        const destino = meta.destino || "Medellín (Antioquia)";
        const peso = meta.peso || meta.peso_real || 10;
        const largo = meta.largo || 30;
        const ancho = meta.ancho || 30;
        const alto = meta.alto || 30;
        const valor = meta.valor || meta.valor_declarado || 0;
        const tipo = meta.tipo || meta.tipo_mercancia || "General";

        return `
          <div class="p-3 rounded-lg bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 flex items-center justify-between gap-3 shadow-xs">
            <div class="space-y-1 min-w-0">
              <div class="flex items-center space-x-2">
                <span class="font-bold text-zinc-900 dark:text-zinc-100 truncate text-xs">${escapeHtml(origen)} ➔ ${escapeHtml(destino)}</span>
                <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-200/80 dark:bg-amber-900/60 text-amber-900 dark:text-amber-200 shrink-0 font-bold">${peso} kg</span>
              </div>
              <div class="text-[11px] text-zinc-600 dark:text-zinc-400">
                ${largo}x${ancho}x${alto} cm • $${Number(valor).toLocaleString()} COP • ${escapeHtml(tipo)}
              </div>
              <div class="text-[10px] text-zinc-400 font-mono">${fecha}</div>
            </div>
            <button type="button" onclick="restoreQuoteToForm('${escapeHtml(origen)}', '${escapeHtml(destino)}', ${peso}, ${largo}, ${ancho}, ${alto}, ${valor}, '${escapeHtml(tipo)}')" class="shrink-0 text-xs font-semibold bg-amber-600 hover:bg-amber-700 active:scale-95 text-white px-3 py-1.5 rounded-md transition shadow-xs flex items-center gap-1">
              <span>Restaurar</span>
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        `;
      }).join("");
    }

    // 2. Historial de eventos SQLite
    const eventsList = document.getElementById("userEventsList");
    const events = data.eventos_recientes || [];
    if (events.length === 0) {
      eventsList.innerHTML = `<div class="p-2 text-zinc-400 italic text-[11px]">No hay actividad reciente registrada en SQLite.</div>`;
    } else {
      eventsList.innerHTML = events.map(ev => {
        const fecha = ev.creado_en ? new Date(ev.creado_en).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "";
        let badgeColor = "bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300";
        if (ev.tipo_evento === "COTIZACION_INCOMPLETA") badgeColor = "bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300";
        else if (ev.tipo_evento === "COTIZACION_COMPLETADA") badgeColor = "bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300";
        else if (ev.tipo_evento === "QUERY_CHAT") badgeColor = "bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300";

        return `
          <div class="p-2 rounded bg-zinc-50 dark:bg-zinc-950/50 border border-zinc-200 dark:border-zinc-800 flex items-center justify-between gap-2">
            <div class="flex items-center space-x-2 truncate">
              <span class="text-[9px] px-1.5 py-0.5 rounded font-mono font-bold ${badgeColor}">${escapeHtml(ev.tipo_evento)}</span>
              <span class="text-zinc-700 dark:text-zinc-300 text-[11px] truncate">${escapeHtml(ev.descripcion)}</span>
            </div>
            <span class="text-[10px] text-zinc-400 shrink-0 font-mono">${fecha}</span>
          </div>
        `;
      }).join("");
    }

    // 3. Memorias Vectoriales en ChromaDB
    const vectorList = document.getElementById("userVectorMemoriesList");
    const memories = data.memorias_vectoriales || [];
    if (memories.length === 0) {
      vectorList.innerHTML = `<div class="p-2 text-zinc-400 italic text-[11px]">No hay fragmentos vectoriales almacenados aún.</div>`;
    } else {
      vectorList.innerHTML = memories.map(m => `
        <div class="p-2.5 rounded bg-zinc-50 dark:bg-zinc-950/50 border border-zinc-200 dark:border-zinc-800 space-y-1">
          <div class="flex items-center justify-between text-[10px] font-mono text-zinc-500">
            <span class="text-indigo-600 dark:text-indigo-400 font-semibold">🧬 Embedding Ollama (bge-m3)</span>
            <span>${escapeHtml(m.metadata?.tipo_evento || "MEMORIA")}</span>
          </div>
          <p class="text-zinc-700 dark:text-zinc-300 text-[11px] font-mono leading-relaxed">${escapeHtml(m.documento)}</p>
        </div>
      `).join("");
    }

  } catch (err) {
    console.error("Error cargando historial de usuario:", err);
  }
}

function closeUserHistoryModal() {
  const modal = document.getElementById("userHistoryModal");
  if (modal) modal.classList.add("hidden");
}

function restoreQuoteToForm(origen, destino, peso, largo, ancho, alto, valor, tipo) {
  closeUserHistoryModal();
  if (origen) {
    const selO = document.getElementById("cotizOrigen");
    if (selO) selO.value = origen;
  }
  if (destino) {
    const selD = document.getElementById("cotizDestino");
    if (selD) selD.value = destino;
  }
  if (peso) document.getElementById("cotizPeso").value = peso;
  if (largo) document.getElementById("cotizLargo").value = largo;
  if (ancho) document.getElementById("cotizAncho").value = ancho;
  if (alto) document.getElementById("cotizAlto").value = alto;
  if (valor) document.getElementById("cotizValor").value = valor;
  if (tipo) document.getElementById("cotizTipo").value = tipo;

  const widget = document.getElementById("widgetCotizador");
  if (widget) {
    widget.scrollIntoView({ behavior: "smooth", block: "center" });
    widget.classList.add("agent-focus-pulse");
    setTimeout(() => widget.classList.remove("agent-focus-pulse"), 1800);
  }
}

function schedulePendingQuoteTracking() {
  if (!currentAuthToken) return;

  const origen = document.getElementById("cotizOrigen")?.value;
  const destino = document.getElementById("cotizDestino")?.value;
  const alto = parseFloat(document.getElementById("cotizAlto")?.value) || 0;
  const ancho = parseFloat(document.getElementById("cotizAncho")?.value) || 0;
  const largo = parseFloat(document.getElementById("cotizLargo")?.value) || 0;
  const peso = parseFloat(document.getElementById("cotizPeso")?.value) || 0;
  const valor = parseFloat(document.getElementById("cotizValor")?.value) || 0;
  const tipo = document.getElementById("cotizTipo")?.value || "";

  if (!origen || !destino || peso <= 0) return;

  clearTimeout(uncompletedQuoteTimer);
  uncompletedQuoteTimer = setTimeout(async () => {
    const quoteKey = `${origen}-${destino}-${peso}-${largo}x${ancho}x${alto}-${valor}`;
    if (lastTrackedQuotePayload === quoteKey) return;
    lastTrackedQuotePayload = quoteKey;

    try {
      await fetch(`${API_BASE_URL}/api/v1/user/event`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${currentAuthToken}`
        },
        body: JSON.stringify({
          tipo_evento: "COTIZACION_INCOMPLETA",
          descripcion: `Intento de cotización no completado: envío de ${origen} a ${destino}, peso ${peso}kg (${largo}x${ancho}x${alto}cm), valor $${valor.toLocaleString()} COP, tipo: ${tipo}`,
          metadatos: { origen, destino, peso, largo, ancho, alto, valor, tipo }
        })
      });
      console.log("[UserMemory] Cotización incompleta guardada en SQLite y ChromaDB.");
      if (currentUser) {
        currentUser.cotizaciones_incompletas_count = (currentUser.cotizaciones_incompletas_count || 0) + 1;
        updateAuthUI();
      }
    } catch (e) {
      console.warn("No se pudo registrar intento de cotización:", e);
    }
  }, 3500);
}

function setupQuoteInputTracking() {
  const fields = ["cotizOrigen", "cotizDestino", "cotizAlto", "cotizAncho", "cotizLargo", "cotizPeso", "cotizValor", "cotizTipo"];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", schedulePendingQuoteTracking);
      el.addEventListener("change", schedulePendingQuoteTracking);
    }
  });
}

// Sincronizador con Obsidian Vault
async function syncObsidianVault() {
  const btn = document.getElementById("btnSyncObsidian");
  const origHtml = btn ? btn.innerHTML : "";
  if (btn) btn.innerHTML = `<span>Sincronizando...</span>`;

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/obsidian/sync`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      alert("✅ ¡Sincronizado con tu Obsidian Vault exitosamente!\nPuedes abrir Obsidian para explorar el Dashboard, los usuarios, cotizaciones y el Canvas.");
    } else {
      alert("⚠️ Error al sincronizar con Obsidian: " + (data.detail || data.mensaje));
    }
  } catch (err) {
    alert("Error de conexión al sincronizar con Obsidian: " + err.message);
  } finally {
    if (btn) btn.innerHTML = origHtml;
  }
}

// Cargar modelos instalados dinámicamente desde el backend Ollama
async function loadAvailableModels() {
  if (!selectModel) return;
  try {
    const res = await fetch(`${API_BASE_URL}/api/models`);
    if (!res.ok) return;
    const data = await res.json();
    if (data.models && data.models.length > 0) {
      const currentVal = selectModel.value;
      selectModel.innerHTML = "";
      data.models.forEach((m) => {
        const opt = document.createElement("option");
        opt.value = m.id;
        let icon = "⚡";
        if (m.id.includes("gemma")) icon = "💎";
        else if (m.id.includes("llama")) icon = "🦙";
        else if (m.id.includes("1.5b") || m.id.includes("1b")) icon = "⚡";
        else if (m.id.includes("2b")) icon = "💎";
        else if (m.id.includes("3b")) icon = "🍃";
        else if (m.id.includes("14b")) icon = "⚖️";
        else if (m.id.includes("32b")) icon = "🚀";
        else if (m.id.includes("35b")) icon = "🧠";
        opt.textContent = `${icon} ${m.nombre} (${m.size_gb}GB - ${m.tier})`;
        if (m.id === currentVal || (!currentVal && m.id === "qwen2.5:3b")) {
          opt.selected = true;
        }
        selectModel.appendChild(opt);
      });
      if (!selectModel.value && selectModel.options.length > 0) {
        // Preferir 3b o 1.5b si existen
        const pref = Array.from(selectModel.options).find(o => o.value.includes("3b") || o.value.includes("1.5b"));
        if (pref) pref.selected = true;
        else selectModel.options[0].selected = true;
      }
    }
  } catch (e) {
    console.warn("No se pudieron cargar modelos dinámicos:", e);
  }
}

// Iniciar al cargar la ventana
window.addEventListener("DOMContentLoaded", () => {
  checkHealth();
  checkAuthStatus();
  loadGeoDatabase();
  setupQuoteInputTracking();
  loadAvailableModels();
});
