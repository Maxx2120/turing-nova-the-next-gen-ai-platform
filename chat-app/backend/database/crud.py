from sqlalchemy.orm import Session
from .models import ChatSession, Message
from datetime import datetime
import uuid

def create_chat_session(db: Session, session_id: str = None) -> ChatSession:
    """
    Creates a new chat session. If session_id is provided, it attempts to use it,
    otherwise generates a new UUID.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Check if exists first to be safe, though usually we want new if not specified
    existing = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if existing:
        return existing

    new_session = ChatSession(id=session_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_chat_session(db: Session, session_id: str) -> ChatSession:
    """Retrieves a chat session by ID."""
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()

def add_message(db: Session, session_id: str, sender: str, content: str) -> Message:
    """
    Adds a message to a session. 
    Ensures session exists before adding.
    """
    # Ensure session exists
    session = get_chat_session(db, session_id)
    if not session:
        session = create_chat_session(db, session_id)

    new_message = Message(
        session_id=session_id,
        sender=sender,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_messages(db: Session, session_id: str, limit: int = 50):
    """Retrieves recent messages for a session."""
    return db.query(Message).filter(Message.session_id == session_id)\
            .order_by(Message.timestamp.asc())\
            .limit(limit)\
            .all()
