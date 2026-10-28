// Task Management UI Logic

let currentTasks = [];
let currentFilter = "all";

document.addEventListener("DOMContentLoaded", () => {
  loadTasks();
  loadProgrammingJoke();
  setupTaskEventListeners();
});

function setupTaskEventListeners() {
  // Add task form submission
  const addForm = document.getElementById("add-task-form");
  if (addForm) {
    addForm.addEventListener("submit", handleAddTask);
  }

  // Clear button
  const clearBtn = document.getElementById("clear-task-btn");
  if (clearBtn && addForm) {
    clearBtn.addEventListener("click", () => addForm.reset());
  }

  // Filter tabs
  const filterTabs = document.querySelectorAll(".filter-tab");
  filterTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      filterTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentFilter = tab.dataset.filter || "all";
      renderTasks();
    });
  });

  // Edit task form submission
  const editForm = document.getElementById("edit-task-form");
  if (editForm) {
    editForm.addEventListener("submit", handleEditTask);
  }
}

async function loadTasks() {
  const listEl = document.getElementById("task-list-container");
  if (!listEl) return;

  try {
    const res = await API.get("/api/tasks");
    currentTasks = res.data || [];
    updateStatistics();
    renderTasks();
  } catch (err) {
    listEl.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3>Failed to load tasks</h3>
        <p>${err.message}</p>
        <button class="btn btn-outline btn-sm" onclick="loadTasks()">Retry</button>
      </div>
    `;
  }
}

function updateStatistics() {
  const total = currentTasks.length;
  const completed = currentTasks.filter(t => t.is_completed).length;
  const pending = total - completed;
  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const totalEl = document.getElementById("stat-total");
  const pendingEl = document.getElementById("stat-pending");
  const completedEl = document.getElementById("stat-completed");
  const rateEl = document.getElementById("stat-rate");

  if (totalEl) totalEl.textContent = total;
  if (pendingEl) pendingEl.textContent = pending;
  if (completedEl) completedEl.textContent = completed;
  if (rateEl) rateEl.textContent = `${rate}%`;
}

function renderTasks() {
  const listEl = document.getElementById("task-list-container");
  if (!listEl) return;

  let filtered = currentTasks;
  if (currentFilter === "pending") {
    filtered = currentTasks.filter(t => !t.is_completed);
  } else if (currentFilter === "completed") {
    filtered = currentTasks.filter(t => t.is_completed);
  }

  if (filtered.length === 0) {
    listEl.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>No tasks found</h3>
        <p>${currentFilter === "all" ? "You have no tasks yet. Create your first task above!" : `No ${currentFilter} tasks right now.`}</p>
      </div>
    `;
    return;
  }

  listEl.innerHTML = filtered.map(task => {
    const priorityClass = `badge-${task.priority.toLowerCase()}`;
    const dueDateText = task.due_date ? `📅 Due: ${task.due_date}` : "";
    const isChecked = task.is_completed;

    return `
      <div class="task-item ${isChecked ? "completed" : ""}" data-id="${task.id}">
        <div class="task-main">
          <button 
            type="button"
            class="task-checkbox-btn ${isChecked ? "checked" : ""}" 
            title="${isChecked ? "Reopen Task" : "Complete Task"}"
            onclick="toggleTaskComplete(${task.id}, ${isChecked})"
          >
            ${isChecked ? "✓" : ""}
          </button>
          <div class="task-content">
            <h4 class="task-title">${escapeHtml(task.title)}</h4>
            ${task.description ? `<p class="task-desc">${escapeHtml(task.description)}</p>` : ""}
            <div class="task-meta">
              <span class="badge ${priorityClass}">${task.priority}</span>
              ${dueDateText ? `<span>${dueDateText}</span>` : ""}
            </div>
          </div>
        </div>
        <div class="task-actions">
          <button class="btn btn-secondary btn-sm" onclick="openEditModal(${task.id})">Edit</button>
          <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">Delete</button>
        </div>
      </div>
    `;
  }).join("");
}

async function handleAddTask(e) {
  e.preventDefault();
  const form = e.target;
  const title = form.title.value.trim();
  const description = form.description.value.trim();
  const priority = form.priority.value;
  const due_date = form.due_date.value;

  if (!title) {
    showToast("Task title is required", "error");
    return;
  }

  const payload = { title, priority };
  if (description) payload.description = description;
  if (due_date) payload.due_date = due_date;

  try {
    const res = await API.post("/api/tasks", payload);
    showToast("Task created successfully!", "success");
    form.reset();
    await loadTasks();
  } catch (err) {
    showToast(err.message || "Failed to create task", "error");
  }
}

async function toggleTaskComplete(id, currentlyCompleted) {
  const endpoint = currentlyCompleted ? `/api/tasks/${id}/reopen` : `/api/tasks/${id}/complete`;
  try {
    await API.patch(endpoint);
    showToast(currentlyCompleted ? "Task reopened" : "Task completed!", "success");
    await loadTasks();
  } catch (err) {
    showToast(err.message || "Action failed", "error");
  }
}

async function deleteTask(id) {
  if (!confirm("Are you sure you want to delete this task?")) return;

  try {
    await API.delete(`/api/tasks/${id}`);
    showToast("Task deleted", "info");
    await loadTasks();
  } catch (err) {
    showToast(err.message || "Failed to delete task", "error");
  }
}

function openEditModal(id) {
  const task = currentTasks.find(t => t.id === id);
  if (!task) return;

  const form = document.getElementById("edit-task-form");
  if (!form) return;

  form.task_id.value = task.id;
  form.title.value = task.title;
  form.description.value = task.description || "";
  form.priority.value = task.priority || "Medium";
  form.due_date.value = task.due_date || "";

  openModal("edit-task-modal");
}

async function handleEditTask(e) {
  e.preventDefault();
  const form = e.target;
  const id = form.task_id.value;
  const title = form.title.value.trim();
  const description = form.description.value.trim();
  const priority = form.priority.value;
  const due_date = form.due_date.value;

  if (!title) {
    showToast("Task title is required", "error");
    return;
  }

  const payload = {
    title,
    description: description || null,
    priority,
    due_date: due_date || null
  };

  try {
    await API.put(`/api/tasks/${id}`, payload);
    showToast("Task updated successfully!", "success");
    closeModal("edit-task-modal");
    await loadTasks();
  } catch (err) {
    showToast(err.message || "Failed to update task", "error");
  }
}

async function loadProgrammingJoke() {
  const jokeContainer = document.getElementById("programming-joke");
  if (!jokeContainer) return;

  try {
    const res = await API.get("/api/joke");
    const joke = res.data;
    jokeContainer.innerHTML = `
      <div class="joke-icon">💡</div>
      <div class="joke-body">
        <p class="joke-setup">${escapeHtml(joke.setup)}</p>
        <p class="joke-punchline">${escapeHtml(joke.punchline)}</p>
      </div>
    `;
  } catch (err) {
    jokeContainer.innerHTML = `
      <div class="joke-icon">💡</div>
      <div class="joke-body">
        <p class="joke-setup">Why do programmers prefer dark mode?</p>
        <p class="joke-punchline">Because light attracts bugs!</p>
      </div>
    `;
  }
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
