# src/simulation.py
import threading
import time
import random
from src.algorithms import LoadBalancer

state_lock = threading.Lock()

def simulate_request(request_id: int, lb: LoadBalancer, algo_type: str, tracking_list: list):
    try:
        with state_lock:
            # Dynamically match algorithm strings to class methods
            if algo_type == "round_robin":
                server = lb.route_round_robin()
            elif algo_type == "least_loaded":
                server = lb.route_least_loaded()
            elif algo_type == "priority":
                server = lb.route_priority()
            
            server.current_load += 1
            server.total_processed += 1
            print(f"[➔ Route] Request {request_id:03d} -> {server.server_id} | Live Load: {server.current_load}/{server.max_capacity}")
        
        # Simulate computing latency
        time.sleep(random.uniform(0.1, 0.3))
        
        with state_lock:
            server.current_load -= 1
            tracking_list.append(True)
            
    except Exception:
        pass # Drop request gracefully if routing fails due to 503/504 errors

def health_checker_daemon(lb: LoadBalancer):
    while True:
        time.sleep(1.0)
        with state_lock:
            target_server = random.choice(lb.servers)
            target_server.is_healthy = not target_server.is_healthy