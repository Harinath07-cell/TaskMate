// FAQ Page Logic

let allFaqs = [];

document.addEventListener("DOMContentLoaded", () => {
  loadFaqs();
  setupFaqSearch();
});

async function loadFaqs() {
  const container = document.getElementById("faq-accordion");
  if (!container) return;

  try {
    const res = await API.get("/api/faqs");
    allFaqs = res.data || [];
    renderFaqs(allFaqs);
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3>Failed to load FAQs</h3>
        <p>${err.message}</p>
        <button class="btn btn-outline btn-sm" onclick="loadFaqs()">Retry</button>
      </div>
    `;
  }
}

function setupFaqSearch() {
  const searchInput = document.getElementById("faq-search-input");
  if (!searchInput) return;

  let debounceTimer;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const query = e.target.value.trim();
      if (!query) {
        renderFaqs(allFaqs);
        return;
      }
      try {
        const res = await API.get(`/api/faqs/search?q=${encodeURIComponent(query)}`);
        renderFaqs(res.data || []);
      } catch (err) {
        // Fallback to client-side filtering if search endpoint encounters an issue
        const filtered = allFaqs.filter(
          f => f.question.toLowerCase().includes(query.toLowerCase()) ||
               f.answer.toLowerCase().includes(query.toLowerCase())
        );
        renderFaqs(filtered);
      }
    }, 200);
  });
}

function renderFaqs(faqs) {
  const container = document.getElementById("faq-accordion");
  const countBadge = document.getElementById("faq-count-badge");
  if (!container) return;

  if (countBadge) {
    countBadge.textContent = `${faqs.length} Question${faqs.length === 1 ? "" : "s"}`;
  }

  if (faqs.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No matching questions found</h3>
        <p>Try searching for a different keyword or ask our AI Assistant.</p>
        <button class="btn btn-primary btn-sm" onclick="window.TaskMateChat && window.TaskMateChat.open()">Ask Assistant</button>
      </div>
    `;
    return;
  }

  container.innerHTML = faqs.map((faq, index) => {
    return `
      <div class="card" style="margin-bottom: 0.85rem; padding: 1.25rem; cursor: pointer;" onclick="toggleFaqAccordion(${faq.id})">
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
          <h4 style="margin: 0; font-size: 1.05rem; display: flex; align-items: center; gap: 0.75rem;">
            <span style="color: var(--primary); font-weight: 800;">Q.</span>
            <span>${escapeHtml(faq.question)}</span>
          </h4>
          <span id="faq-chevron-${faq.id}" style="color: var(--text-muted); font-size: 1.15rem; transition: var(--transition);">▼</span>
        </div>
        <div id="faq-answer-${faq.id}" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6;">
          ${escapeHtml(faq.answer)}
          <div style="margin-top: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge" style="background-color: var(--bg-subtle); color: var(--text-secondary);">${escapeHtml(faq.category || "General")}</span>
            <button 
              type="button" 
              class="btn btn-outline btn-sm" 
              style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" 
              onclick="event.stopPropagation(); askAboutFaq('${escapeHtml(faq.question).replace(/'/g, "\\'")}')"
            >
              Ask Assistant
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function toggleFaqAccordion(id) {
  const answer = document.getElementById(`faq-answer-${id}`);
  const chevron = document.getElementById(`faq-chevron-${id}`);
  if (!answer) return;

  const isHidden = answer.style.display === "none";
  answer.style.display = isHidden ? "block" : "none";
  if (chevron) {
    chevron.style.transform = isHidden ? "rotate(180deg)" : "rotate(0deg)";
    chevron.style.color = isHidden ? "var(--primary)" : "var(--text-muted)";
  }
}

function askAboutFaq(questionText) {
  if (window.TaskMateChat) {
    window.TaskMateChat.open();
    window.TaskMateChat.sendMessage(questionText);
  }
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
