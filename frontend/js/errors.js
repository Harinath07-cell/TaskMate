// Error Guide Page Logic

let allErrors = [];

document.addEventListener("DOMContentLoaded", () => {
  loadErrors();
  setupErrorSearch();
});

async function loadErrors() {
  const container = document.getElementById("error-cards-container");
  if (!container) return;

  try {
    const res = await API.get("/api/errors");
    allErrors = res.data || [];
    renderErrors(allErrors);
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3>Failed to load error definitions</h3>
        <p>${err.message}</p>
        <button class="btn btn-outline btn-sm" onclick="loadErrors()">Retry</button>
      </div>
    `;
  }
}

function setupErrorSearch() {
  const input = document.getElementById("error-search-input");
  if (!input) return;

  input.addEventListener("input", (e) => {
    const term = e.target.value.trim().toLowerCase();
    if (!term) {
      renderErrors(allErrors);
      return;
    }
    const filtered = allErrors.filter(err =>
      err.code.toLowerCase().includes(term) ||
      err.name.toLowerCase().includes(term) ||
      err.meaning.toLowerCase().includes(term)
    );
    renderErrors(filtered);
  });
}

function renderErrors(errors) {
  const container = document.getElementById("error-cards-container");
  if (!container) return;

  if (errors.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No error codes matched</h3>
        <p>Try searching by code number (e.g. 404, 500) or by name.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = errors.map(err => {
    const isCustom = err.code === "DEV001";
    const badgeColor = isCustom ? "badge-high" : (err.http_status >= 500 ? "badge-high" : "badge-medium");
    const causesHtml = (err.common_causes || []).map(c => `<li>${escapeHtml(c)}</li>`).join("");
    const solutionsHtml = (err.solutions || []).map(s => `<li>${escapeHtml(s)}</li>`).join("");

    return `
      <div class="card" style="margin-bottom: 1.5rem;" id="error-card-${err.code}">
        <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;">
          <div>
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.25rem;">
              <span class="badge ${badgeColor}" style="font-size: 0.85rem; padding: 0.3rem 0.75rem;">
                ${isCustom ? "CUSTOM CODE" : `HTTP ${err.code}`}
              </span>
              <h3 style="margin: 0; font-size: 1.3rem;">${escapeHtml(err.name)}</h3>
            </div>
            <p style="margin: 0; color: var(--text-muted); font-size: 0.85rem;">
              ${isCustom ? "TaskMate Internal Application Exception" : `Standard HTTP Status Code ${err.code}`}
            </p>
          </div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button 
              type="button" 
              class="btn btn-outline btn-sm" 
              onclick="simulateError('${err.code.toLowerCase()}')"
            >
              ⚡ Test API Call
            </button>
            <button 
              type="button" 
              class="btn btn-primary btn-sm" 
              onclick="askAboutError('${err.code}', '${escapeHtml(err.name).replace(/'/g, "\\'")}')"
            >
              💬 Ask Assistant
            </button>
          </div>
        </div>

        <p style="font-size: 1rem; color: var(--text-primary); margin-bottom: 1rem;">
          <strong>Meaning:</strong> ${escapeHtml(err.meaning)}
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
          <div style="background-color: var(--bg-subtle); padding: 1rem; border-radius: var(--radius-md);">
            <h4 style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--danger); margin-bottom: 0.5rem;">
              ⚠️ Common Causes
            </h4>
            <ul style="padding-left: 1.25rem; font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5;">
              ${causesHtml}
            </ul>
          </div>

          <div style="background-color: var(--bg-subtle); padding: 1rem; border-radius: var(--radius-md);">
            <h4 style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--success); margin-bottom: 0.5rem;">
              ✅ Recommended Solutions
            </h4>
            <ul style="padding-left: 1.25rem; font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5;">
              ${solutionsHtml}
            </ul>
          </div>
        </div>

        <div id="sim-result-${err.code.toLowerCase()}" style="display: none; margin-top: 1rem; padding: 0.75rem 1rem; border-radius: var(--radius-md); background: #1e293b; color: #f8fafc; font-family: monospace; font-size: 0.85rem;">
        </div>
      </div>
    `;
  }).join("");
}

async function simulateError(code) {
  const resultEl = document.getElementById(`sim-result-${code}`);
  if (!resultEl) return;

  resultEl.style.display = "block";
  resultEl.textContent = `Calling GET /api/errors/test/${code}...`;

  try {
    const res = await fetch(`/api/errors/test/${code}`);
    const data = await res.json();
    resultEl.textContent = `Status: ${res.status} ${res.statusText}\nResponse: ${JSON.stringify(data, null, 2)}`;
  } catch (err) {
    resultEl.textContent = `Error: ${err.message}`;
  }
}

function askAboutError(code, name) {
  if (window.TaskMateChat) {
    window.TaskMateChat.open();
    window.TaskMateChat.sendMessage(`Can you explain error ${code} (${name}) and how to solve it?`);
  }
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
