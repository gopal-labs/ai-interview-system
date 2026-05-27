import time
import requests

BASE_URL = "http://127.0.0.1:8000" # Update port according to environment configs
TEST_SESSION = "perf-test-session-uuid-100x"

def run_performance_suite():
    print("Initiating Memory Module Test Suite...")
    
    # Test 1: Batch Load Testing 
    print("\n--- Running Load Test (Sequential Entry Processing) ---")
    start_time = time.time()
    for i in range(25):
        payload = {
            "session_id": TEST_SESSION,
            "question": f"What is your architectural vision regarding paradigm archetype {i}?",
            "answer": f"My implementation optimizes paradigm execution via interface structural architecture abstraction {i}.",
            "score": float(i % 10)
        }
        res = requests.post(f"{BASE_URL}/api/memory/store", json=payload)
        assert res.status_code in [200, 201, 409], f"Unexpected code returned: {res.status_code}"
    
    duration = time.time() - start_time
    print(f"Successfully completed sequential write operations in {duration:.4f} seconds.")

    # Test 2: Deduplication Constraint Check
    print("\nRunning Deduplication Isolation Validation")
    duplicate_payload = {
        "session_id": TEST_SESSION,
        "question": "What is your architectural vision regarding paradigm archetype 0?",
        "answer": "My implementation optimizes paradigm execution via interface structural architecture abstraction 0.",
        "score": 0.0
    }
    res = requests.post(f"{BASE_URL}/api/memory/store", json=duplicate_payload)
    if res.status_code == 409:
        print("Core Guardrail Passed: Duplicate payload rejected with HTTP 409 Conflict.")
    else:
        print(f"Core Guardrail Failed: System accepted duplicate entry with code {res.status_code}")

    # Test 3: Sliding Window Truncation Check
    print("\nVerifying Memory Size Constraints & Outputs")
    limit_size = 5
    res = requests.get(f"{BASE_URL}/api/memory/retrieve?session_id={TEST_SESSION}&limit={limit_size}")
    
    assert res.status_code == 200, "History retrieval returned failure codes."
    data = res.json()
    
    print(f"Target history retrieval frame length requested: {limit_size}")
    print(f"Actual parsed response dataset count returned: {len(data['history'])}")
    print(f"Target Formatted Sample Output Validation:\n", data)
    
    if len(data['history']) <= limit_size:
        print("\nVerification Successful: Sliding window bounds enforced cleanly.")

if __name__ == "__main__":
    # Ensure local Uvicorn instance execution is running prior to parsing suite execution
    try:
        run_performance_suite()
    except Exception as e:
        print(f"Test Execution Failure. Verification Engine error details: {e}")