# TaskMate — AI-Powered Task Manager with Intelligent FAQ and Error Support

A complete, production-ready, full-stack personal task management web application featuring a grounded AI assistant, MySQL relational database, MongoDB chat and feedback logging, centralized error handling, third-party API integration with timeout and fallback, and responsive design.

Developed for final academic software assessment at Kumaraguru College of Technology.

---

## 1. Project Title
**TaskMate — AI-Powered Task Manager with Intelligent FAQ and Error Support**

## 2. Project Overview
TaskMate enables students and professionals to organize daily tasks, set priorities, track due dates, and monitor completion rates. Beyond task tracking, TaskMate integrates an intelligent conversational assistant grounded in the system's MySQL knowledge base and error catalog. When users experience application anomalies or HTTP status errors, the assistant explains the causes and solutions. If an inquiry cannot be resolved automatically, TaskMate seamlessly generates a tracked support ticket.

## 3. Problem Statement
Everyday task management tools often leave users stranded when technical errors, network interruptions, or configuration issues arise. Students and users must navigate confusing error codes without context or support channels. TaskMate solves this by integrating task productivity with contextual, grounded AI troubleshooting, relational knowledge bases, and built-in ticket escalation.

## 4. Objectives
- Deliver a responsive, intuitive task management dashboard with real-time progress metrics.
- Establish a dual-database architecture: MySQL for structured business entities (tasks, FAQs, tickets) and MongoDB for flexible conversational logs and feedback.
- Provide a grounded AI agent backed by Groq API (Llama 3.3) with an automated offline fallback to ensure 100% uptime.
- Implement comprehensive error handling for HTTP 400, 401, 403, 404, 429, 500, 503, and custom code `DEV001`.
- Maintain strict security practices: zero hardcoded secrets, parameterized queries, and defensive timeouts.

## 5. Features
- **Task Management**: Create, read, update, complete, reopen, and delete tasks with priority levels (Low, Medium, High) and due dates.
- **Dynamic Metrics**: Instant calculation of total tasks, pending tasks, completed tasks, and completion percentage.
- **Relational FAQ Engine**: Searchable MySQL-backed knowledge base with animated accordion expand/collapse.
- **Error Code Guide**: Interactive troubleshooting guide for 8 error codes with live simulated API test execution.
- **Grounded AI Assistant & Agent**: Floating chatbot widget embedded across every page, answering questions and taking actions (querying/creating tasks, searching FAQs) using Groq API Llama 3.3.
- **Support Ticket Escalation**: Automatic generation of collision-resistant ticket codes (`TKT-YYYY-XXXX`) stored in MySQL.
- **MongoDB Audit & Feedback**: Conversation logging and helpful/unhelpful rating capture with graceful offline tolerance.
- **External API Safety**: Daily programming joke integration with 3.0s timeout and offline fallback jokes.
- **System Monitoring**: Live `/health` diagnostic endpoint and request logging.
- **Custom Error Pages**: Dedicated, user-friendly 404 and 500 pages with direct "Ask the Assistant" integration.

## 6. Technology Stack
- **Frontend**: Vanilla HTML5, CSS3 (Modern Flexbox/Grid), Vanilla JavaScript (ES6+), SVG Assets.
- **Backend**: Python 3.11+, Flask 3.0, Flask-CORS, PyMySQL, PyMongo, Requests, Python-Dotenv.
- **Databases**:
  - **MySQL 8.0**: Structured relational storage for `tasks`, `faqs`, and `support_tickets`.
  - **MongoDB 7.0**: Document collection storage for `chat_logs` and `feedback`.
  - **SQLite Fallback**: Development driver enabling automated tests and offline evaluation.
- **AI Integration**: Groq API (`llama-3.3-70b-versatile`) with ultra-fast LPU inference, grounding, and offline fallback (Gemini supported as secondary provider).
- **Testing**: Pytest automated test suite (33 tests covering all modules).
- **Production Server**: Waitress (Windows) / Gunicorn (Linux/PaaS).

## 7. Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Viewport                       │
│    (Desktop / Tablet / Mobile - HTML5, CSS3, Vanilla JS)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ REST JSON (fetch)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Monolithic API                     │
│               (Request Logger, CORS, Config)                │
└───┬─────────────┬─────────────┬─────────────┬───────────┬───┘
    │             │             │             │           │
    ▼             ▼             ▼             ▼           ▼
┌───────┐     ┌───────┐     ┌───────┐     ┌───────┐   ┌───────┐
│ Tasks │     │ FAQs  │     │Tickets│     │ Errors│   │ Jokes │
└───┬───┘     └───┬───┘     └───┬───┘     └───┬───┘   └───┬───┘
    │             │             │             │           │
    └──────┬──────┴──────┬──────┘             │       External API
           │             │                    │       (3s timeout)
           ▼             ▼                    ▼
    ┌──────────────┐  ┌───────────┐   ┌────────────────┐
    │ MySQL 8.0    │  │ MongoDB   │   │ Google Gemini  │
    │ (Relational) │  │ (Logs)    │   │ AI Assistant   │
    └──────────────┘  └───────────┘   └────────────────┘
```

## 8. Project Directory Structure
```
Gowry-assignment/
├── backend/
│   ├── __init__.py
│   ├── ai_service.py         # Grounded AI logic, Gemini API & rate limiting
│   ├── app.py                # Flask app factory, static routes, error handlers
│   ├── chat_routes.py        # /api/chat & /api/chat/feedback endpoints
│   ├── config.py             # Environment configuration loader
│   ├── database.py           # MySQL & SQLite connection manager
│   ├── error_definitions.py  # 8 Error code specifications
│   ├── error_routes.py       # /api/errors & simulation endpoints
│   ├── faq_routes.py         # /api/faqs & search endpoints
│   ├── health_routes.py      # /health monitoring endpoint
│   ├── joke_routes.py        # /api/joke endpoint
│   ├── joke_service.py       # Joke API client with timeout & fallback
│   ├── logging_config.py     # Request logging middleware
│   ├── mongo_client.py       # MongoDB chat & feedback logger
│   ├── requirements.txt      # Backend Python dependencies
│   ├── task_routes.py        # /api/tasks CRUD endpoints
│   └── ticket_routes.py      # /api/tickets endpoints
├── database/
│   ├── schema.sql            # MySQL schema definition
│   └── seed.sql              # 12 Initial FAQs & sample tasks
├── frontend/
│   ├── index.html            # Home & Task Dashboard
│   ├── faq.html              # FAQ Knowledge Base & Search
│   ├── errors.html           # Error Guide & Simulator
│   ├── about.html            # About & Student Assessment Details
│   ├── 404.html              # Custom 404 Not Found Page
│   ├── 500.html              # Custom 500 Server Error Page
│   ├── assets/
│   │   └── logo.svg          # TaskMate vector logo
│   ├── css/
│   │   ├── chat.css          # Floating chatbot styles
│   │   ├── responsive.css    # Responsive breakpoints (375px - 1440px)
│   │   └── styles.css        # Base design tokens & components
│   └── js/
│       ├── api.js            # Unified REST client
│       ├── app.js            # Navigation, toast notifications, modals
│       ├── chat.js           # Reusable floating chatbot component
│       ├── errors.js         # Error guide & simulation controller
│       ├── faq.js            # FAQ accordion & search controller
│       └── tasks.js          # Task CRUD, metrics, & joke card
├── tests/
│   ├── conftest.py           # Pytest test fixtures
│   ├── test_chat.py          # Chatbot & rate limiting tests
│   ├── test_errors.py        # Error definition & simulation tests
│   ├── test_faqs.py          # FAQ retrieval & search tests
│   ├── test_health.py        # Health & joke endpoint tests
│   ├── test_tasks.py         # Task CRUD & validation tests
│   └── test_tickets.py       # Ticket generation & retrieval tests
├── .env.example              # Configuration environment template
├── .gitignore                # Git exclusions (secrets, logs, caches)
├── Procfile                  # Production PaaS process definition
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Root Python dependencies
├── TASKS.md                  # Development phase tracking
├── wsgi.py                   # Production WSGI entry point
└── README.md                 # Complete project documentation
```

## 9. Prerequisites
- Python 3.11 or higher
- Git
- MySQL 8.0+ (optional locally; automatic SQLite development driver activates when MySQL is offline)
- MongoDB 7.0+ (optional locally; graceful offline tolerance activates when MongoDB is offline)
- Modern web browser (Chrome, Edge, Firefox, Safari)

## 10. Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/taskmate.git
   cd taskmate
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 11. Environment Variable Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure your environment settings in `.env`:
```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=dev-secret-key-taskmate-assignment-2026

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=taskmate_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password

# Database Fallback (set true to use SQLite if MySQL service is not running locally)
DB_FALLBACK_SQLITE=true
SQLITE_DB_PATH=taskmate_dev.db

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/taskmate_logs
MONGODB_DATABASE=taskmate_logs

# Groq AI Configuration (Ultra-fast LPU inference)
# Get a free API key at: https://console.groq.com/keys
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional Fallback AI Configuration (Gemini API)
GEMINI_API_KEY=your_gemini_api_key_here
AI_MODEL=gemini-1.5-flash

# CORS
FRONTEND_ORIGIN=http://localhost:5500,http://127.0.0.1:5500,http://localhost:5000,http://127.0.0.1:5000

# Chatbot Rate Limiting (Requests per minute per client)
CHAT_RATE_LIMIT=30
```

## 12. MySQL Setup
If running MySQL locally or in the cloud:
1. Log into MySQL:
   ```bash
   mysql -u root -p
   ```
2. Execute the schema script:
   ```sql
   SOURCE database/schema.sql;
   ```
3. Populate initial FAQs and starter tasks:
   ```sql
   SOURCE database/seed.sql;
   ```

## 13. MongoDB Setup
If running MongoDB locally or using MongoDB Atlas:
1. Start the MongoDB daemon (`mongod`) or obtain your Atlas connection string.
2. Set `MONGODB_URI` in `.env`.
3. TaskMate will automatically initialize the `chat_logs` and `feedback` collections upon first interaction.
*(Note: If MongoDB is unavailable, TaskMate logs an internal warning and continues functioning normally without interruption).*

## 14. Backend Startup
Run with Flask development server:
```bash
python backend/app.py
```
Or run with production WSGI server:
```bash
# Windows
python -m waitress --port=5000 backend.app:app

# Linux / Mac
gunicorn wsgi:app --bind 0.0.0.0:5000
```

## 15. Frontend Startup
TaskMate supports two hosting modes:
1. **Monolithic Mode (Recommended)**: The Flask backend serves both the API and frontend pages directly at `http://localhost:5000`. No secondary server needed.
2. **Decoupled Static Mode**: You can open `frontend/index.html` via VS Code Live Server or Python HTTP server on port 5500:
   ```bash
   cd frontend
   python -m http.server 5500
   ```

## 16. API Endpoint Documentation

| Category | Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| **Tasks** | `GET` | `/api/tasks` | List tasks (supports `?status=pending\|completed\|all`) | 200 |
| **Tasks** | `POST` | `/api/tasks` | Create task (`title`, `priority`, optional `due_date`, `description`) | 201 |
| **Tasks** | `GET` | `/api/tasks/<id>` | Retrieve a single task by ID | 200 / 404 |
| **Tasks** | `PUT` | `/api/tasks/<id>` | Update existing task details | 200 / 400 / 404 |
| **Tasks** | `PATCH` | `/api/tasks/<id>/complete` | Mark task as completed | 200 / 404 |
| **Tasks** | `PATCH` | `/api/tasks/<id>/reopen` | Reopen a completed task | 200 / 404 |
| **Tasks** | `DELETE` | `/api/tasks/<id>` | Delete task permanently | 200 / 404 |
| **FAQs** | `GET` | `/api/faqs` | List all FAQs from MySQL | 200 |
| **FAQs** | `GET` | `/api/faqs/<id>` | Get single FAQ by ID | 200 / 404 |
| **FAQs** | `GET` | `/api/faqs/search?q=...` | Search FAQ questions & answers | 200 |
| **Chat** | `POST` | `/api/chat` | Send user message to AI assistant | 200 / 400 / 429 |
| **Chat** | `POST` | `/api/chat/feedback` | Submit response feedback (helpful/not_helpful) | 200 / 400 |
| **Tickets** | `POST` | `/api/tickets` | Create support ticket (`title`, `description`, optional `email`) | 201 / 400 |
| **Tickets** | `GET` | `/api/tickets/<code>` | Retrieve public ticket status | 200 / 404 |
| **Errors** | `GET` | `/api/errors` | List all 8 documented error codes | 200 |
| **Errors** | `GET` | `/api/errors/<code>` | Get definition for specific code | 200 / 404 |
| **Simulations** | `GET` | `/api/errors/test/<code>` | Simulate 400, 401, 403, 404, 429, 500, 503, DEV001 | Corresponding Status |
| **Joke API** | `GET` | `/api/joke` | Programming joke with 3s timeout & fallback | 200 |
| **Health** | `GET` | `/health` | Check application, DB, MongoDB, and AI status | 200 / 503 |

## 17. AI Assistant & Agent Workflow
1. User enters query in floating chatbot widget on any page.
2. Request hits `POST /api/chat`.
3. Client IP checked against sliding window rate limiter (HTTP 429 if > 30 requests/min).
4. System scans MySQL FAQ database, Error Code directory, and live database task summaries for grounding context.
5. Multi-turn conversation history is retrieved from MongoDB / session memory to preserve dialogue context.
6. If `GROQ_API_KEY` is present, the message chain and OpenAI-compatible agent tools (`list_tasks`, `create_task`, `complete_task`, `get_ticket_status`, `search_knowledge_base`) are dispatched to Groq's high-speed LPU API (`llama-3.3-70b-versatile`):
   - **Agent Tool Execution**: If Groq invokes an action (e.g. creating a task or querying pending tasks), the agent executes the function directly against the database and submits the result back to Groq for final natural response formatting.
   - If `GEMINI_API_KEY` is configured instead, Gemini API is called as secondary provider.
7. If the AI API is absent, times out, or encounters errors:
   - Error questions are answered directly from local error definitions.
   - FAQ questions are answered directly from MySQL FAQ records.
   - Task inquiries report live database status.
   - Unresolved inquiries trigger a friendly response offering a Support Ticket (`suggest_ticket: true`).
8. User interaction logged to MongoDB `chat_logs`.
9. User can submit feedback (👍 Helpful / 👎 Not Helpful) logged to MongoDB `feedback`.

## 18. Error Code Documentation

| Code | Name | Meaning | Recommended Resolution |
| :--- | :--- | :--- | :--- |
| **400** | Bad Request | Missing required inputs or invalid due date format | Check input fields and payload format |
| **401** | Unauthorized | Authentication required or credentials invalid | Provide credentials or refresh session |
| **403** | Forbidden | Server refuses authorization | Check endpoint permissions and origins |
| **404** | Not Found | Requested task, ticket, or URL does not exist | Verify URL path or check task ID |
| **429** | Too Many Requests | Rate limit exceeded (>30 queries/min) | Throttle requests; wait 30 seconds |
| **500** | Internal Server Error | Unexpected server runtime exception | Inspect server logs; retry request |
| **503** | Service Unavailable | Service is undergoing maintenance or DB down | Check `/health` endpoint; retry shortly |
| **DEV001** | TaskMate Application Error | Custom application-level business logic failure | Refresh task list; verify constraints |

## 19. Support Ticket Workflow
1. User clicks **🎫 Open Support Ticket** in chatbot widget or navigates from unresolved inquiry.
2. User provides:
   - Issue Title (Required, max 255 chars)
   - Description (Required)
   - Email (Optional, validated format)
3. Backend validates input and generates unique collision-resistant ID (`TKT-YYYY-XXXX`).
4. Ticket saved in MySQL with initial status `OPEN`.
5. Frontend displays confirmation and posts ticket ID in chat for easy reference.
6. User can check ticket status anytime via `GET /api/tickets/<ticket_code>`.

## 20. Third-Party API Integration
- **Service**: Official Joke API (`https://official-joke-api.appspot.com/jokes/programming/random`).
- **Resilience Strategy**:
  - 3.0-second network timeout.
  - HTTP status and JSON structure validation.
  - Curated offline programming jokes fallback pool.
  - Core task operations never depend on external API availability.

## 21. Logging and Health Check
- **Request Logging**: Configured via `backend/logging_config.py`. Every request logs timestamp, method, path, HTTP status, and duration in ms. Sensitive headers, passwords, and API keys are strictly excluded.
- **Health Check**: Accessed via `GET /health`:
  ```json
  {
    "dependencies": {
      "ai_assistant": {
        "critical": false,
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "status": "configured"
      },
      "database": {
        "critical": true,
        "engine": "mysql",
        "status": "connected"
      },
      "mongodb": {
        "critical": false,
        "status": "connected"
      }
    },
    "service": "TaskMate API",
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

## 22. Testing Instructions
Run the automated test suite with pytest:
```bash
python -m pytest -v
```
All 32 tests will run across all modules:
- `tests/test_tasks.py`: 8 tests (CRUD, status toggles, validation, 404s)
- `tests/test_faqs.py`: 5 tests (Listing, search filtering, empty queries, 404s)
- `tests/test_tickets.py`: 5 tests (Generation, validation, retrieval, 404s)
- `tests/test_chat.py`: 8 tests (Grounding, rate limits, ticket escalation, feedback)
- `tests/test_errors.py`: 4 tests (All 8 error codes, simulation routes, custom 404 HTML)
- `tests/test_health.py`: 2 tests (Health status reporting, joke fallback)

## 23. Deployment Instructions
1. **PaaS Hosting (Render / Railway / Heroku)**:
   - Connect GitHub repository.
   - Select Python environment.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`
   - Add environment variables from `.env.example`.
2. **Database Provisioning**:
   - Provision a managed MySQL instance (e.g. Aiven, PlanetScale, Railway MySQL).
   - Run `database/schema.sql` and `database/seed.sql`.
   - Provision MongoDB Atlas free tier cluster.

## 24. Live HTTPS Link
- **Deployment URL**: `[https://taskmate-demo.onrender.com (Placeholder - Ready for PaaS deployment)]`
- **Health Check URL**: `[https://taskmate-demo.onrender.com/health (Placeholder)]`

## 25. GitHub Repository Link
- **Repository**: `[https://github.com/student/taskmate (Placeholder)]`

## 26. Security Considerations
- Zero secrets committed to version control (`.env` added to `.gitignore`).
- 100% Parameterized SQL queries preventing SQL injection.
- Input validation and length bounds on all API endpoints.
- Strict rate limiting on conversational endpoints (HTTP 429).
- Stack traces and internal error paths masked in production JSON responses.
- CORS whitelist restricting cross-origin access to authorized origins.

## 27. Known Limitations
- Single-user / shared task space: Currently, tasks are shared across all visitors because user authentication (JWT / sessions) was omitted to prioritize simple monolithic architecture.
- Gemini API requires valid API key: Without a key, the assistant gracefully uses the grounded FAQ and error fallback engine.

## 28. Proposed Improvement
- **User Authentication and Private Workspaces**: In a future iteration, introduce user registration and login using bcrypt password hashing and JWT (JSON Web Tokens). This will allow users to maintain private task lists, personalized categories, and individual support ticket histories.

## 29. Author Information
- **Student Name**: Gowry S.
- **Roll / Registration Number**: [Registration Number]
- **Department**: Department of Computer Science and Engineering
- **Institution**: Kumaraguru College of Technology, Coimbatore
- **Assessment**: Final Full-Stack Web Development Project Assessment
