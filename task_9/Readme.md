AI Interview System — Conversation Memory Module (Phase 3)
Project Overview
This module serves as the contextual engine for the AI Interview System. Its primary purpose is to capture, store, and recall past conversational interactions (questions, candidate answers, and evaluation scores) during an active live interview session. By maintaining this chronological context, the system enables the automated Answer Evaluation Module and downstream GPT/LLM engines to make context-aware decisions, prevent question repetition, and assess candidate progression accurately.

My Task
Objectives and Core Deliverables
The core focus of this assignment under Phase 3 was to construct a highly reliable, high-throughput memory storage and retrieval system using FastAPI and a PostgreSQL database backend. The system successfully addresses technical edge cases through three primary mechanisms:

Chronological Retrieval & Context Truncation: Implements a sliding window parameter (limit) that ensures large conversational histories do not overload the LLM context token windows or cause performance bottlenecks during retrieval.

Data Deduplication Guardrails: Features a deterministic SHA-256 content-hashing validation check that prevents identical entries (session_id + question + answer) from creating duplicate database records.

Strict Integrity Verification: Uses validation models to catch missing fields, blank spaces, or unformatted input payloads directly at the API gateway before any database mutations occur.

Technical Architecture & Output Specifications
The API returns history strings cleanly formatted as JSON arrays, ordered chronologically so that external modules can parse the data directly into LLM prompts:

JSON
{
  "history": [
    {
      "question": "What are your thoughts on microservice abstraction?",
      "answer": "Using centralized API routing handles data pipelines efficiently.",
      "score": 8.5
    }
  ]
}
Directory Layout
Plaintext
system_integration/
├── database.py             # Database engine setup, pool configuration, and session maker
├── models.py               # SQLAlchemy schema defining the conversation_memories table
├── schemas.py              # Pydantic data models for payload filtering and validation
├── main.py                 # FastAPI application endpoints and core logical services
├── test_performance.py     # Automated performance stress test and guardrail validation suite
└── requirements.txt        # Isolated virtual environment frozen dependencies
System Configuration and Installation
Prerequisites
Python 3.10 or higher installed.

PostgreSQL server running locally or via a cloud instance.

pgAdmin 4 installed for database monitoring.

Step 1: Virtual Environment Setup
Isolate dependencies by setting up and activating a local virtual environment:

Bash
# Windows
python -m venv venv
venv\Scripts\activate



Bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary requests pydantic
Step 3: Configure Database Connection
Open database.py and modify the connection string with the access credentials extracted from your pgAdmin properties window:

Python
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
Note: For default local setups, this typically points to postgresql://postgres:YOUR_PASSWORD@localhost:5432/YOUR_DATABASE_NAME.

Running the Application
1. Boot up the Live API Server
Run the FastAPI pipeline using the standard Uvicorn web server engine:

Bash
uvicorn main:app --reload
The application will launch successfully on [http://127.0.0.1:8000](http://127.0.0.1:8000). On startup, SQLAlchemy detects your pgAdmin server configuration and automatically creates the conversation_memories data table along with its unique indexing indices.

2. Verify Interactive Documentation
Open your browser and navigate to the endpoint mapping interface to test the routing manually:

Plaintext
http://127.0.0.1:8000/docs
3. Run the Automated Validation Suite
Keep the server running in your first terminal session. Open a separate terminal window, ensure the virtual environment is active, and run the automated performance script:

Bash
python test_performance.py
Verification Logs and Test Performance Metrics
The test script runs a multi-stage validation check to prove that the database layer operates correctly within constraints:

Load Testing (Sequential Entry Processing): Writes 25 continuous interactions rapidly to verify that database transaction connection pooling behaves reliably under heavy loads.

Deduplication Constraint Check: Intentionally fires a matching payload to the server to ensure the system drops the request and throws an HTTP 409 Conflict code instead of polluting tables with duplicates.

Sliding Window Bounds Verification: Requests a constrained data payload limit to prove that historical logs truncate cleanly without throwing memory array errors.