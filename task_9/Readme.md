# AI Interview System - Conversation Memory Module (Phase 3)

## Project Overview

The **Conversation Memory Module** acts as the contextual backbone of the AI Interview System. Its primary role is to capture, store, retrieve, and manage interview conversations during active interview sessions.

This module maintains chronological conversation history, including:

- Interview questions
- Candidate responses
- Evaluation scores

By preserving contextual continuity, the system enables downstream AI/LLM components to:

- Generate context-aware follow-up questions
- Prevent repetitive questioning
- Track candidate progression throughout the interview
- Improve automated answer evaluation accuracy

---

# Objectives & Core Deliverables

The primary objective of this Phase 3 assignment was to design and implement a **high-performance conversational memory service** using **FastAPI** and **PostgreSQL**.

The system was engineered to handle real-world backend edge cases through the following mechanisms:

## 1. Chronological Retrieval & Context Truncation

Implemented a sliding window retrieval mechanism using configurable `limit` parameters to:

- Prevent LLM context overflow
- Reduce unnecessary token consumption
- Improve retrieval performance for long interview sessions

---

## 2. Data Deduplication Guardrails

Integrated deterministic **SHA-256 hashing validation** to prevent duplicate conversation records.

Duplicate detection is based on:

```text
session_id + question + answer
```

This ensures database consistency and prevents redundant memory entries.

---

## 3. Strict Payload Integrity Validation

Used **Pydantic validation models** to enforce strict API-level input validation, including:

- Missing field detection
- Empty string validation
- Invalid payload filtering
- Malformed request rejection

Validation occurs before database mutations to maintain data integrity.

---

# Technical Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Testing:** Requests + Custom Performance Scripts
- **Server:** Uvicorn

---

# API Response Structure

Conversation history is returned as structured chronological JSON data:

```json
{
  "history": [
    {
      "question": "What are your thoughts on microservice abstraction?",
      "answer": "Using centralized API routing handles data pipelines efficiently.",
      "score": 8.5
    }
  ]
}
```

This structure allows external AI/LLM modules to directly consume conversation history for prompt generation and contextual evaluation.

---

# Project Structure

```text
system_integration/
├── database.py
├── models.py
├── schemas.py
├── main.py
├── test_performance.py
└── requirements.txt
```

## File Descriptions

| File | Purpose |
|---|---|
| `database.py` | Database engine setup, connection pooling, and session management |
| `models.py` | SQLAlchemy schema definitions |
| `schemas.py` | Pydantic request/response validation models |
| `main.py` | FastAPI routes and core application logic |
| `test_performance.py` | Automated testing and stress validation suite |
| `requirements.txt` | Project dependencies |

---

# Installation & Setup

## Prerequisites

Ensure the following are installed:

- Python 3.10+
- PostgreSQL
- pgAdmin 4

---

## Step 1 — Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 2 — Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary requests pydantic
```

Or install directly from:

```bash
pip install -r requirements.txt
```

---

## Step 3 — Configure Database Connection

Open `database.py` and update the PostgreSQL connection string:

```python
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
```

Example:

```python
DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/interview_memory_db"
```

---

# Running the Application

## Start FastAPI Server

```bash
uvicorn main:app --reload
```

The API will start at:

```text
http://127.0.0.1:8000
```

On startup, SQLAlchemy automatically creates the required database tables and indexes.

---

# API Documentation

FastAPI automatically generates interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running Performance Tests

Keep the FastAPI server running and execute:

```bash
python test_performance.py
```

---

# Validation & Performance Testing

The automated test suite validates multiple backend reliability scenarios.

## Load Testing

- Inserts 25 sequential interview interactions
- Validates connection pooling stability
- Tests transaction handling under rapid requests

---

## Deduplication Testing

- Sends intentionally duplicated payloads
- Verifies SHA-256 duplicate protection
- Ensures API returns `HTTP 409 Conflict`

---

## Sliding Window Verification

- Tests constrained retrieval limits
- Ensures proper chronological truncation
- Prevents oversized response payloads

---

# Key Features

- Context-aware interview memory storage
- Chronological conversation retrieval
- SHA-256 duplicate protection
- Sliding window context management
- Strict payload validation
- PostgreSQL-backed persistence
- FastAPI-powered REST APIs
- Automated performance testing

