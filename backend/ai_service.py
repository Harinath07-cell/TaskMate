import re
import time
import json
import logging
import requests
from backend.config import Config
from backend.database import db
from backend.error_definitions import ERROR_DEFINITIONS
from backend.mongo_client import mongo_service

logger = logging.getLogger("taskmate.ai")

# In-memory rate limiting tracker: {ip_or_session: [timestamps]}
RATE_LIMIT_CACHE = {}

def check_rate_limit(client_id, max_requests=30, window_seconds=60):
    """
    Simple in-memory sliding window rate limiter.
    Returns True if allowed, False if rate limited.
    """
    now = time.time()
    timestamps = RATE_LIMIT_CACHE.get(client_id, [])
    timestamps = [t for t in timestamps if now - t < window_seconds]
    if len(timestamps) >= max_requests:
        RATE_LIMIT_CACHE[client_id] = timestamps
        return False
    timestamps.append(now)
    RATE_LIMIT_CACHE[client_id] = timestamps
    return True

def get_live_task_context():
    """Fetches a concise live summary of tasks from the database for agent context."""
    try:
        stats = db.fetch_one("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN is_completed = 0 THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) as completed
            FROM tasks
        """)
        total = (stats.get("total") or 0) if stats else 0
        pending = (stats.get("pending") or 0) if stats else 0
        completed = (stats.get("completed") or 0) if stats else 0

        pending_tasks = db.fetch_all(
            "SELECT id, title, priority, due_date FROM tasks WHERE is_completed = 0 ORDER BY priority = 'High' DESC, due_date ASC LIMIT 5"
        )
        task_lines = [
            f"- [Task #{t['id']}] {t['title']} (Priority: {t.get('priority', 'Medium')}, Due: {t.get('due_date') or 'None'})"
            for t in pending_tasks
        ]
        context_str = f"Database Task Summary: Total {total} tasks ({pending} pending, {completed} completed)."
        if task_lines:
            context_str += "\nTop Active Tasks:\n" + "\n".join(task_lines)
        return context_str
    except Exception as e:
        logger.debug(f"Unable to retrieve live task context: {e}")
        return ""

# Agent Tool Definitions (OpenAI / Groq API compatible function definitions)
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks from TaskMate database filtered by status (all, pending, or completed).",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by task status: 'all', 'pending', or 'completed'. Default is 'all'."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task in the TaskMate database on behalf of the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title or action of the task (required)."
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional detailed notes or description."
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"],
                        "description": "Priority of the task. Defaults to 'Medium'."
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in YYYY-MM-DD format."
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark an existing task as completed using its numeric task ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The numeric ID of the task to mark completed."
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket_status",
            "description": "Look up the status and details of a support ticket by ticket code (e.g., TKT-2026-ABCD).",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_code": {
                        "type": "string",
                        "description": "The ticket identifier code."
                    }
                },
                "required": ["ticket_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search the FAQ database and Error Code Guide for technical answers or troubleshooting steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords or question to search in the knowledge base."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def execute_list_tasks(status="all"):
    """Tool execution: fetches tasks from database."""
    status_clean = str(status or "all").lower()
    if status_clean == "pending":
        sql = "SELECT id, title, description, priority, due_date, is_completed FROM tasks WHERE is_completed = 0 ORDER BY priority = 'High' DESC, created_at DESC LIMIT 15"
    elif status_clean == "completed":
        sql = "SELECT id, title, description, priority, due_date, is_completed FROM tasks WHERE is_completed = 1 ORDER BY updated_at DESC LIMIT 15"
    else:
        sql = "SELECT id, title, description, priority, due_date, is_completed FROM tasks ORDER BY is_completed ASC, priority = 'High' DESC, created_at DESC LIMIT 15"
    tasks = db.fetch_all(sql)
    for t in tasks:
        t["is_completed"] = bool(t.get("is_completed", 0))
    return {"status_filter": status_clean, "count": len(tasks), "tasks": tasks}

def execute_create_task(title, description=None, priority="Medium", due_date=None):
    """Tool execution: inserts a new task into database."""
    clean_title = str(title).strip()
    if not clean_title:
        return {"error": "Task title is required."}
    clean_prio = str(priority).capitalize() if priority else "Medium"
    if clean_prio not in ("Low", "Medium", "High"):
        clean_prio = "Medium"
    clean_due = str(due_date).strip() if due_date else None

    last_id, _ = db.execute_query(
        "INSERT INTO tasks (title, description, priority, due_date, is_completed) VALUES (%s, %s, %s, %s, 0)",
        (clean_title, description, clean_prio, clean_due)
    )
    return {
        "success": True,
        "task_id": last_id,
        "title": clean_title,
        "priority": clean_prio,
        "due_date": clean_due,
        "message": f"Task #{last_id} '{clean_title}' successfully created."
    }

def execute_complete_task(task_id):
    """Tool execution: marks a task as completed."""
    try:
        t_id = int(task_id)
    except (ValueError, TypeError):
        return {"error": "Invalid task ID"}
    existing = db.fetch_one("SELECT id, title, is_completed FROM tasks WHERE id = %s", (t_id,))
    if not existing:
        return {"error": f"Task with ID {t_id} not found."}
    db.execute_query("UPDATE tasks SET is_completed = 1 WHERE id = %s", (t_id,))
    return {
        "success": True,
        "task_id": t_id,
        "title": existing["title"],
        "message": f"Task #{t_id} '{existing['title']}' has been marked as completed."
    }

def execute_get_ticket_status(ticket_code):
    """Tool execution: looks up a support ticket by code."""
    clean_code = str(ticket_code).strip().upper()
    ticket = db.fetch_one(
        "SELECT ticket_code, title, description, status, created_at, updated_at FROM support_tickets WHERE UPPER(ticket_code) = %s",
        (clean_code,)
    )
    if not ticket:
        return {"found": False, "message": f"No support ticket found with code '{clean_code}'."}
    return {"found": True, "ticket": ticket}

def execute_search_knowledge_base(query):
    """Tool execution: searches FAQs and Error Definitions."""
    faq = AIService.find_matching_faq(query)
    err = AIService.find_matching_error(query)
    found = {}
    if faq:
        found["faq"] = {"question": faq["question"], "answer": faq["answer"], "category": faq.get("category")}
    if err:
        found["error_code"] = {
            "code": err["code"],
            "name": err["name"],
            "meaning": err["meaning"],
            "causes": err["common_causes"],
            "solutions": err["solutions"]
        }
    return found if found else {"message": f"No specific FAQ or error guide match found for query: '{query}'"}

def execute_tool_call(tool_name, arguments_dict):
    """Dispatches tool execution safely with exception handling."""
    try:
        if tool_name == "list_tasks":
            return execute_list_tasks(status=arguments_dict.get("status", "all"))
        elif tool_name == "create_task":
            return execute_create_task(
                title=arguments_dict.get("title", ""),
                description=arguments_dict.get("description"),
                priority=arguments_dict.get("priority", "Medium"),
                due_date=arguments_dict.get("due_date")
            )
        elif tool_name == "complete_task":
            return execute_complete_task(arguments_dict.get("task_id"))
        elif tool_name == "get_ticket_status":
            return execute_get_ticket_status(arguments_dict.get("ticket_code", ""))
        elif tool_name == "search_knowledge_base":
            return execute_search_knowledge_base(arguments_dict.get("query", ""))
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        logger.error(f"Error executing agent tool {tool_name}: {e}")
        return {"error": str(e)}


def safe_groq_post(payload, timeout=Config.GROQ_TIMEOUT):
    """
    Safely executes a POST request to Groq API with SSL resilience and model fallback.
    Returns (response, used_model_name).
    """
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    requested_model = payload.get("model") or Config.GROQ_MODEL
    fallbacks = getattr(Config, "GROQ_FALLBACK_MODELS", ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"])
    models_to_try = [requested_model] + [m for m in fallbacks if m != requested_model]

    last_resp = None
    for model_name in models_to_try:
        body = dict(payload)
        body["model"] = model_name
        try:
            try:
                resp = requests.post(
                    Config.GROQ_API_URL,
                    headers=headers,
                    json=body,
                    timeout=timeout
                )
            except requests.exceptions.SSLError:
                import urllib3
                urllib3.disable_warnings()
                logger.debug("SSL verification failed; retrying Groq request without certificate verification.")
                resp = requests.post(
                    Config.GROQ_API_URL,
                    headers=headers,
                    json=body,
                    timeout=timeout,
                    verify=False
                )

            if resp is not None:
                if resp.status_code == 200:
                    if Config.GROQ_MODEL != model_name:
                        logger.info(f"Groq active model set to: {model_name}")
                        Config.GROQ_MODEL = model_name
                    return resp, model_name
                elif resp.status_code == 404 and "model" in resp.text.lower():
                    logger.info(f"Groq model '{model_name}' not available. Trying candidate fallback...")
                    last_resp = resp
                    continue
                else:
                    return resp, model_name
        except Exception as e:
            logger.warning(f"Error calling Groq with model {model_name}: {e}")

    return last_resp, requested_model


class AIService:
    @staticmethod
    def find_matching_faq(query):
        """Searches MySQL/SQLite FAQs for matching questions or keywords."""
        query_clean = query.strip().lower()
        stopwords = {
            'what', 'when', 'where', 'which', 'your', 'this', 'that', 'have',
            'help', 'need', 'with', 'about', 'some', 'from', 'tell', 'show',
            'please', 'know', 'does', 'make', 'into', 'just', 'more', 'work',
            'like', 'problem', 'issue', 'could', 'would', 'should', 'there',
            'their', 'they', 'them', 'than', 'then', 'also', 'will', 'very',
            'server', 'complex', 'task', 'tasks', 'mark', 'add', 'create', 'update'
        }
        try:
            # 1. Exact full question match or substring
            faqs = db.fetch_all(
                "SELECT id, question, answer, category FROM faqs WHERE LOWER(question) LIKE %s",
                (f"%{query_clean}%",)
            )
            if faqs:
                return faqs[0]

            # 2. Check if query is an FAQ inquiry (starts with question phrases)
            is_faq_query = any(query_clean.startswith(prefix) for prefix in ["what", "how", "where", "can i", "why", "who"])

            # 3. Match multi-keyword intersections (at least two distinctive terms)
            keywords = [w for w in re.findall(r'\b[a-z]{4,}\b', query_clean) if w not in stopwords]
            if len(keywords) >= 2:
                for kw1 in keywords:
                    for kw2 in keywords:
                        if kw1 != kw2:
                            results = db.fetch_all(
                                "SELECT id, question, answer, category FROM faqs WHERE LOWER(question) LIKE %s AND LOWER(question) LIKE %s",
                                (f"%{kw1}%", f"%{kw2}%")
                            )
                            if results:
                                return results[0]

            # 4. If query is specifically an FAQ question inquiry with a distinctive domain term
            if is_faq_query and keywords:
                domain_terms = {'priority', 'reopen', 'filter', 'storage', 'mysql', 'mongo', 'ticket', 'support', 'assistant'}
                matched_terms = [kw for kw in keywords if kw in domain_terms]
                for kw in matched_terms:
                    results = db.fetch_all(
                        "SELECT id, question, answer, category FROM faqs WHERE LOWER(question) LIKE %s",
                        (f"%{kw}%",)
                    )
                    if results:
                        return results[0]
        except Exception as e:
            logger.error(f"Error querying FAQs for AI grounding: {e}")
        return None

    @staticmethod
    def find_matching_error(query):
        """Checks if the query asks about any supported HTTP error code or DEV001."""
        query_upper = query.upper()
        # Check DEV001
        if "DEV001" in query_upper or "DEV-001" in query_upper or "APPLICATION ERROR" in query_upper:
            return ERROR_DEFINITIONS["DEV001"]

        # Check HTTP status codes: 400, 401, 403, 404, 429, 500, 503
        for code in ["400", "401", "403", "404", "429", "500", "503"]:
            pattern = rf"\b{code}\b"
            if re.search(pattern, query) or f"error {code}" in query.lower() or f"http {code}" in query.lower():
                return ERROR_DEFINITIONS[code]

        # Check descriptive error names
        query_lower = query.lower()
        if "bad request" in query_lower:
            return ERROR_DEFINITIONS["400"]
        if "unauthorized" in query_lower:
            return ERROR_DEFINITIONS["401"]
        if "forbidden" in query_lower:
            return ERROR_DEFINITIONS["403"]
        if "not found" in query_lower or "page not found" in query_lower:
            return ERROR_DEFINITIONS["404"]
        if "too many requests" in query_lower or "rate limit" in query_lower:
            return ERROR_DEFINITIONS["429"]
        if "internal server error" in query_lower:
            return ERROR_DEFINITIONS["500"]
        if "service unavailable" in query_lower:
            return ERROR_DEFINITIONS["503"]

        return None

    @classmethod
    def process_message(cls, message, conversation_id=None):
        """
        Processes a user message through the Groq AI Agent, utilizing grounding,
        tool calling, and multi-turn conversation memory, with robust fallback.
        """
        message = message.strip()
        if not message:
            return {
                "response": "Please enter a question or message.",
                "suggest_ticket": False,
                "source": "validation"
            }

        # 1. Retrieve Knowledge Grounding
        matched_faq = cls.find_matching_faq(message)
        matched_error = cls.find_matching_error(message)
        live_task_summary = get_live_task_context()

        context_snippets = []
        if matched_faq:
            context_snippets.append(f"FAQ Match - Q: {matched_faq['question']}\nA: {matched_faq['answer']}")
        if matched_error:
            causes = "; ".join(matched_error['common_causes'])
            solutions = "; ".join(matched_error['solutions'])
            context_snippets.append(
                f"Error Code Match - {matched_error['code']} ({matched_error['name']}): {matched_error['meaning']}. "
                f"Common causes: {causes}. Recommended solutions: {solutions}."
            )
        if live_task_summary:
            context_snippets.append(live_task_summary)

        grounded_context = "\n\n".join(context_snippets)

        system_prompt = (
            "You are TaskMate AI Assistant, an intelligent, helpful, and concise assistant for the TaskMate Task Manager web application.\n"
            "You have direct access to tools to view tasks, create tasks, complete tasks, search the knowledge base, and check support tickets.\n\n"
            "Guidelines:\n"
            "1. Be direct, polite, and concise in your responses.\n"
            "2. When users ask to inspect tasks, create a task, or mark one complete, use the provided tools.\n"
            "3. Ground your explanations in the provided TaskMate Application Context.\n"
            "4. Never invent fake error codes, fake features, or non-existent authentication mechanisms.\n"
            "5. If a technical issue cannot be resolved, politely advise the user to submit a support ticket.\n\n"
            f"Grounded Application Context:\n{grounded_context if grounded_context else 'No direct FAQ or Error code matched.'}"
        )

        # 2. Build Groq / LLM Message Chain with History
        messages = [{"role": "system", "content": system_prompt}]

        if conversation_id:
            try:
                history = mongo_service.get_conversation_history(conversation_id, limit=6, exclude_last=True)
                for item in history:
                    r = item.get("role", "user")
                    c = str(item.get("content", "")).strip()
                    if c and r in ("user", "assistant"):
                        messages.append({"role": r, "content": c})
            except Exception as e:
                logger.debug(f"Could not load conversation history: {e}")

        messages.append({"role": "user", "content": message})

        # 3. Primary Agent Provider: Groq API
        if Config.GROQ_API_KEY:
            try:
                payload = {
                    "model": Config.GROQ_MODEL,
                    "messages": messages,
                    "tools": AGENT_TOOLS,
                    "tool_choice": "auto",
                    "temperature": 0.2,
                    "max_tokens": 600
                }
                resp, used_model = safe_groq_post(payload, timeout=Config.GROQ_TIMEOUT)

                if resp is not None and resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        msg_obj = choices[0].get("message", {})
                        tool_calls = msg_obj.get("tool_calls")

                        # Handle Tool Calls if Groq invoked any functions
                        if tool_calls:
                            logger.info(f"Groq agent invoked {len(tool_calls)} tool call(s) with model {used_model}. Executing...")
                            # Clean assistant message conforming strictly to OpenAI/Groq tool call protocol
                            messages.append({
                                "role": "assistant",
                                "content": msg_obj.get("content") or "",
                                "tool_calls": tool_calls
                            })

                            for tc in tool_calls:
                                fn_name = tc.get("function", {}).get("name", "")
                                fn_args_raw = tc.get("function", {}).get("arguments", "{}")
                                try:
                                    fn_args = json.loads(fn_args_raw) if isinstance(fn_args_raw, str) else fn_args_raw
                                except Exception:
                                    fn_args = {}
                                tool_result = execute_tool_call(fn_name, fn_args)
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tc.get("id", f"call_{fn_name}"),
                                    "name": fn_name,
                                    "content": json.dumps(tool_result)
                                })

                            # Follow-up request to Groq for natural response incorporating tool output
                            follow_up_payload = {
                                "model": used_model,
                                "messages": messages,
                                "temperature": 0.2,
                                "max_tokens": 500
                            }
                            follow_resp, _ = safe_groq_post(follow_up_payload, timeout=Config.GROQ_TIMEOUT)
                            if follow_resp is not None and follow_resp.status_code == 200:
                                follow_data = follow_resp.json()
                                follow_choices = follow_data.get("choices", [])
                                if follow_choices:
                                    final_text = follow_choices[0].get("message", {}).get("content", "").strip()
                                    if final_text:
                                        return {
                                            "response": final_text,
                                            "suggest_ticket": "support ticket" in final_text.lower() or "submit a ticket" in final_text.lower(),
                                            "source": "groq"
                                        }

                        # Standard conversational text response (no tool calls)
                        text = msg_obj.get("content", "").strip()
                        if text:
                            return {
                                "response": text,
                                "suggest_ticket": "support ticket" in text.lower() or "submit a ticket" in text.lower(),
                                "source": "groq"
                            }

                status_code = resp.status_code if resp is not None else "No response"
                err_text = resp.text[:200] if resp is not None else "Timeout / Network error"
                logger.warning(f"Groq API returned {status_code}: {err_text}. Proceeding with fallback.")
            except Exception as e:
                logger.warning(f"Groq API agent invocation failed ({e}). Proceeding with grounded fallback.")

        # 4. Secondary Provider: Gemini API (if GEMINI_API_KEY is configured and Groq is not/failed)
        elif Config.GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.AI_MODEL}:generateContent?key={Config.GEMINI_API_KEY}"
                payload = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {"text": f"{system_prompt}\n\nUser Question: {message}"}
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.2,
                        "maxOutputTokens": 300
                    }
                }
                resp = requests.post(url, json=payload, timeout=5.0)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                        if text:
                            return {
                                "response": text,
                                "suggest_ticket": "support ticket" in text.lower() or "submit a ticket" in text.lower(),
                                "source": "gemini"
                            }
                logger.warning(f"Gemini API returned status {resp.status_code}. Using fallback.")
            except Exception as e:
                logger.warning(f"Gemini API invocation failed ({e}). Proceeding with grounded fallback.")

        # 5. Grounded Offline Fallback Engine (when external AI providers are offline or not configured)
        if matched_error:
            resp_text = (
                f"**Error {matched_error['code']} — {matched_error['name']}**\n\n"
                f"{matched_error['meaning']}\n\n"
                f"**Common Causes:**\n- " + "\n- ".join(matched_error['common_causes']) + "\n\n"
                f"**Recommended Solutions:**\n- " + "\n- ".join(matched_error['solutions'])
            )
            return {
                "response": resp_text,
                "suggest_ticket": False,
                "source": "local_error_guide"
            }

        if matched_faq:
            return {
                "response": f"**{matched_faq['question']}**\n\n{matched_faq['answer']}",
                "suggest_ticket": False,
                "source": "local_faq"
            }

        # Check general greetings
        if re.fullmatch(r'\s*(hi|hello|hey|greetings|help|hi there|hello there)\s*[!.]*\s*', message.lower()):
            return {
                "response": "Hello! I am your TaskMate AI Assistant. You can ask me how to manage tasks, explore FAQs, or learn about HTTP error codes like 400, 404, 500, or custom DEV001. How can I help you today?",
                "suggest_ticket": False,
                "source": "local_greeter"
            }

        # Task query fallback if user mentions tasks while offline
        if any(term in message.lower() for term in ["my task", "list task", "pending task", "show task", "all tasks"]):
            if live_task_summary:
                return {
                    "response": f"Here is your current task status:\n\n{live_task_summary}",
                    "suggest_ticket": False,
                    "source": "local_task_status"
                }

        # Unresolved question fallback: Offer Support Ticket
        return {
            "response": (
                "I couldn't find an exact answer in our knowledge base. "
                "Would you like me to help you create a support ticket so our team can assist you further?"
            ),
            "suggest_ticket": True,
            "source": "fallback_ticket_offer"
        }
