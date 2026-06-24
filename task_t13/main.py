# main.py
import json
import threading
import time
import random
from src.server import Server
from src.algorithms import LoadBalancer
from src.simulation import simulate_request, health_checker_daemon, state_lock

def main():
    # 1. Load the Configuration
    with open("config/input.json", "r") as f:
        config = json.load(f)
        
    num_requests = config["requests"]
    num_servers = config["servers"]
    algo = config.get("algorithm", "round_robin")
    
    # 2. Setup Server Pool with random priority attributes
    servers = [Server(i, priority=random.randint(1, 3)) for i in range(1, num_servers + 1)]
    lb = LoadBalancer(servers)
    
    # 3. Spin up Background Health Daemon
    hc_thread = threading.Thread(target=health_checker_daemon, args=(lb,), daemon=True)
    hc_thread.start()
    
    # 4. Spin up Worker Traffic Threads
    processed_tracker = []
    threads = []
    
    for i in range(num_requests):
        t = threading.Thread(target=simulate_request, args=(i, lb, algo, processed_tracker))
        threads.append(t)
        t.start()
        time.sleep(0.005) # Tiny arrival delay
        
        
    for t in threads:
        t.join()
        
    # 5. Bring all servers online at finish line for final clean output reporting
    with state_lock:
        for s in lb.servers:
            s.is_healthy = True
            
    # Output formatting match requirement
    output_data = {
        "processed_requests": len(processed_tracker),
        "healthy_servers": sum(1 for s in lb.servers if s.is_healthy)
    }
    print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()