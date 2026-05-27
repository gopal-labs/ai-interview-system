from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
import datetime
from database import Base

class ConversationMemory(Base):
    __tablename__ = "conversation_memories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    content_hash = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('content_hash', name='uq_conversation_content_hash'),
    )