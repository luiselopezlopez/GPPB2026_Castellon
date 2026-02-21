const mensajeEl = document.getElementById("mensaje");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");
const statusEl = document.getElementById("status");
const conversacionEl = document.getElementById("conversacion");

function setStatus(text, type = "") {
  statusEl.textContent = text;
  statusEl.className = `status ${type}`.trim();
}

async function enviarPeticion() {
  const mensaje = mensajeEl.value.trim();

  if (!mensaje) {
    setStatus("El mensaje no puede estar vacío.", "error");
    mensajeEl.focus();
    return;
  }

  sendBtn.disabled = true;
  setStatus("Enviando petición...", "");
  appendMessage("user", mensaje);

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensaje }),
    });

    const payload = await response.json();

    if (!response.ok) {
      setStatus(payload.error || "No se pudo procesar la petición.", "error");
      return;
    }

    appendMessage(
      "agent",
      payload.respuesta || "(sin texto en la respuesta)",
      payload.respuesta_html || null
    );
    mensajeEl.value = "";
    setStatus("Petición procesada correctamente.", "ok");
  } catch (error) {
    appendMessage("agent", "No se pudo obtener respuesta del agente.");
    setStatus(`Error de conexión: ${error.message}`, "error");
  } finally {
    sendBtn.disabled = false;
    mensajeEl.focus();
  }
}

function appendMessage(type, text, html = null) {
  const emptyConversationEl = document.getElementById("emptyConversation");
  if (emptyConversationEl) {
    emptyConversationEl.remove();
  }

  const message = document.createElement("div");
  message.className = `msg ${type}`;
  if (type === "agent" && html) {
    message.innerHTML = html;
  } else {
    message.textContent = text;
  }
  conversacionEl.appendChild(message);
  conversacionEl.scrollTop = conversacionEl.scrollHeight;
}

async function resetConversation() {
  resetBtn.disabled = true;
  setStatus("Reiniciando conversación...", "");

  try {
    const response = await fetch("/reset", { method: "POST" });
    const payload = await response.json();

    if (!response.ok || !payload.ok) {
      setStatus(payload.error || "No se pudo reiniciar.", "error");
      return;
    }

    conversacionEl.innerHTML = '<div id="emptyConversation" class="empty">Aún no hay mensajes.</div>';
    mensajeEl.value = "";
    setStatus("Conversación reiniciada.", "ok");
  } catch (error) {
    setStatus(`Error de conexión: ${error.message}`, "error");
  } finally {
    resetBtn.disabled = false;
  }
}

sendBtn.addEventListener("click", enviarPeticion);
resetBtn.addEventListener("click", resetConversation);
mensajeEl.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    enviarPeticion();
  }
});
