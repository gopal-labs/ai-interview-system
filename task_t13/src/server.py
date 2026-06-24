class Server:
    def __init__(self, server_id: int, priority: int = 1):
        self.server_id = f"Server-{server_id}"
        self.is_healthy = True
        self.current_load = 0       
        self.max_capacity = 30      
        self.priority = priority    
        self.total_processed = 0    

    def __repr__(self):
        return f"[{self.server_id} | Healthy: {self.is_healthy} | Load: {self.current_load} | Priority: {self.priority}]"