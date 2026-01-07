from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from sqlalchemy.orm import Session
from database.crud import get_messages, add_message
from database.models import SessionLocal
from utils.logger import logger

# In-memory cache for active sessions to reduce DB reads during active chat
# format: {session_id: ChatMessageHistory}
active_sessions = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Factory function to retrieve chat history for a given session ID.
    It first checks the in-memory cache. If not found, it loads from DB.
    """
    if session_id in active_sessions:
        return active_sessions[session_id]

    logger.info(f"Loading history for session: {session_id}")
    history = ChatMessageHistory()
    
    # Load from DB
    db: Session = SessionLocal()
    try:
        messages = get_messages(db, session_id, limit=50) 
        # Note: get_messages returns older first due to saving order, 
        # but we might want to ensure they are added in chronological order.
        
        for msg in messages:
            if msg.sender == 'user':
                history.add_user_message(msg.content)
            else:
                history.add_ai_message(msg.content)
    except Exception as e:
        logger.error(f"Error loading history for {session_id}: {e}")
    finally:
        db.close()

    active_sessions[session_id] = history
    return history

def persist_message(session_id: str, sender: str, content: str):
    """
    Saves a single message to the database.
    This should be called after a successful turn.
    """
    db: Session = SessionLocal()
    try:
        add_message(db, session_id, sender, content)
    except Exception as e:
        logger.error(f"Failed to persist message for {session_id}: {e}")
    finally:
        db.close()
