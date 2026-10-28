// TaskMate API Client
// Supports both same-origin deployment and cross-origin hosting (e.g., Vercel + Render)

const API = {
  getBaseUrl() {
    // If an explicit API base URL is configured in window, use it; otherwise use same origin
    return window.TASKMATE_API_BASE || "";
  },

  async request(endpoint, options = {}) {
    const url = `${this.getBaseUrl()}${endpoint}`;
    const defaultHeaders = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data?.error?.message || `Request failed with status ${response.status}`;
        const err = new Error(errorMsg);
        err.status = response.status;
        err.errorData = data?.error;
        throw err;
      }

      return data;
    } catch (err) {
      if (!err.status) {
        err.status = 0;
        err.message = err.message || "Network connection error. Server may be unreachable.";
      }
      throw err;
    }
  },

  get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  },

  post(endpoint, body) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(body)
    });
  },

  put(endpoint, body) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(body)
    });
  },

  patch(endpoint, body = {}) {
    return this.request(endpoint, {
      method: "PATCH",
      body: JSON.stringify(body)
    });
  },

  delete(endpoint) {
    return this.request(endpoint, { method: "DELETE" });
  }
};
