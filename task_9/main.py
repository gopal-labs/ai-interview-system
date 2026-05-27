from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import hashlib

from database import engine, Base, get_db
from models import ConversationMemory
from schemas import MemoryStoreRequest, MemoryRetrieveResponse

app = FastAPI(title="AI Interview System - Conversation Memory Module")

# Automatically creates tables in your pgAdmin4 database on startup
Base.metadata.create_all(bind=engine)

def generate_content_hash(session_id: str, question: str, answer: str) -> str:
    raw_string = f"{session_id}||{question.strip()}||{answer.strip()}"
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

@app.post("/api/memory/store", status_code=status.HTTP_201_CREATED)
def store_interaction(payload: MemoryStoreRequest, db: Session = Depends(get_db)):
    record_hash = generate_content_hash(payload.session_id, payload.question, payload.answer)
    
    existing_record = db.query(ConversationMemory).filter(ConversationMemory.content_hash == record_hash).first()
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Duplicate entry detected. This specific interaction has already been recorded."
        )
    
    new_memory = ConversationMemory(
        session_id=payload.session_id,
        question=payload.question,
        answer=payload.answer,
        score=payload.score,
        content_hash=record_hash
    )
    
    try:
        db.add(new_memory)
        db.commit()
        db.refresh(new_memory)
        return {"status": "success", "message": "Interaction saved successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database persistent failure: {str(e)}")

@app.get("/api/memory/retrieve", response_model=MemoryRetrieveResponse)
def retrieve_history(
    session_id: str = Query(..., description="The interview context tracking token"),
    limit: int = Query(default=10, ge=1, le=50, description="Sliding window token limit optimization parameter"),
    db: Session = Depends(get_db)
):
    memories = (
        db.query(ConversationMemory)
        .filter(ConversationMemory.session_id == session_id)
        .order_by(ConversationMemory.created_at.desc())
        .limit(limit)
        .all()
    )
    
    chronological_memories = reversed(memories)
    history_list = [
        {"question": item.question, "answer": item.answer, "score": item.score} 
        for item in chronological_memories
    ]
    
    return {"history": history_list}