import logging
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from backend.config import Config

logger = logging.getLogger("taskmate.mongodb")

class MongoDBService:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
        self._memory_history = {}  # Fallback in-memory history cache {conversation_id: [{"role": role, "content": content}]}
        self._init_client()

    def _init_client(self):
        try:
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=1500,
                connectTimeoutMS=1500
            )
            # Test connection with ping
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGODB_DATABASE]
            self.is_connected = True
            logger.info(f"Connected to MongoDB database: {Config.MONGODB_DATABASE}")
        except (ServerSelectionTimeoutError, PyMongoError, Exception) as e:
            self.is_connected = False
            self.client = None
            self.db = None
            logger.warning(
                f"MongoDB connection unavailable ({e}). Continuing in graceful offline logging mode."
            )

    def check_connection(self):
        """Checks if MongoDB is actively responding."""
        if not self.is_connected or not self.client:
            # Try to reconnect once
            self._init_client()
        if self.is_connected and self.client:
            try:
                self.client.admin.command('ping')
                return True, "connected"
            except Exception as e:
                self.is_connected = False
                return False, str(e)
        return False, "unavailable"

    def log_chat_message(self, conversation_id, message_id, role, content, ticket_code=None):
        """Stores a chat message in MongoDB and tracks recent turns in local memory."""
        # Always maintain in-memory conversational cache for active session context
        if conversation_id:
            if conversation_id not in self._memory_history:
                self._memory_history[conversation_id] = []
            self._memory_history[conversation_id].append({"role": role, "content": content})
            # Cap memory cache to last 20 messages per session
            if len(self._memory_history[conversation_id]) > 20:
                self._memory_history[conversation_id] = self._memory_history[conversation_id][-20:]

        if not self.is_connected or not self.db:
            logger.debug(f"[Offline Log] Chat ({role}) {conversation_id}: {content[:50]}...")
            return False

        try:
            doc = {
                "conversation_id": conversation_id,
                "message_id": message_id,
                "role": role,
                "content": content,
                "ticket_code": ticket_code,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.db.chat_logs.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to log chat message to MongoDB: {e}")
            return False

    def get_conversation_history(self, conversation_id, limit=6, exclude_last=True):
        """
        Retrieves recent conversation messages for conversational agent context.
        Returns list of {'role': 'user'|'assistant', 'content': str}.
        """
        if not conversation_id:
            return []

        messages = []
        if self.is_connected and self.db is not None:
            try:
                cursor = self.db.chat_logs.find(
                    {"conversation_id": conversation_id}
                ).sort("timestamp", -1).limit(limit + (1 if exclude_last else 0))
                docs = list(cursor)
                docs.reverse()
                messages = [{"role": d.get("role", "user"), "content": str(d.get("content", ""))} for d in docs]
            except Exception as e:
                logger.warning(f"Failed to fetch conversation history from MongoDB: {e}")
                messages = list(self._memory_history.get(conversation_id, []))
        else:
            messages = list(self._memory_history.get(conversation_id, []))

        if exclude_last and messages:
            messages = messages[:-1]

        return messages[-limit:]

    def log_feedback(self, conversation_id, message_id, rating, comment=None):
        """Stores user feedback in the feedback collection if MongoDB is available."""
        if not self.is_connected:
            logger.debug(f"[Offline Log] Feedback for {message_id}: {rating}")
            return False

        try:
            doc = {
                "conversation_id": conversation_id,
                "message_id": message_id,
                "rating": rating,
                "comment": comment,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.db.feedback.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to log feedback to MongoDB: {e}")
            return False

# Global singleton
mongo_service = MongoDBService()
