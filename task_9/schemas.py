from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class MemoryStoreRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the interview session")
    question: str = Field(..., min_length=1, description="The question asked by the AI")
    answer: str = Field(..., min_length=1, description="The response provided by the candidate")
    score: Optional[float] = Field(None, ge=0, le=10, description="Evaluation score from 0 to 10")

    @field_validator('question', 'answer', 'session_id')
    @classmethod
    def check_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only whitespace.")
        return v.strip()

class MemoryItem(BaseModel):
    question: str
    answer: str
    score: Optional[float]

    class Config:
        from_attributes = True

class MemoryRetrieveResponse(BaseModel):
    history: List[MemoryItem]