# MASTER PROMPT: BUILD TASKMATE — AI-POWERED TASK MANAGER

## 1. ROLE AND OBJECTIVE

Act as a senior full-stack developer, software architect, UI/UX designer, database engineer, AI integration engineer, QA engineer, and deployment engineer.

Your task is to design, develop, test, and prepare for deployment a complete web application named **TaskMate — AI-Powered Task Manager**.

This is a student software development project for a final assessment. The application must be simple enough to understand and maintain while demonstrating proper full-stack development practices.

The application must include:
- A functional task management system.
- A responsive multi-page website.
- An AI-powered chatbot.
- A frequently asked questions system backed by MySQL.
- An error code guide.
- Custom 404 and 500 error pages.
- A support ticket system.
- MongoDB storage for chat logs and feedback.
- Request logging and a health check endpoint.
- An external API integration with timeout and fallback handling.
- Secure environment variable management.
- Automated tests and deployment documentation.
- A GitHub-ready repository with a complete README.

Do not build an unnecessarily complicated application.

Prioritize working functionality, clean code, simple architecture, responsive design, and reliable error handling.

---

# 2. CRITICAL DEVELOPMENT INSTRUCTIONS

## 2.1 Split the work into independent tasks

Do not attempt to implement the entire application in one step.

First, analyze the requirements and create a detailed implementation plan divided into manageable tasks.

Organize the project into the following phases:

1. Requirements analysis and project planning.
2. Repository inspection and project setup.
3. Frontend design and implementation.
4. Flask backend implementation.
5. MySQL database integration.
6. Task management functionality.
7. FAQ system.
8. Error code system and custom error pages.
9. AI chatbot integration.
10. Support ticket system.
11. MongoDB chat history and feedback integration.
12. Third-party API integration.
13. Logging, monitoring, and health checks.
14. Testing and bug fixing.
15. Security and configuration review.
16. Deployment preparation.
17. README documentation and final assessment verification.

For each phase, create individual tasks with:
- Task ID.
- Task name.
- Objective.
- Required implementation.
- Dependencies.
- Expected files or outputs.
- Acceptance criteria.
- Tests required.
- Status.

Use the following statuses:

- NOT STARTED
- IN PROGRESS
- BLOCKED
- TESTING
- COMPLETED

Maintain a `TASKS.md` file that tracks the status of every task.

## 2.2 Work sequentially and verify every task

Follow this execution procedure:

1. Inspect the existing repository and environment.
2. Understand the existing code before modifying it.
3. Create the task breakdown and implementation plan.
4. Identify dependencies between tasks.
5. Implement the tasks in the appropriate order.
6. Run relevant tests after each significant implementation.
7. Fix any errors before marking a task complete.
8. Update `TASKS.md` after completing each task.
9. Continue to the next task only when its dependencies are satisfied.
10. Perform a complete integration test after all components are implemented.
11. Fix integration problems and repeat the tests.
12. Prepare the final deployment instructions and assessment checklist.

Do not mark a task complete merely because its code has been written.

A task is complete only when its acceptance criteria have been verified.

If a task fails, investigate the root cause, fix it, and rerun the relevant tests.

If an external service or credential is unavailable, implement the appropriate configuration and fallback behavior. Clearly identify anything that requires manual configuration or cannot be tested.

## 2.3 Keep the project simple

Avoid:
- Microservices.
- Kubernetes.
- Complex state management.
- Unnecessary frameworks.
- Complicated AI agent architectures.
- Multiple AI models.
- Unnecessary authentication systems.
- Excessive abstractions.
- Unnecessary infrastructure.

Use a simple monolithic Flask backend and a lightweight frontend.

The application should be easy for a student to explain during a project demonstration.

## 2.4 Do not stop after creating a plan

After creating the plan, begin implementation automatically.

Do not wait for approval between ordinary development phases.

Ask the user only when a decision is genuinely blocking, such as selecting an unavailable AI provider or obtaining required credentials.

Where a reasonable default exists, choose it, document the decision, and continue.

If the environment provides terminal access, browser access, file editing, and testing tools, use them to perform the work rather than merely describing commands.

---

# 3. PROJECT OVERVIEW

## Project Name

TaskMate

## Project Title

AI-Powered Task Manager with Intelligent FAQ and Error Support

## Project Objective

Build a web application that allows users to manage personal tasks while providing an AI assistant that answers frequently asked questions and explains common HTTP errors.

When the assistant cannot answer a question, it should help the user create a support ticket.

The application will demonstrate frontend development, backend APIs, relational database operations, document database operations, AI integration, error handling, logging, testing, and deployment.

## Target Users

Students and individuals who want a simple application for organizing daily tasks.

## Core Features

1. Create tasks.
2. View tasks.
3. Update tasks.
4. Mark tasks as completed.
5. Delete tasks.
6. Filter tasks by status.
7. View FAQs.
8. Search FAQs.
9. Ask questions through an AI chatbot.
10. Understand HTTP error codes.
11. Create support tickets.
12. Submit chatbot feedback.
13. Store chat logs in MongoDB.
14. Check application health.
15. View a programming joke from a third-party API.

---

# 4. TECHNOLOGY STACK

Use the following technologies unless a genuine environment limitation requires a documented alternative.

## Frontend

- HTML5.
- CSS3.
- Vanilla JavaScript.
- Fetch API for communicating with the backend.
- Responsive CSS using Flexbox and Grid.

Do not use React for this version. Keep the frontend lightweight and straightforward.

## Backend

- Python 3.12 or a compatible supported Python version.
- Flask.
- Flask-CORS only if required by the deployment architecture.
- Requests for external HTTP requests.
- Environment variables for configuration.
- Python logging for request and application logs.

## Databases

### MySQL

Use MySQL for:
- Tasks.
- FAQs.
- Support tickets.

### MongoDB

Use MongoDB for:
- Chat conversation logs.
- User feedback.

Use an appropriate MongoDB Python driver, such as PyMongo.

Do not use MongoDB as a replacement for the required MySQL database.

## AI Integration

Use a supported external LLM API, preferably Gemini, to power the chatbot.

Read the API key from an environment variable.

Do not hardcode API keys.

If credentials are unavailable, implement the integration and provide a clearly documented way to configure it. Include a limited FAQ-based fallback so the application remains usable without the external AI service.

Do not claim that a live AI response was tested if no valid credentials were available.

## Third-Party API

Use a public programming-joke API to display a random programming joke.

The API must have:
- A request timeout.
- HTTP status validation.
- Exception handling.
- A fallback joke if the service is unavailable.
- A simple frontend component that displays the result.

Do not make the core task management system depend on this API.

## Deployment

Prepare the application for deployment using:
- A static hosting provider such as Vercel for the frontend, if appropriate.
- A Python-compatible hosting provider such as Render for the Flask backend.
- A managed MySQL database.
- A managed MongoDB service.

Verify the actual deployment platform's requirements before configuring it.

Do not assume that a static frontend host can run the Flask backend directly.

---

# 5. WEBSITE PAGES

Build a website with four primary pages.

Every page must contain the same reusable floating chatbot widget.

## PAGE 1: HOME / TASK DASHBOARD

Suggested route:

`/`

Features:

### Header

Include:
- TaskMate logo.
- Home.
- FAQ.
- Error Guide.
- About.
- AI Assistant button.

The navigation must work on desktop, tablet, and mobile.

### Hero Section

Heading:

"Organize Your Day. Get More Done."

Supporting text:

"TaskMate helps you manage everyday tasks and get instant assistance when you need it."

Include a button that scrolls to the task dashboard.

### Task Dashboard

Display:
- Total tasks.
- Pending tasks.
- Completed tasks.
- Task completion percentage.

### Add Task Form

Fields:
- Task title.
- Optional description.
- Priority: Low, Medium, High.
- Optional due date.

Buttons:
- Add Task.
- Cancel or Clear.

Validation:
- Task title must not be empty.
- Task title must have a reasonable maximum length.
- Due dates must be validated.
- Invalid input must display a helpful message.

### Task List

Each task should display:
- Title.
- Description, if present.
- Priority.
- Due date, if present.
- Completion status.
- Edit button.
- Complete or Reopen button.
- Delete button.

Include filters:
- All.
- Pending.
- Completed.

The dashboard must load and update tasks using Flask API endpoints and MySQL.

Do not implement a frontend-only task list that loses data when the page refreshes.

### Additional Section

Include a small programming joke card.

Fetch the joke from the backend endpoint that integrates the third-party API.

Display the fallback joke when the external API is unavailable.

---

## PAGE 2: FAQ

Suggested route:

`/faq`

Requirements:
- Store at least 10 FAQs in MySQL.
- Retrieve FAQs through the backend.
- Display them on the FAQ page.
- Add a search field.
- Support expanding and collapsing answers.
- Display an appropriate empty state if no matching questions exist.
- Show loading and error states.

Seed the database with at least these questions:

1. What is TaskMate?
2. How do I create a task?
3. How do I edit a task?
4. How do I delete a task?
5. How do I mark a task as completed?
6. Can I reopen a completed task?
7. How do I filter my tasks?
8. What do the task priority levels mean?
9. Where are my tasks stored?
10. What should I do if the website is unavailable?
11. How can I contact support?
12. How does the AI assistant work?

You may add more FAQs.

The FAQ answers must be relevant to the implemented application.

Do not hardcode the entire FAQ collection into the HTML or JavaScript. The displayed FAQs must come from MySQL through the backend API.

---

## PAGE 3: ERROR CODE GUIDE

Suggested route:

`/errors`

Display a searchable list of supported error codes.

Each error entry must contain:
- Error code.
- Error name.
- Meaning.
- Common causes.
- Recommended solutions.
- Ask the Assistant button.

Implement explanations for at least these eight codes:

### HTTP 400 — Bad Request

Explain that the server could not process an invalid request.

### HTTP 401 — Unauthorized

Explain that authentication is required or the supplied credentials are invalid.

### HTTP 403 — Forbidden

Explain that access to the requested resource is denied.

### HTTP 404 — Not Found

Explain that the requested page or resource could not be found.

### HTTP 429 — Too Many Requests

Explain that too many requests were made within a specified period.

### HTTP 500 — Internal Server Error

Explain that an unexpected server-side problem occurred.

### HTTP 503 — Service Unavailable

Explain that the service is temporarily unavailable.

### DEV001 — TaskMate Application Error

Define this as a TaskMate-specific application error.

Explain that the application encountered an internal task-processing or application-level failure.

Make it clear that DEV001 is a custom application code, not a standard HTTP status code.

Provide a short troubleshooting guide for each code.

The chatbot must be able to explain these codes even when the external AI service is unavailable, using the application's locally available error definitions.

---

## PAGE 4: ABOUT / PROJECT INFORMATION

Suggested route:

`/about`

Include:
- Project name.
- Project objective.
- Main features.
- Technologies used.
- Basic architecture overview.
- Developer information.

Do not invent personal information.

Use editable placeholders for the student's name, registration number, department, and college.

Keep this page simple.

The four pages must share the same navigation and chatbot widget.

---

# 6. RESPONSIVE DESIGN REQUIREMENTS

Create a clean, modern, minimal interface.

## Visual Style

Use:
- A light background.
- White cards.
- Dark text.
- One consistent accent color.
- Subtle borders.
- Soft shadows.
- Rounded corners.
- Clear spacing.
- Readable typography.

The interface should look professional without unnecessary animations or visual clutter.

## Responsive Requirements

Desktop:
- Sidebar or top navigation.
- Task dashboard arranged in clear sections.
- Task cards displayed with adequate spacing.

Tablet:
- Flexible grid.
- Adjusted spacing.
- No horizontal overflow.

Mobile:
- Compact navigation.
- Single-column task layout.
- Full-width task form.
- Touch-friendly buttons.
- Chat widget that fits within the viewport.
- Error and FAQ pages that remain readable.

Use a mobile-first approach.

Test at approximate viewport widths of:
- 375px.
- 768px.
- 1024px.
- 1440px.

Do not claim mobile testing was completed unless it was actually performed.

---

# 7. AI CHATBOT

Create a floating chatbot widget that appears on all four pages.

The widget should be implemented as a reusable JavaScript component or shared frontend module.

## Chatbot Interface

Include:
- Floating assistant button.
- Chat window.
- Conversation messages.
- Text input.
- Send button.
- Loading indicator.
- Error state.
- Feedback controls.
- Close button.

The widget must work on desktop and mobile.

## Supported Questions

The assistant must handle:

1. Questions about TaskMate.
2. Questions about task management.
3. Questions answered by the FAQ database.
4. Questions about supported HTTP error codes.
5. Basic troubleshooting questions.

## Assistant Workflow

When the user sends a message:

1. Validate the input.
2. Send the message to the Flask backend.
3. Search the MySQL FAQ database for relevant entries.
4. Check the application's known error code definitions when relevant.
5. Construct a grounded prompt using relevant information.
6. Call the configured AI API when available and appropriate.
7. Return the answer to the frontend.
8. Store the chat message and response in MongoDB.
9. Display the answer in the chat window.
10. Allow the user to provide feedback.

Do not send unnecessary private information to the AI provider.

Do not let the AI invent FAQ entries, error codes, or application features.

The assistant should explain when it does not have enough information.

## AI Grounding

The chatbot should prioritize:
- Retrieved FAQ information.
- Locally defined error code information.
- Documented application functionality.

Use the AI API to formulate helpful responses based on this information.

If no relevant information is found, the assistant may ask a clarifying question.

If it still cannot answer confidently, offer to create a support ticket.

Do not pretend to know an answer merely to avoid creating a ticket.

## Chatbot Fallback

When the external AI API is unavailable:
- Answer recognized error code questions using local definitions.
- Answer FAQ questions using relevant MySQL data.
- Explain that advanced AI assistance is temporarily unavailable.
- Offer support ticket creation for unresolved questions.

The application must not crash because the AI service fails.

## Feedback

Provide simple feedback options:
- Helpful.
- Not helpful.

Store feedback in MongoDB.

Associate feedback with the relevant conversation or response using an appropriate identifier.

---

# 8. SUPPORT TICKET SYSTEM

When the assistant cannot resolve an issue, offer a support ticket.

The chatbot should ask for:
- Issue title.
- Issue description.
- Optional email address.

Do not require an email address.

Validate all fields on the backend.

When the user submits the ticket:

1. Generate a unique ticket identifier.
2. Save the ticket in MySQL.
3. Set the initial status to OPEN.
4. Record the creation timestamp.
5. Return the ticket identifier to the frontend.
6. Display a confirmation message.

Example:

"Your support ticket has been created successfully. Ticket ID: TKT-2026-0001."

The identifier must be generated safely and must not collide with an existing ticket.

The example is illustrative; implement a reliable identifier-generation mechanism.

## Database Fields

Suggested support ticket fields:
- id.
- ticket_code.
- title.
- description.
- email, nullable.
- status.
- created_at.
- updated_at.

Do not expose database stack traces to users.

---

# 9. MYSQL DATABASE

Create a properly structured relational database.

Suggested database name:

`taskmate_db`

## Table 1: tasks

Fields:
- id.
- title.
- description.
- priority.
- due_date.
- is_completed.
- created_at.
- updated_at.

## Table 2: faqs

Fields:
- id.
- question.
- answer.
- category.
- created_at.

## Table 3: support_tickets

Fields:
- id.
- ticket_code.
- title.
- description.
- email.
- status.
- created_at.
- updated_at.

Use appropriate:
- Primary keys.
- Unique constraints.
- Indexes where useful.
- Data types.
- Nullability constraints.
- Foreign keys if required by the chosen schema.

Use parameterized SQL queries.

Never build SQL queries by concatenating untrusted user input.

Provide database initialization scripts and seed data.

The application should have a documented database setup process.

Do not automatically destroy existing user data during startup.

---

# 10. MONGODB DATABASE

Use MongoDB to store chat logs and feedback.

Suggested database name:

`taskmate_logs`

## Collection 1: chat_logs

Store:
- Conversation identifier.
- Message identifier.
- Role.
- Message content.
- Timestamp.
- Optional related support ticket identifier.

Each user message and assistant response should be stored in a way that makes the conversation traceable.

## Collection 2: feedback

Store:
- Feedback identifier.
- Conversation identifier.
- Related message identifier.
- Rating.
- Optional comment.
- Timestamp.

Use an appropriate schema-validation strategy in application code.

Handle MongoDB connection failures gracefully.

If MongoDB is unavailable:
- The task management system must remain functional.
- The FAQ page must remain functional.
- The application must report the logging limitation internally.
- The user must not see database credentials or stack traces.

Document whether chat logging is temporarily unavailable.

Do not silently claim that logs were saved when MongoDB writes failed.

---

# 11. REQUIRED ERROR HANDLING

Implement the required HTTP error codes and custom application error code.

The application must support:
- HTTP 400.
- HTTP 401.
- HTTP 403.
- HTTP 404.
- HTTP 429.
- HTTP 500.
- HTTP 503.
- DEV001.

Do not implement insecure authentication simply to manufacture 401 or 403 errors.

If a route requires no authentication, explain in the README how these error responses are demonstrated through safe test routes or simulated error scenarios.

For HTTP 429, use a reasonable rate-limiting strategy on selected endpoints, particularly the chatbot endpoint.

Avoid excessive complexity.

## Custom 404 Page

Create a dedicated page with:
- A clear "Page Not Found" heading.
- A short explanation.
- A button to return home.
- An "Ask the Assistant" button.
- The shared chatbot widget.

Example message:

"We couldn't find the page you requested. Check the address or ask the TaskMate assistant for help."

The 404 handler must return the correct HTTP status code.

## Custom 500 Page

Create a dedicated error page with:
- A clear "Something Went Wrong" heading.
- A friendly explanation.
- A return-home button.
- An "Ask the Assistant" option.
- The shared chatbot widget.

The 500 handler must return the correct HTTP status code.

Do not display stack traces, file paths, secrets, SQL errors, or internal implementation details.

Log diagnostic information on the server instead.

## Custom Error Code

Define DEV001 as an application-specific error code.

Provide a central location for the definition and explanation.

Document when it should be used.

Do not incorrectly return HTTP status 001. Use a suitable actual HTTP status code and include DEV001 in the structured error response when appropriate.

## Structured Error Responses

Where appropriate, use a consistent JSON structure such as:

{
  "success": false,
  "error": {
    "code": "DEV001",
    "message": "The requested operation could not be completed."
  }
}

The example is illustrative.

Use the correct HTTP status code for the actual failure.

---

# 12. API DESIGN

Create REST-style Flask endpoints.

Use consistent response structures and proper HTTP status codes.

## Task Endpoints

GET `/api/tasks`

Return tasks.

POST `/api/tasks`

Create a task.

GET `/api/tasks/<id>`

Retrieve a single task.

PUT `/api/tasks/<id>`

Update a task.

PATCH `/api/tasks/<id>/complete`

Mark a task as completed.

PATCH `/api/tasks/<id>/reopen`

Reopen a completed task.

DELETE `/api/tasks/<id>`

Delete a task.

Support filtering through query parameters where appropriate.

## FAQ Endpoints

GET `/api/faqs`

Return FAQs from MySQL.

GET `/api/faqs/<id>`

Return a single FAQ.

GET `/api/faqs/search?q=<query>`

Search relevant FAQ questions and answers.

## Chat Endpoints

POST `/api/chat`

Accept a user message, retrieve relevant FAQ and error information, generate a response where possible, and record the conversation in MongoDB.

POST `/api/chat/feedback`

Store chatbot feedback in MongoDB.

## Support Ticket Endpoints

POST `/api/tickets`

Create a support ticket.

GET `/api/tickets/<ticket_code>`

Retrieve a ticket's public status without exposing internal database information.

Only expose information appropriate for the user.

## Error Guide Endpoints

GET `/api/errors`

Return the supported error code definitions.

GET `/api/errors/<code>`

Return information about a specific error code.

The DEV001 code must be included.

## Third-Party API Endpoint

GET `/api/joke`

Return a programming joke.

Use a timeout, validate the response, and return a fallback joke when the external service fails.

## Health Check

GET `/health`

Return a health status and appropriate HTTP status code.

Check the application and its critical dependencies.

Distinguish:
- Application running.
- MySQL connected.
- MongoDB connected.
- AI provider configured or unavailable, where useful.

Do not expose credentials, connection strings, or sensitive diagnostic information.

Use an appropriate response status if a critical dependency prevents the application from performing its core functions.

---

# 13. REQUEST LOGGING

Implement Flask request logging.

Log:
- Timestamp.
- HTTP method.
- Request path.
- Response status code.
- Request duration.
- Unexpected exceptions.

Do not log:
- API keys.
- Database passwords.
- Authentication secrets.
- Full environment variables.
- Sensitive personal information.
- Unnecessary full chat transcripts.

Configure appropriate log levels.

Use a production-compatible logging approach and document how logs can be inspected in the deployment environment.

Avoid excessive console output.

---

# 14. SECURITY REQUIREMENTS

Security is mandatory even for a small student project.

Implement the following:

1. Read secrets from environment variables.
2. Include a `.env.example` file containing placeholders only.
3. Add `.env` to `.gitignore`.
4. Never commit real API keys or database passwords.
5. Use parameterized SQL queries.
6. Validate and limit user input.
7. Handle database errors safely.
8. Avoid exposing Python tracebacks to users.
9. Configure CORS only for the required frontend origins.
10. Add reasonable chatbot request limits.
11. Validate external API responses.
12. Set timeouts for external HTTP requests.
13. Avoid rendering user input as untrusted HTML.
14. Use secure production configuration.
15. Keep dependencies reasonably current and compatible.
16. Do not commit production database exports containing user data.
17. Do not expose support ticket information unnecessarily.
18. Avoid logging sensitive information.

If a security issue is discovered, fix it before deployment.

Do not invent authentication requirements that are not part of this project.

Because the application has no user accounts, clearly document that tasks are not private per-user records and that authentication would be a future improvement.

---

# 15. ENVIRONMENT CONFIGURATION

Create a `.env.example` file.

Include placeholders for configuration such as:

FLASK_ENV=development
SECRET_KEY=replace-with-a-random-secret
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=taskmate_db
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=taskmate_logs
GEMINI_API_KEY=your_ai_api_key
AI_MODEL=your_supported_model_name
FRONTEND_ORIGIN=http://localhost:5500
FLASK_PORT=5000

Adjust the names and values to match the actual implementation.

Do not assume every value is valid without testing it.

Do not commit a real `.env` file.

Ensure that the application starts with a clear error message when a mandatory configuration value is missing.

Optional services should degrade gracefully when possible.

---

# 16. PROJECT STRUCTURE

Use a clean, maintainable project structure similar to:

taskmate/
│
├── frontend/
│   ├── index.html
│   ├── faq.html
│   ├── errors.html
│   ├── about.html
│   ├── 404.html
│   ├── 500.html
│   │
│   ├── css/
│   │   ├── styles.css
│   │   ├── responsive.css
│   │   └── chat.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── tasks.js
│   │   ├── faq.js
│   │   ├── errors.js
│   │   ├── chat.js
│   │   └── api.js
│   │
│   └── assets/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── task_routes.py
│   ├── faq_routes.py
│   ├── chat_routes.py
│   ├── ticket_routes.py
│   ├── error_routes.py
│   ├── ai_service.py
│   ├── logging_config.py
│   ├── error_definitions.py
│   └── requirements.txt
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── tests/
│   ├── test_tasks.py
│   ├── test_faqs.py
│   ├── test_chat.py
│   ├── test_tickets.py
│   ├── test_errors.py
│   └── test_health.py
│
├── .env.example
├── .gitignore
├── TASKS.md
├── README.md
└── requirements.txt

This structure is a starting point, not a rigid requirement.

Adjust it where needed to avoid unnecessary complexity.

Do not create empty files merely to imitate the structure.

Every implemented file must have a clear purpose.

Make sure the actual file paths and deployment configuration agree with the final README.

---

# 17. TESTING STRATEGY

Create automated tests for the major features.

Use pytest for the Flask backend.

## Task Tests

Verify:
- Creating a task.
- Listing tasks.
- Updating a task.
- Completing a task.
- Reopening a task.
- Deleting a task.
- Invalid task input.
- Unknown task identifiers.

## FAQ Tests

Verify:
- Retrieving FAQs.
- Searching FAQs.
- Handling empty search queries.
- Handling unknown FAQ identifiers.
- Ensuring FAQs originate from the database.

## Chatbot Tests

Verify:
- Valid chat requests.
- Empty messages.
- Oversized messages.
- FAQ-based responses.
- Error code explanations.
- AI provider timeout.
- AI provider failure.
- Fallback response.
- Support ticket offer when the answer is unavailable.
- MongoDB logging behavior.

Use mocks for external services where appropriate.

Do not require a paid AI API call for every automated test.

## Support Ticket Tests

Verify:
- Ticket creation.
- Ticket identifier generation.
- Required field validation.
- Optional email handling.
- Ticket retrieval.
- Invalid ticket identifiers.

## Error Handling Tests

Verify:
- HTTP 400.
- HTTP 401.
- HTTP 403.
- HTTP 404.
- HTTP 429.
- HTTP 500.
- HTTP 503.
- DEV001.

Confirm that custom 404 and 500 pages contain an Ask the Assistant option and return the appropriate HTTP status.

## Health Check Tests

Verify:
- Healthy application response.
- MySQL connection failure.
- MongoDB connection failure.
- Missing optional AI configuration.

Test dependency failure behavior without deliberately damaging production services.

## Frontend Tests

Where practical, test:
- Navigation between pages.
- Chat widget initialization on every page.
- Task form validation.
- FAQ search.
- Responsive layout.
- Error page links.
- Chat input behavior.

Use a browser automation tool if one is available.

## Regression Testing

After fixing a bug, rerun the relevant test and any related integration tests.

At the end, run the complete test suite.

Report the actual results.

Never claim all tests passed if tests were not run.

---

# 18. THIRD-PARTY API FAILURE HANDLING

The programming joke API must not interfere with the task management functionality.

Implementation requirements:

1. Request the joke through the Flask backend.
2. Use a finite request timeout.
3. Handle connection errors.
4. Handle HTTP errors.
5. Handle invalid JSON.
6. Validate the required response fields.
7. Return a local fallback joke when the service fails.
8. Log the failure without exposing secrets.
9. Return a usable response to the frontend.

The fallback should be available even when the external service is completely offline.

Document the third-party API used and explain the timeout and fallback behavior in the README.

---

# 19. DEPLOYMENT PREPARATION

Prepare the project for deployment.

## Frontend

Configure the frontend to use the deployed Flask backend through a configurable API base URL.

Do not hardcode localhost URLs in production JavaScript.

## Backend

Prepare the Flask application for production deployment.

Do not use Flask's development server as the production server.

Use an appropriate production WSGI server supported by the chosen hosting platform.

## Databases

Document:
- MySQL database creation.
- Schema initialization.
- FAQ seeding.
- Required network access.
- MongoDB connection configuration.
- Production environment variables.

Do not include production credentials in the repository.

## Deployment Files

Create the configuration files required by the selected hosting platform.

Do not create conflicting or unnecessary deployment configurations for multiple providers.

Choose a practical deployment strategy and document it.

## Deployment Verification

After deployment, verify where possible:
- The HTTPS homepage loads.
- All primary pages load.
- API requests reach the backend.
- FAQs load from MySQL.
- Task operations work.
- The chatbot responds or falls back correctly.
- Support tickets can be created.
- The health check is available.
- The custom 404 page works.
- The mobile layout is usable.

If actual deployment requires the user's account, credentials, or manual approval, complete everything possible beforehand and provide precise remaining steps.

Never invent a live URL or claim deployment succeeded without verifying it.

---

# 20. README REQUIREMENTS

Create a complete README.md.

Include the following sections:

1. Project title.
2. Project overview.
3. Problem statement.
4. Objectives.
5. Features.
6. Technology stack.
7. Application architecture.
8. Project directory structure.
9. Prerequisites.
10. Local installation.
11. Environment variable configuration.
12. MySQL setup.
13. MongoDB setup.
14. Backend startup.
15. Frontend startup.
16. API endpoint documentation.
17. AI assistant workflow.
18. Error code documentation.
19. Support ticket workflow.
20. Third-party API integration.
21. Logging and health check.
22. Testing instructions.
23. Deployment instructions.
24. Live HTTPS link.
25. GitHub repository link.
26. Security considerations.
27. Known limitations.
28. One proposed improvement.
29. Author information.

Use placeholders for the live URL and repository URL until the actual values are known.

After deployment, update the README with the verified live URL.

Include one realistic proposed improvement, such as adding user accounts and private task lists.

Do not claim that features are implemented when they are only planned.

---

# 21. GITHUB READINESS

Ensure that the project can be safely published to GitHub.

Before the final commit or push:

1. Check `.gitignore`.
2. Check for accidental `.env` files.
3. Search for hardcoded credentials.
4. Search for API keys and connection strings.
5. Check for database dumps containing user data.
6. Check for unnecessary generated files.
7. Verify dependency files.
8. Verify README instructions.
9. Verify tests.
10. Ensure the repository contains all necessary source files.

Never push secrets to GitHub.

If a real secret is accidentally committed, do not simply delete it in a later commit. Treat it as compromised and recommend rotating it.

Do not force-push, overwrite unrelated work, or delete existing repository files without understanding their purpose.

If the repository already contains work, preserve it and make changes carefully.

---

# 22. FINAL ACCEPTANCE CHECKLIST

The application is ready for assessment only when the following requirements have been verified.

## Core Application

- [ ] TaskMate homepage works.
- [ ] Users can create tasks.
- [ ] Users can view tasks.
- [ ] Users can update tasks.
- [ ] Users can complete and reopen tasks.
- [ ] Users can delete tasks.
- [ ] Task data persists in MySQL.

## Pages and Design

- [ ] Home page exists.
- [ ] FAQ page exists.
- [ ] Error Guide page exists.
- [ ] About page exists.
- [ ] Navigation works on every page.
- [ ] Chat widget appears on every page.
- [ ] Mobile layout works.
- [ ] No horizontal overflow at the required viewport widths.

## FAQ and AI

- [ ] At least 10 FAQs are stored in MySQL.
- [ ] FAQ data is retrieved through the backend.
- [ ] FAQ search works.
- [ ] The AI assistant answers FAQ-related questions.
- [ ] The AI assistant explains all eight required error codes.
- [ ] The assistant handles unavailable AI services.
- [ ] Unanswered questions lead to a support ticket option.

## Errors

- [ ] HTTP 400 is handled.
- [ ] HTTP 401 is handled.
- [ ] HTTP 403 is handled.
- [ ] HTTP 404 is handled.
- [ ] HTTP 429 is handled.
- [ ] HTTP 500 is handled.
- [ ] HTTP 503 is handled.
- [ ] DEV001 is implemented and documented.
- [ ] The custom 404 page works.
- [ ] The custom 500 page works.
- [ ] Both custom pages provide an Ask the Assistant option.

## Database and Support

- [ ] Support tickets are stored in MySQL.
- [ ] Ticket identifiers are generated reliably.
- [ ] Chat logs are stored in MongoDB when available.
- [ ] Feedback is stored in MongoDB when available.
- [ ] Database failures are handled safely.

## Operations and Security

- [ ] Request logging is implemented.
- [ ] Health check endpoint works.
- [ ] Third-party API has a timeout.
- [ ] Third-party API has a fallback.
- [ ] Secrets are loaded from environment variables.
- [ ] No confidential information is committed to GitHub.
- [ ] Input validation is implemented.
- [ ] Errors do not expose stack traces.

## Delivery

- [ ] Automated tests have been run.
- [ ] Integration tests have been run.
- [ ] README is complete.
- [ ] The application has been deployed over HTTPS, or remaining manual deployment steps are documented.
- [ ] The deployed website has been tested on mobile.
- [ ] An incorrect URL displays the custom 404 page.
- [ ] The README contains the verified live link.
- [ ] The README contains one proposed improvement.
- [ ] The GitHub repository is ready for submission.

---

# 23. FINAL REPORT FROM THE AGENT

After implementation, produce a concise final report containing:

## A. Project Summary

Explain what was built.

## B. Completed Tasks

List the completed tasks from TASKS.md.

## C. Technology Stack

List the technologies actually used.

## D. Database Implementation

Explain the MySQL tables and MongoDB collections.

## E. AI Assistant

Explain how FAQ retrieval, error code explanations, AI responses, fallbacks, and support tickets work.

## F. Testing Results

Report:
- Number of tests run.
- Number of tests passed.
- Number of tests failed.
- Any tests that could not be run.
- Any known limitations.

Use actual results.

## G. Deployment

Provide:
- Verified live HTTPS URL, if deployed.
- GitHub repository URL, if available.
- Health check URL.
- Any remaining deployment steps.

Do not fabricate URLs.

## H. Assessment Requirement Mapping

Provide a table mapping each assessment requirement to:
- Its implementation.
- Relevant files or endpoints.
- Its verification status.

## I. Proposed Improvement

Include one realistic improvement that could be implemented in a future version.

## J. Final Status

Choose one:
- COMPLETE AND VERIFIED.
- IMPLEMENTED WITH KNOWN LIMITATIONS.
- PARTIALLY COMPLETED.
- BLOCKED BY EXTERNAL REQUIREMENTS.

Explain the choice briefly.

---

# 24. BEGIN EXECUTION

Start by inspecting the current workspace and available tools.

Then:

1. Create `TASKS.md` with the complete implementation plan.
2. Identify the current project structure and available dependencies.
3. Establish the project architecture.
4. Begin implementing the tasks in dependency order.
5. Test each significant component.
6. Fix failures before proceeding.
7. Complete integration testing.
8. Prepare deployment.
9. Write the README.
10. Produce the final assessment report.

Work autonomously wherever possible.

Do not merely provide a tutorial, code snippets, or a list of recommendations.

**The objective is to produce a working, tested, maintainable application—not just a project plan.**