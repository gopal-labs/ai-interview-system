# Multi-Threaded Load Balancer Simulator

A modular, concurrent load balancer simulation engine built in Python. Models enterprise-layer traffic distribution across dynamic backend nodes with real-time health monitoring and pluggable scheduling algorithms.

---

## Features

- **Multi-threaded traffic generation** -- spawns 100+ independent client threads to simulate high-concurrency arrivals
- **Three routing algorithms** -- Round Robin, Least Loaded (Least Connections), and Priority-Tiered
- **Async health checker daemon** -- background thread that toggles server health to evaluate automatic failover
- **Thread-safe telemetry** -- `threading.Lock` primitives prevent race conditions across shared server state

---

## Architecture

```
[ JSON Config Input ]
         |
         v
[ Concurrent Clients ] --(100+ threads)-->  [ Load Balancer ] <-- [ Health Checker Daemon ]
                                                    |
                                          (routes via algorithm)
                                           |              |
                                      [ Server-1 ]   [ Server-2 ] ...
```

**Flow:**
1. Parses `config/input.json` to instantiate the server pool
2. Client threads arrive; the load balancer filters unhealthy nodes, applies the chosen algorithm, and assigns work
3. Workers execute simulated network latency outside the sync block for true concurrency, then safely decrement load

---

## Directory Structure

```
load-balancer-simulator/
|
+-- config/
|   +-- input.json          # Simulation parameters
|
+-- src/
|   +-- __init__.py
|   +-- server.py           # Server node data model
|   +-- algorithms.py       # Routing algorithm implementations
|   +-- simulation.py       # Multi-threaded orchestration and background tasks
|
+-- main.py                 # Entry point
```

---

## Getting Started

**Prerequisites:** Python 3.8+

**Clone and configure:**

```bash
git clone https://github.com/your-username/load-balancer-simulator.git
cd load-balancer-simulator
```

Edit `config/input.json`:

```json
{
  "requests": 100,
  "servers": 4,
  "algorithm": "round_robin"
}
```

Supported `algorithm` values: `round_robin`, `least_loaded`, `priority`

**Run:**

```bash
python main.py
```

---

## Sample Output

**Live trace:**

```
Initializing Simulation: 100 requests across 4 servers using round_robin.
[Route] Request 001 -> Server-1 | Live Load: 1/30
[Route] Request 002 -> Server-2 | Live Load: 1/30
[Health Check] Server-3 went OFFLINE!
[Route] Request 003 -> Server-4 | Live Load: 1/30
[Route] Request 004 -> Server-1 | Live Load: 2/30
```

**Final output:**

```json
{
  "processed_requests": 100,
  "healthy_servers": 4
}
```

---

## Concepts Demonstrated

- Thread synchronization with `threading.Lock` and daemon threads
- Dynamic server pool management with automatic failover
- Pluggable algorithm design (easy to extend with new routing strategies)
- Simulated distributed systems behavior without external dependencies
