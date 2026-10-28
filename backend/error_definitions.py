# Error code definitions for TaskMate
# Supports standard HTTP errors and custom DEV001 application error code

ERROR_DEFINITIONS = {
    "400": {
        "code": "400",
        "name": "Bad Request",
        "http_status": 400,
        "meaning": "The server could not understand or process the request due to invalid syntax or missing parameters.",
        "common_causes": [
            "Missing required fields (such as task title or ticket description)",
            "Invalid due date format (must be YYYY-MM-DD)",
            "Payload data exceeding maximum permitted length",
            "Malformed JSON request body"
        ],
        "solutions": [
            "Check that all required fields are filled out properly",
            "Verify the format and type of all submitted inputs",
            "Ensure the request body contains valid JSON"
        ]
    },
    "401": {
        "code": "401",
        "name": "Unauthorized",
        "http_status": 401,
        "meaning": "The request lacks valid authentication credentials for the target resource.",
        "common_causes": [
            "Missing Authorization header or session cookie",
            "Expired or invalidated authentication token",
            "Invalid API key supplied in configuration"
        ],
        "solutions": [
            "Log in or authenticate before retrying the action",
            "Verify your API keys and environment configuration",
            "Refresh your expired credentials or session"
        ]
    },
    "403": {
        "code": "403",
        "name": "Forbidden",
        "http_status": 403,
        "meaning": "The server understood the request, but refuses to authorize it.",
        "common_causes": [
            "Attempting to perform an administrative action without permissions",
            "Accessing a private or restricted endpoint",
            "IP address block or CORS origin violation"
        ],
        "solutions": [
            "Verify your account permissions with the administrator",
            "Check that your client origin matches FRONTEND_ORIGIN",
            "Ensure you are accessing only authorized public endpoints"
        ]
    },
    "404": {
        "code": "404",
        "name": "Not Found",
        "http_status": 404,
        "meaning": "The requested resource, task, ticket, or page could not be located on the server.",
        "common_causes": [
            "Typo or misspelling in the URL path",
            "The requested task ID or ticket code does not exist or was deleted",
            "Outdated bookmark or deprecated route"
        ],
        "solutions": [
            "Double-check the URL path for typing errors",
            "Confirm the task ID or ticket identifier exists",
            "Navigate back to the TaskMate home dashboard"
        ]
    },
    "429": {
        "code": "429",
        "name": "Too Many Requests",
        "http_status": 429,
        "meaning": "The client has exceeded the permitted rate limit of requests within a given timeframe.",
        "common_causes": [
            "Sending rapid automated messages to the AI assistant endpoint",
            "Excessive repetitive task creation or query requests",
            "Bot activity or client-side infinite loop"
        ],
        "solutions": [
            "Wait 30 to 60 seconds before sending another message",
            "Throttle client-side requests and avoid rapid repeated clicks",
            "Use caching for frequent search queries"
        ]
    },
    "500": {
        "code": "500",
        "name": "Internal Server Error",
        "http_status": 500,
        "meaning": "An unexpected server-side condition prevented the request from being fulfilled.",
        "common_causes": [
            "Unhandled runtime exception in backend application logic",
            "Database connection timeout or sudden disconnection",
            "Missing system dependency or configuration file"
        ],
        "solutions": [
            "Check the server console or application log for diagnostic traces",
            "Refresh the page and retry the action after a moment",
            "Submit a support ticket if the issue continues"
        ]
    },
    "503": {
        "code": "503",
        "name": "Service Unavailable",
        "http_status": 503,
        "meaning": "The server is currently unable to handle the request due to temporary maintenance or capacity overload.",
        "common_causes": [
            "Backend server is starting up, restarting, or undergoing maintenance",
            "Downstream dependency (MySQL, MongoDB, or AI service) is unavailable",
            "Excessive concurrent server workload"
        ],
        "solutions": [
            "Check the /health endpoint to view system dependency status",
            "Wait a few moments and reload the page",
            "Contact your hosting provider or system administrator"
        ]
    },
    "DEV001": {
        "code": "DEV001",
        "name": "TaskMate Application Error",
        "http_status": 422,
        "meaning": "A TaskMate-specific application error indicating internal task-processing or application-level business logic failure.",
        "common_causes": [
            "Task state conflict (e.g., trying to reopen an already open task)",
            "Support ticket generation collision or database write failure",
            "Application validation rule mismatch during task update"
        ],
        "solutions": [
            "Refresh your task list to synchronize with current database state",
            "Check that task fields satisfy all application validation constraints",
            "Submit a support ticket referencing error code DEV001"
        ]
    }
}

def get_all_errors():
    """Returns list of all supported error code dictionaries."""
    return list(ERROR_DEFINITIONS.values())

def get_error(code):
    """Retrieves specific error definition by code (e.g. '404' or 'DEV001')."""
    return ERROR_DEFINITIONS.get(str(code).upper())
