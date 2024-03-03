import threading

# SafeMap: class that implements a thread-safe map. Implements most of the methods of a dict with a lock
class SafeMap:
    def __init__(self):
        self.lock = threading.Lock()
        self.map = {}

    def __str__(self):
        with self.lock:
            return str(self.map)

    def put(self, key, value):
        with self.lock:
            self.map[key] = value

    def get(self, key):
        with self.lock:
            return self.map.get(key)

    def remove(self, key):
        with self.lock:
            if key in self.map:
                del self.map[key]

    def get_keys(self):
        with self.lock:
            return list(self.map.keys())

    def get_values(self):
        with self.lock:
            return list(self.map.values())

    def get_items(self):
        with self.lock:
            return list(self.map.items())
        
    def exists(self, key):
        with self.lock:
            return key in self.map
    
    def isEmpty (self):
        with self.lock:
            return len(self.map) == 0