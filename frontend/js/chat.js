// Reusable TaskMate AI Chatbot Widget & Support Ticket Integration

(function () {
  let conversationId = sessionStorage.getItem("taskmate_chat_conv_id") || null;
  if (!conversationId) {
    conversationId = "conv_" + Math.random().toString(36).substring(2, 10);
    sessionStorage.setItem("taskmate_chat_conv_id", conversationId);
  }

  let isChatOpen = false;
  let isSending = false;

  function initChatbot() {
    // Inject Chatbot HTML into the document body
    const widgetContainer = document.createElement("div");
    widgetContainer.id = "taskmate-chat-root";
    widgetContainer.innerHTML = `
      <!-- Floating Button -->
      <button id="chat-toggle-btn" class="chat-widget-btn" title="Open AI Assistant" aria-label="Open AI Assistant">
        <svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>
      </button>

      <!-- Chat Window -->
      <div id="chat-window-box" class="chat-window" role="dialog" aria-modal="true" aria-label="TaskMate AI Assistant">
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-header-avatar">🤖</div>
            <div>
              <h4 class="chat-header-title">TaskMate Assistant</h4>
              <p class="chat-header-status"><span class="status-dot"></span> Online & Grounded</p>
            </div>
          </div>
          <button id="chat-close-x" class="chat-close-btn" title="Close Assistant" aria-label="Close Assistant">✕</button>
        </div>

        <div id="chat-messages-container" class="chat-messages">
          <!-- Initial Welcome Message -->
          <div class="chat-message assistant">
            <div class="chat-bubble">
              👋 Hi! I'm your TaskMate AI Assistant. You can ask me how to create and organize tasks, look up FAQs, or understand HTTP error codes like 400, 404, 500, or DEV001!
            </div>
            <div class="chat-meta">Just now</div>
          </div>
        </div>

        <div class="chat-input-area">
          <form id="chat-msg-form" class="chat-input-form">
            <input 
              type="text" 
              id="chat-user-input" 
              class="chat-input" 
              placeholder="Ask a question..." 
              autocomplete="off" 
              maxlength="500" 
              required
            />
            <button type="submit" id="chat-submit-btn" class="chat-send-btn" title="Send message" aria-label="Send message">
              <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
            </button>
          </form>
        </div>
      </div>

      <!-- Support Ticket Modal -->
      <div id="ticket-modal-overlay" class="modal-overlay">
        <div class="modal-card">
          <div class="modal-header">
            <h3 style="margin: 0; font-size: 1.25rem;">🎫 Create Support Ticket</h3>
            <button type="button" class="btn btn-secondary btn-sm" onclick="window.TaskMateChat.closeTicketModal()">✕</button>
          </div>
          <form id="create-ticket-form">
            <div class="modal-body">
              <p style="font-size: 0.9rem; margin-bottom: 1rem; color: var(--text-secondary);">
                Please provide details about the issue you are facing. Our team will review your ticket promptly.
              </p>
              <div class="form-group">
                <label class="form-label" for="ticket-title-input">Issue Title <span class="required">*</span></label>
                <input type="text" id="ticket-title-input" class="form-control" placeholder="Brief summary of the problem" maxlength="255" required />
              </div>
              <div class="form-group">
                <label class="form-label" for="ticket-desc-input">Description <span class="required">*</span></label>
                <textarea id="ticket-desc-input" class="form-control" placeholder="Detailed explanation..." required></textarea>
              </div>
              <div class="form-group">
                <label class="form-label" for="ticket-email-input">Your Email (Optional)</label>
                <input type="email" id="ticket-email-input" class="form-control" placeholder="user@example.com" />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" onclick="window.TaskMateChat.closeTicketModal()">Cancel</button>
              <button type="submit" class="btn btn-primary" id="ticket-submit-btn">Submit Ticket</button>
            </div>
          </form>
        </div>
      </div>
    `;

    document.body.appendChild(widgetContainer);

    // Wire Event Listeners
    const toggleBtn = document.getElementById("chat-toggle-btn");
    const closeBtn = document.getElementById("chat-close-x");
    const chatForm = document.getElementById("chat-msg-form");
    const ticketForm = document.getElementById("create-ticket-form");

    if (toggleBtn) toggleBtn.addEventListener("click", toggleChat);
    if (closeBtn) closeBtn.addEventListener("click", closeChat);
    if (chatForm) chatForm.addEventListener("submit", handleChatSubmit);
    if (ticketForm) ticketForm.addEventListener("submit", handleTicketSubmit);
  }

  function toggleChat() {
    isChatOpen ? closeChat() : openChat();
  }

  function openChat() {
    const win = document.getElementById("chat-window-box");
    if (win) {
      win.classList.add("open");
      isChatOpen = true;
      const input = document.getElementById("chat-user-input");
      if (input) setTimeout(() => input.focus(), 200);
    }
  }

  function closeChat() {
    const win = document.getElementById("chat-window-box");
    if (win) {
      win.classList.remove("open");
      isChatOpen = false;
    }
  }

  async function handleChatSubmit(e) {
    if (e) e.preventDefault();
    const input = document.getElementById("chat-user-input");
    if (!input) return;

    const message = input.value.trim();
    if (!message || isSending) return;

    input.value = "";
    await sendMessage(message);
  }

  async function sendMessage(text) {
    appendMessage("user", text);
    showTypingIndicator();
    isSending = true;

    try {
      const res = await API.post("/api/chat", {
        message: text,
        conversation_id: conversationId
      });

      removeTypingIndicator();
      const data = res.data;
      appendMessage("assistant", data.response, data.message_id, data.suggest_ticket);
    } catch (err) {
      removeTypingIndicator();
      let errorText = "Sorry, I ran into an issue communicating with the assistant.";
      if (err.status === 429) {
        errorText = "Too many requests. Please wait a moment before sending another message.";
      } else if (err.message) {
        errorText = err.message;
      }
      appendMessage("assistant", errorText, null, true);
    } finally {
      isSending = false;
    }
  }

  function appendMessage(role, content, messageId = null, suggestTicket = false) {
    const container = document.getElementById("chat-messages-container");
    if (!container) return;

    const msgEl = document.createElement("div");
    msgEl.className = `chat-message ${role}`;

    // Convert line breaks and format bolding
    let formatted = escapeHtml(content)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");

    let actionsHtml = "";
    if (role === "assistant") {
      if (suggestTicket) {
        actionsHtml += `
          <button type="button" class="ticket-prompt-btn" onclick="window.TaskMateChat.openTicketModal()">
            🎫 Open Support Ticket
          </button>
        `;
      }
      if (messageId) {
        actionsHtml += `
          <div class="chat-actions">
            <button type="button" class="feedback-btn" onclick="window.TaskMateChat.sendFeedback('${messageId}', 'helpful', this)">👍 Helpful</button>
            <button type="button" class="feedback-btn" onclick="window.TaskMateChat.sendFeedback('${messageId}', 'not_helpful', this)">👎 Not Helpful</button>
          </div>
        `;
      }
    }

    msgEl.innerHTML = `
      <div class="chat-bubble">${formatted}</div>
      ${actionsHtml}
      <div class="chat-meta">${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
    `;

    container.appendChild(msgEl);
    container.scrollTop = container.scrollHeight;
  }

  function showTypingIndicator() {
    const container = document.getElementById("chat-messages-container");
    if (!container || document.getElementById("chat-typing-indicator")) return;

    const indicator = document.createElement("div");
    indicator.id = "chat-typing-indicator";
    indicator.className = "typing-indicator";
    indicator.innerHTML = `
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    `;
    container.appendChild(indicator);
    container.scrollTop = container.scrollHeight;
  }

  function removeTypingIndicator() {
    const indicator = document.getElementById("chat-typing-indicator");
    if (indicator) indicator.remove();
  }

  async function sendFeedback(messageId, rating, btn) {
    try {
      await API.post("/api/chat/feedback", {
        conversation_id: conversationId,
        message_id: messageId,
        rating: rating
      });
      const parent = btn.parentElement;
      if (parent) {
        parent.innerHTML = `<span style="font-size: 0.75rem; color: var(--success); font-weight: 600;">✓ Thanks for feedback!</span>`;
      }
    } catch (err) {
      console.warn("Feedback error:", err);
    }
  }

  function openTicketModal() {
    openModal("ticket-modal-overlay");
  }

  function closeTicketModal() {
    closeModal("ticket-modal-overlay");
  }

  async function handleTicketSubmit(e) {
    e.preventDefault();
    const titleInput = document.getElementById("ticket-title-input");
    const descInput = document.getElementById("ticket-desc-input");
    const emailInput = document.getElementById("ticket-email-input");

    const title = titleInput.value.trim();
    const description = descInput.value.trim();
    const email = emailInput.value.trim();

    if (!title || !description) {
      showToast("Please fill in the required ticket fields.", "error");
      return;
    }

    try {
      const res = await API.post("/api/tickets", {
        title,
        description,
        email: email || null
      });

      closeTicketModal();
      showToast("Support ticket created!", "success");
      titleInput.value = "";
      descInput.value = "";
      emailInput.value = "";

      // Post in chat
      appendMessage("assistant", `✅ ${res.message}\nYou can reference this ID when contacting support.`);
    } catch (err) {
      showToast(err.message || "Failed to create support ticket.", "error");
    }
  }

  function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Expose global controller
  window.TaskMateChat = {
    open: openChat,
    close: closeChat,
    toggle: toggleChat,
    sendMessage,
    openTicketModal,
    closeTicketModal,
    sendFeedback
  };

  document.addEventListener("DOMContentLoaded", initChatbot);
})();
