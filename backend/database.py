import logging
import sqlite3
import pymysql
from pymysql.cursors import DictCursor
from backend.config import Config

logger = logging.getLogger("taskmate.database")

class Database:
    def __init__(self):
        self.driver = None  # "mysql" or "sqlite"
        self._detect_driver()

    def _detect_driver(self):
        """Attempts to connect to MySQL; falls back to SQLite if configured."""
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE,
                cursorclass=DictCursor,
                connect_timeout=2
            )
            conn.close()
            self.driver = "mysql"
            logger.info(f"Connected to MySQL on {Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}")
        except Exception as e:
            if Config.DB_FALLBACK_SQLITE:
                self.driver = "sqlite"
                logger.warning(
                    f"MySQL connection failed ({e}). Falling back to SQLite at: {Config.SQLITE_DB_PATH}"
                )
                self._init_sqlite()
            else:
                self.driver = None
                logger.error(f"MySQL connection failed: {e}. SQLite fallback disabled.")

    def _get_connection(self):
        if self.driver == "mysql":
            return pymysql.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE,
                cursorclass=DictCursor,
                autocommit=True
            )
        elif self.driver == "sqlite":
            conn = sqlite3.connect(Config.SQLITE_DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        else:
            raise ConnectionError("No database backend available.")

    def _init_sqlite(self):
        """Initializes tables and seeds default data in SQLite if not already created."""
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT,
                is_completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                email TEXT,
                status TEXT NOT NULL DEFAULT 'OPEN',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check if FAQs already seeded
        cursor.execute("SELECT COUNT(*) FROM faqs")
        count = cursor.fetchone()[0]
        if count == 0:
            default_faqs = [
                ("What is TaskMate?", "TaskMate is an AI-powered personal task management web application designed to help students and professionals organize everyday to-dos, track priorities, and get instant assistance via an integrated chatbot.", "General"),
                ("How do I create a task?", "To create a task, navigate to the Home page dashboard, locate the 'Add New Task' form, enter a task title (required), optional description, select a priority (Low, Medium, High), choose an optional due date, and click the 'Add Task' button.", "Tasks"),
                ("How do I edit a task?", "Find the task card in your dashboard list, click the 'Edit' button, modify the title, description, priority, or due date in the edit modal, and click 'Save Changes'.", "Tasks"),
                ("How do I delete a task?", "Click the 'Delete' button on any task card and confirm the deletion. The task will be permanently removed from the database.", "Tasks"),
                ("How do I mark a task as completed?", "Click the checkmark or 'Complete' button on any pending task card. The task status will update immediately to completed and update your dashboard completion stats.", "Tasks"),
                ("Can I reopen a completed task?", "Yes! On any completed task card, click the 'Reopen' button. The task will return to pending status and recalculate your progress statistics.", "Tasks"),
                ("How do I filter my tasks?", "Use the filter tabs located above the task list: 'All Tasks' displays everything, 'Pending' displays only active tasks, and 'Completed' shows finished items.", "Tasks"),
                ("What do the task priority levels mean?", "TaskMate provides three priority levels: High (urgent and important, highlighted in red), Medium (standard everyday items, highlighted in amber), and Low (minor or flexible tasks, highlighted in green).", "Tasks"),
                ("Where are my tasks stored?", "Your tasks, FAQs, and support tickets are stored reliably in a relational MySQL database (with local development fallback support). Chat conversations and feedback are stored in MongoDB.", "Technical"),
                ("What should I do if the website is unavailable?", "First, check your internet connection. If the issue persists, check the server health endpoint at /health or refer to the Error Guide page for HTTP 500/503 troubleshooting. You can also submit a support ticket.", "Troubleshooting"),
                ("How can I contact support?", "You can open the AI Assistant widget at the bottom-right of any page and request a support ticket, or submit a ticket when the assistant is unable to resolve your inquiry. You will receive a unique ticket ID (e.g., TKT-2026-0001).", "Support"),
                ("How does the AI assistant work?", "The TaskMate AI Assistant is an agent grounded on our MySQL FAQ knowledge base, error code directory, and live tasks. It utilizes Groq API (Llama 3.3) for high-speed reasoning and tool execution, with automatic offline fallback when external AI is unreachable.", "AI Assistant")
            ]
            cursor.executemany("INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)", default_faqs)

            # Sample starter tasks
            sample_tasks = [
                ("Welcome to TaskMate!", "Explore the dashboard, try editing or completing this task, and ask the AI assistant any questions.", "High", None, 0),
                ("Review Final Project Checklist", "Ensure all 17 phases are completed, tested, and ready for evaluation.", "High", None, 0),
                ("Explore Error Code Guide", "Check /errors to learn about HTTP 400, 401, 403, 404, 429, 500, 503, and DEV001.", "Medium", None, 1)
            ]
            cursor.executemany("INSERT INTO tasks (title, description, priority, due_date, is_completed) VALUES (?, ?, ?, ?, ?)", sample_tasks)
            conn.commit()
            logger.info("Seeded initial FAQs and sample tasks into SQLite database.")

        conn.close()

    def _prepare_sql(self, sql):
        """Translates MySQL `%s` placeholders to SQLite `?` placeholders if using SQLite."""
        if self.driver == "sqlite":
            return sql.replace("%s", "?")
        return sql

    def execute_query(self, sql, params=None):
        """Executes INSERT, UPDATE, DELETE queries. Returns (lastrowid, rowcount)."""
        params = params or ()
        sql = self._prepare_sql(sql)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if self.driver == "sqlite":
                conn.commit()
            last_id = cursor.lastrowid
            row_count = cursor.rowcount
            return last_id, row_count
        finally:
            conn.close()

    def fetch_all(self, sql, params=None):
        """Executes SELECT query and returns all rows as list of dicts."""
        params = params or ()
        sql = self._prepare_sql(sql)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if self.driver == "sqlite":
                return [dict(row) for row in rows]
            return rows
        finally:
            conn.close()

    def fetch_one(self, sql, params=None):
        """Executes SELECT query and returns a single row as dict, or None."""
        params = params or ()
        sql = self._prepare_sql(sql)
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            if row and self.driver == "sqlite":
                return dict(row)
            return row
        finally:
            conn.close()

    def check_connection(self):
        """Checks if the relational database is connected and healthy."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            return True, self.driver
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False, str(e)

# Global singleton
db = Database()
