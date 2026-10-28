# TaskMate — AI-Powered Task Manager with Intelligent FAQ and Error Support

A complete, production-ready, full-stack personal task management web application featuring a grounded AI assistant powered by Groq LPUs, MySQL relational database with automatic SQLite fallback, MongoDB chat and feedback logging, centralized error tracking, and automated deployment readiness.

---

## 1. Project Title
**TaskMate — AI-Powered Task Manager with Intelligent FAQ and Error Support**

---

## 2. Project Overview
TaskMate enables students and professionals to organize daily tasks, set priorities, track due dates, and monitor completion rates with live metrics. Beyond standard task tracking, TaskMate integrates an intelligent AI Assistant grounded directly in the application's relational FAQ knowledge base and error code directory. When issues cannot be resolved automatically, the assistant enables users to generate support tickets with collision-resistant tracking IDs.

---

## 3. Problem Statement
Everyday task management tools often leave users stranded when technical errors, network interruptions, or configuration issues arise. Students and users must navigate confusing HTTP error codes without context or support channels. TaskMate solves this by integrating task productivity with contextual, grounded AI troubleshooting, relational knowledge bases, autonomous task action execution via LLM tool calling, and built-in ticket escalation.

---

## 4. Objectives
- Deliver a responsive, intuitive task management dashboard with real-time progress metrics.
- Establish a dual-database architecture: MySQL for structured business entities (tasks, FAQs, tickets) and MongoDB for flexible conversational logs and feedback.
- Provide a grounded AI agent backed by Groq API (`openai/gpt-oss-120b` / Llama 3.3) with function calling tools and an automated offline fallback to ensure 100% uptime.
- Implement comprehensive error handling for HTTP 400, 401, 403, 404, 429, 500, 503, and custom application code `DEV001`.
- Maintain strict security practices: zero hardcoded secrets, parameterized queries, and defensive timeouts.

---

## 5. Features
- **Task Management**: Create, read, update, complete, reopen, and delete tasks with priority levels (Low, Medium, High) and due dates.
- **Dynamic Metrics**: Instant calculation of total tasks, pending tasks, completed tasks, and completion percentage.
- **Autonomous AI Agent**: Floating chatbot widget embedded across every page capable of answering questions, listing pending tasks, creating tasks, and checking ticket status using Groq API tool execution.
- **Relational FAQ Engine**: Searchable MySQL-backed knowledge base with animated accordion expand/collapse.
- **Error Code Guide**: Interactive troubleshooting guide for 8 error codes with live simulated API test execution.
- **Support Ticket Escalation**: Automatic generation of collision-resistant ticket codes (`TKT-YYYY-XXXX`) stored in MySQL.
- **MongoDB Audit & Feedback**: Conversation logging and helpful/unhelpful rating capture with graceful offline tolerance.
- **External API Safety**: Daily programming joke integration with 3.0s timeout and offline fallback jokes.
- **System Monitoring**: Live `/health` diagnostic endpoint and structured request logging.
- **Custom Error Pages**: Dedicated, user-friendly 404 and 500 pages with direct "Ask the Assistant" integration.

---

## 6. Technology Stack

### Frontend
- **HTML5**: Semantic markup across 4 primary pages (`/`, `/faq`, `/errors`, `/about`).
- **CSS3**: Modern responsive styling with custom CSS variables, Flexbox, and CSS Grid.
- **Vanilla JavaScript (ES6+)**: Modular scripts communicating with backend REST endpoints via the Fetch API (zero external frontend frameworks).

### Backend
- **Python 3.11+ / Flask 3.0**: Lightweight monolithic REST API.
- **Flask-CORS**: Cross-origin resource sharing configured for development and production domains.
- **PyMySQL & SQLite**: Relational database drivers with automated local fallback.
- **PyMongo**: Official MongoDB driver for document logging.
- **Requests**: HTTP client for Groq AI inference and third-party joke retrieval.
- **Waitress / Gunicorn**: Production WSGI application servers.

### Databases & AI
- **MySQL 8.0**: Relational storage for tasks, FAQs, and support tickets.
- **SQLite 3**: Zero-configuration local development and testing fallback.
- **MongoDB 7.0**: Document storage for chat conversation transcripts and feedback ratings.
- **Groq API**: Ultra-fast LPU inference (`openai/gpt-oss-120b`, `llama-3.3-70b-versatile`) with native OpenAI-compatible function calling and multi-tier offline fallback.

---

## 7. Application Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Frontend Clients (HTML5 / CSS3 / JS)                  │
│   ├── Home / Dashboard (/)          ├── FAQ Knowledge Base (/faq)           │
│   ├── Error Code Guide (/errors)    ├── About & Assessment (/about)         │
│   └── Shared Floating AI Widget     └── Custom 404 & 500 Pages              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ REST JSON / Fetch
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Flask Backend Monolith Service (Python 3.11+)            │
│   ├── App Factory (create_app)      ├── Request Logger (logging_config.py)  │
│   ├── Rate Limiter (sliding window) ├── Health Diagnostic Router (/health)  │
│   └── Route Blueprints:                                                     │
│       ├── /api/tasks   ├── /api/faqs    ├── /api/tickets   ├── /api/errors  │
│       ├── /api/chat    ├── /api/joke    └── Static Page Controllers         │
└──────────────────────┬───────────────────────┬──────────────────────────────┘
                       │                       │
         ┌─────────────┴─────────────┐         └───────────────┐
         ▼                           ▼                         ▼
┌──────────────────┐       ┌──────────────────┐      ┌──────────────────┐
│  MySQL Database  │       │ MongoDB Database │      │  Groq AI Agent   │
│ (taskmate_db)    │       │ (taskmate_logs)  │      │ (LPU Inference)  │
│ ├── tasks        │       │ ├── chat_logs    │      │ ├── list_tasks   │
│ ├── faqs         │       │ └── feedback     │      │ ├── create_task  │
│ └── tickets      │       │ (Graceful Offline│      │ ├── complete_task│
│ (SQLite Fallback)│       │  Tolerance Mode) │      │ └── ticket_status│
└──────────────────┘       └──────────────────┘      └──────────────────┘
```

---

## 8. Project Directory Structure

```text
Gowry-assignment/
├── backend/
│   ├── __init__.py               # Package marker
│   ├── ai_service.py             # Groq AI Agent, tool execution & grounding engine
│   ├── app.py                    # Flask application factory & static routes
│   ├── chat_routes.py            # AI chat endpoint & feedback collection
│   ├── config.py                 # Centralized environment configuration
│   ├── database.py               # Relational DB connection & SQLite fallback
│   ├── error_definitions.py      # HTTP error catalog & DEV001 data
│   ├── error_routes.py           # Error listing & simulation test routes
│   ├── faq_routes.py             # FAQ retrieval & search endpoints
│   ├── health_routes.py          # /health dependency diagnostic endpoint
│   ├── joke_routes.py            # Third-party joke proxy endpoint
│   ├── joke_service.py           # Joke fetcher with 3.0s timeout & fallback
│   ├── logging_config.py         # Structured request logging
│   ├── mongo_client.py           # MongoDB connection & multi-turn history cache
│   ├── requirements.txt          # Backend dependency manifest
│   ├── task_routes.py            # Task CRUD endpoints & status transitions
│   └── ticket_routes.py          # Support ticket creation & tracking
├── database/
│   ├── schema.sql                # MySQL relational DDL table definitions
│   └── seed.sql                  # Initial seed data for FAQs and sample tasks
├── frontend/
│   ├── 404.html                  # Custom user-friendly 404 error page
│   ├── 500.html                  # Custom user-friendly 500 error page
│   ├── about.html                # Project information & student assessment profile
│   ├── errors.html               # Error code guide with live simulation tests
│   ├── faq.html                  # Searchable FAQ accordion page
│   ├── index.html                # Task management dashboard & joke card
│   ├── assets/
│   │   └── logo.svg              # TaskMate brand logo
│   ├── css/
│   │   ├── chat.css              # AI chatbot widget styling
│   │   ├── responsive.css        # Breakpoints for mobile, tablet & desktop
│   │   └── styles.css            # Core design system, variables & components
│   └── js/
│       ├── api.js                # Centralized Fetch API client wrapper
│       ├── app.js                # Global toast notifications & modal controls
│       ├── chat.js               # Reusable floating chatbot component
│       ├── errors.js             # Error guide rendering & test triggers
│       ├── faq.js                # FAQ rendering, search & accordions
│       └── tasks.js              # Task dashboard CRUD, metrics & filters
├── tests/
│   ├── conftest.py               # Pytest test fixtures & in-memory test DB
│   ├── test_chat.py              # Chatbot grounding, Groq tools & rate limit tests
│   ├── test_errors.py            # Error guide & simulation tests
│   ├── test_faqs.py              # FAQ retrieval & keyword search tests
│   ├── test_health.py            # System health endpoint tests
│   ├── test_tasks.py             # Task CRUD & validation tests
│   └── test_tickets.py           # Support ticket generation & code validation
├── .env.example                  # Environment variable configuration template
├── .gitignore                    # Git exclusion rules (ignores secrets & local DBs)
├── Procfile                      # Process configuration for Render / Railway (Gunicorn)
├── pytest.ini                    # Pytest configuration
├── README.md                     # Master project documentation
├── requirements.txt              # Root dependency manifest
├── TASKS.md                      # Development implementation phase tracker
├── vercel.json                   # Vercel serverless deployment routing config
└── wsgi.py                       # WSGI entrypoint for development & production
```

---

## 9. Prerequisites
- **Python**: Version 3.11 or higher.
- **Git**: Installed on your operating system.
- **MySQL Server** (Optional for local dev; SQLite fallback is built-in).
- **MongoDB** (Optional for local dev; graceful offline logging is built-in).
- **Groq API Key**: Free API key from [https://console.groq.com/keys](https://console.groq.com/keys).

---

## 10. Local Installation

```bash
# 1. Clone repository
git clone https://github.com/<your-username>/taskmate-ai.git
cd taskmate-ai

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 11. Environment Variable Configuration

Copy `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```

Configure the following variables in `.env`:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=taskmate-local-dev-secret-key-2026

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=taskmate_db
MYSQL_USER=root
MYSQL_PASSWORD=

# SQLite Fallback (Auto-enabled for local development)
DB_FALLBACK_SQLITE=true
SQLITE_DB_PATH=taskmate_dev.db

# MongoDB Configuration (Chat transcripts & feedback)
MONGODB_URI=mongodb://localhost:27017/taskmate_logs
MONGODB_DATABASE=taskmate_logs

# AI Assistant Configuration (Groq API)
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b

# CORS Configuration
FRONTEND_ORIGIN=http://localhost:5500,http://127.0.0.1:5500,http://localhost:5000,http://127.0.0.1:5000

# Rate Limiting (Chat queries per minute)
CHAT_RATE_LIMIT=30
```

> [!IMPORTANT]
> The `.env` file is excluded from Git via `.gitignore`. Never commit your real API keys or passwords to version control.

---

## 12. MySQL Setup
If running a local MySQL server:
```bash
# Log in to MySQL
mysql -u root -p

# Create database and seed tables
source database/schema.sql;
source database/seed.sql;
```
*(If MySQL is not installed, TaskMate automatically falls back to SQLite `taskmate_dev.db` and self-seeds initial FAQs and tasks).*

---

## 13. MongoDB Setup
If running MongoDB locally:
```bash
mongod --dbpath /path/to/data
```
*(If MongoDB is not running, TaskMate logs an internal warning and enters graceful offline logging mode without interrupting task management or chatbot functionality).*

---

## 14. Backend Startup

### Development Server:
```bash
python wsgi.py
```
Backend will start on `http://127.0.0.1:5000`.

### Production Server (Waitress / Windows):
```bash
python -m waitress --port=5000 backend.app:app
```

### Production Server (Gunicorn / Linux):
```bash
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 2 --threads 4
```

---

## 15. Frontend Startup
The Flask application serves all frontend pages directly:
- **Home Dashboard**: [http://localhost:5000/](http://localhost:5000/)
- **FAQ Page**: [http://localhost:5000/faq](http://localhost:5000/faq)
- **Error Guide**: [http://localhost:5000/errors](http://localhost:5000/errors)
- **About Page**: [http://localhost:5000/about](http://localhost:5000/about)

Alternatively, frontend files can be served independently using any static web server (e.g. VS Code Live Server on `http://localhost:5500`).

---

## 16. API Endpoint Documentation

| Group | Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| **Tasks** | `GET` | `/api/tasks?status=all\|pending\|completed` | Retrieve filtered tasks | 200 / 500 |
| **Tasks** | `GET` | `/api/tasks/<id>` | Retrieve a single task by ID | 200 / 404 / 500 |
| **Tasks** | `POST` | `/api/tasks` | Create a new task (`title`, `priority`, `due_date`) | 201 / 400 / 500 |
| **Tasks** | `PUT` | `/api/tasks/<id>` | Update an existing task | 200 / 400 / 404 / 500 |
| **Tasks** | `PATCH` | `/api/tasks/<id>/complete` | Mark task as completed | 200 / 404 / 500 |
| **Tasks** | `PATCH` | `/api/tasks/<id>/reopen` | Reopen a completed task | 200 / 404 / 500 |
| **Tasks** | `DELETE`| `/api/tasks/<id>` | Delete a task | 200 / 404 / 500 |
| **FAQs** | `GET` | `/api/faqs?search=<query>` | Retrieve all FAQs or search by keyword | 200 / 500 |
| **Chat** | `POST` | `/api/chat` | Send message to Groq AI Agent | 200 / 400 / 429 |
| **Feedback** | `POST` | `/api/chat/feedback` | Record helpful/not helpful rating | 200 / 400 |
| **Tickets** | `POST` | `/api/tickets` | Create support ticket (`title`, `description`, `email`) | 201 / 400 / 500 |
| **Tickets** | `GET` | `/api/tickets/<ticket_code>` | Retrieve ticket status by code | 200 / 404 / 500 |
| **Errors** | `GET` | `/api/errors` | List all 8 documented error definitions | 200 |
| **Simulations** | `GET` | `/api/errors/test/<code>` | Simulate 400, 401, 403, 404, 429, 500, 503, DEV001 | Corresponding Code |
| **Joke API** | `GET` | `/api/joke` | Programming joke with 3s timeout & fallback | 200 |
| **Health** | `GET` | `/health` | Diagnostic status of DB, MongoDB, and AI Agent | 200 / 503 |

---

## 17. AI Assistant & Agent Workflow

1. **User Interaction**: User opens the floating chatbot widget and enters a message.
2. **Rate Limiting**: Request hits `POST /api/chat` and is checked against an in-memory sliding window rate limiter (30 requests/min; returns HTTP 429 if exceeded).
3. **Grounding & Context Compilation**: System scans the MySQL FAQ database, error definitions, and live database task counts.
4. **Conversational Memory**: Recent conversation turns are retrieved from MongoDB (or memory session cache) to preserve multi-turn context.
5. **Groq LPU Agent Execution**: Prompt and OpenAI-compatible tools (`list_tasks`, `create_task`, `complete_task`, `get_ticket_status`, `search_knowledge_base`) are dispatched to Groq API (`openai/gpt-oss-120b`).
   - If Groq decides to call a tool (e.g. creating a task or listing active tasks), the agent executes the action directly against the database and passes the output back to Groq for natural response synthesis.
6. **Graceful Fallback**: If Groq is unavailable, the agent falls back to local grounded rules (FAQ exact matches, error explanations, and support ticket creation).
7. **Audit Logging**: User messages and assistant responses are logged to MongoDB `chat_logs`.
8. **Feedback**: User can rate responses (👍 Helpful / 👎 Not Helpful) logged to MongoDB `feedback`.

---

## 18. Error Code Documentation

| Code | Name | Meaning | Recommended Resolution |
| :--- | :--- | :--- | :--- |
| **400** | Bad Request | Missing required input or invalid date format | Verify input fields and JSON payload format |
| **401** | Unauthorized | Authentication required or credentials invalid | Provide valid authorization headers |
| **403** | Forbidden | Server understands request but refuses access | Verify endpoint permissions and allowed CORS origin |
| **404** | Not Found | Requested task, ticket, or URL does not exist | Verify task ID or check URL route |
| **429** | Too Many Requests | Rate limit exceeded (>30 queries/min) | Pause for 30–60 seconds before sending another message |
| **500** | Internal Server Error | Unexpected server runtime exception | Inspect server logs; retry request |
| **503** | Service Unavailable | Service is undergoing maintenance or DB down | Check `/health` endpoint; retry shortly |
| **DEV001** | TaskMate Application Error | Custom application-level business logic failure | Refresh task list; verify input constraints |

---

## 19. Support Ticket Workflow
1. User clicks **🎫 Open Support Ticket** in the chatbot or navigates from an unresolved inquiry.
2. User provides:
   - Issue Title (Required, max 255 chars)
   - Description (Required)
   - Email (Optional, validated format)
3. Backend validates input and generates a unique collision-resistant ID (`TKT-YYYY-XXXX`).
4. Ticket is saved in MySQL with initial status `OPEN`.
5. Frontend displays confirmation and posts the ticket ID into the chat for immediate reference.
6. User can check ticket status anytime via `GET /api/tickets/<ticket_code>`.

---

## 20. Third-Party API Integration
- **Service**: Official Joke API (`https://official-joke-api.appspot.com/jokes/programming/random`).
- **Resilience Strategy**:
  - 3.0-second network timeout.
  - HTTP status and JSON payload validation.
  - Curated offline programming jokes fallback pool.
  - Core task operations never depend on external API availability.

---

## 21. Logging and Health Check
- **Request Logging**: Configured via `backend/logging_config.py`. Logs timestamp, method, path, HTTP status, and duration in milliseconds. Passwords and API keys are strictly excluded.
- **Health Diagnostic**: Accessed via `GET /health`:
  ```json
  {
    "status": "healthy",
    "service": "TaskMate API",
    "version": "1.0.0",
    "dependencies": {
      "database": {
        "status": "connected",
        "engine": "mysql",
        "critical": true
      },
      "mongodb": {
        "status": "connected",
        "critical": false
      },
      "ai_assistant": {
        "provider": "groq",
        "status": "configured",
        "model": "openai/gpt-oss-120b",
        "critical": false
      }
    }
  }
  ```

---

## 22. Testing Instructions
The test suite contains **35 automated test cases** covering task CRUD, FAQs, errors, health checks, tickets, Groq agent completions, tool calling, and rate limiting.

Run the test suite:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

All 35 tests run against an isolated SQLite test database and mocked external services without mutating development data.

---

## 23. Deployment Instructions

### Option A: Vercel (Serverless Deployment)
1. Push your repository to GitHub (ensure `.env` is ignored).
2. Log in to [vercel.com](https://vercel.com) and click **Add New... $\rightarrow$ Project**.
3. Import your GitHub repository.
4. In **Environment Variables**, add:
   - `GROQ_API_KEY`: Your secret Groq API key (`gsk_...`)
   - `GROQ_MODEL`: `openai/gpt-oss-120b`
   - `SECRET_KEY`: Random 32-character secret key
   - `DB_FALLBACK_SQLITE`: `true`
   - `FLASK_ENV`: `production`
5. Click **Deploy**. Vercel will build and deploy the app using [`vercel.json`](vercel.json).

### Option B: Render / Railway (PaaS Container Deployment)
1. Link your GitHub repository to Render or Railway as a **Web Service**.
2. Set Build Command: `pip install -r requirements.txt`.
3. Set Start Command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --threads 4`.
4. Configure environment variables in the provider dashboard.

---

## 24. Live HTTPS Link
- **Production URL**: `https://<your-project-name>.vercel.app` *(Update with verified deployment URL)*

---

## 25. GitHub Repository Link
- **Repository URL**: `https://github.com/<your-username>/<your-repo-name>` *(Update with verified repository URL)*

---

## 26. Security Considerations
- **Zero Hardcoded Secrets**: All credentials and keys are read exclusively from environment variables.
- **SQL Injection Prevention**: All database queries strictly use parameterized statements (`%s` / `?`). Untrusted user input is never concatenated into SQL.
- **Cross-Site Scripting (XSS) Prevention**: All user-supplied inputs and chatbot messages are escaped with an HTML sanitizer before DOM insertion.
- **Rate Limiting**: Sliding window rate limiter protects endpoints against denial-of-service and brute-force abuse.
- **Input Validation**: Backend strictly validates field lengths, priority enums, email formats, and date formats.

---

## 27. Known Limitations
- **Ephemeral Filesystem on Serverless**: When hosted on Vercel serverless without an external MySQL database, the SQLite dev database in `/tmp` resets between cold starts.
- **Session-Based Conversation Scope**: Chat transcripts are tied to client session IDs and MongoDB; authenticating specific user accounts across devices is planned for the next major release.

---

## 28. Proposed Future Improvement
- **User Authentication and Multi-Tenant Workspaces**:  
  In the next release, integrate user registration and login using `bcrypt` password hashing and JWT (JSON Web Tokens). This will allow users to have password-protected private task dashboards, personal task categories, and isolated multi-tenant support tickets.

---

## 29. Author Information
- **Student Name**: [Student Name]
- **Registration Number**: [Roll Number / Reg No]
- **Department**: Department of Computer Science and Engineering
- **Institution**: Kumaraguru College of Technology
- **Course**: Final Assessment Software Development Project
- **Academic Year**: 2026
