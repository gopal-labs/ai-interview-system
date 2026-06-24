# src/algorithms.py
from src.server import Server

class LoadBalancer:
    def __init__(self, servers: list[Server]):
        self.servers = servers
        self.rr_index = 0  

    def get_healthy_servers(self) -> list[Server]:
        return [s for s in self.servers if s.is_healthy]

    def route_round_robin(self) -> Server:
        healthy_pool = self.get_healthy_servers()
        if not healthy_pool:
            raise RuntimeError("503 Service Unavailable")
        
        self.rr_index = self.rr_index % len(healthy_pool)
        selected_server = healthy_pool[self.rr_index]
        self.rr_index += 1
        return selected_server

    def route_least_loaded(self) -> Server:
        healthy_pool = self.get_healthy_servers()
        if not healthy_pool:
            raise RuntimeError("503 Service Unavailable")
        return min(healthy_pool, key=lambda s: s.current_load)

    def route_priority(self) -> Server:
        healthy_pool = self.get_healthy_servers()
        if not healthy_pool:
            raise RuntimeError("503 Service Unavailable")
        
        available_servers = [s for s in healthy_pool if s.current_load < s.max_capacity]
        if not available_servers:
            raise RuntimeError("504 Gateway Timeout")

        available_servers.sort(key=lambda s: (-s.priority, s.current_load))
        return available_servers