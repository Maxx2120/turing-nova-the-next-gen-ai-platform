from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database Definitions
DATABASE_URL = "sqlite:///./chat.db"

Base = declarative_base()

class ChatSession(Base):
    """
    Represents a conversation session.
    """
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True) # UUID
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String, default="New Conversation") 
    
    # Relationship to messages
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    """
    Represents an individual message in a chat session.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    sender = Column(String) # 'user' or 'bot'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship back to session
    session = relationship("ChatSession", back_populates="messages")

# Database Setup Helper
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database tables."""
    Base.metadata.create_all(bind=engine)
