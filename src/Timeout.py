import threading
import time
import socket

class TimeOutThread(threading.Thread):
    # TimeOutThread: thread that waits for a timeout to resend a chunk. Extends threading.Thread
    def __init__(self, resend_interval, get_chunk, key, name, ip):
        super(TimeOutThread, self).__init__()
        self.resend_interval = resend_interval
        self.get_chunk = get_chunk
        self.key = key
        self.ip = ip
        self.name = name
        self.stop_event = threading.Event()

    def run(self):
        start_time = time.time()
        # wait for timeout or stop event. If stop event is set means that the chunk was received and the thread can stop
        while time.time() - start_time < self.resend_interval:
            if self.stop_event.is_set():
                return
            time.sleep(0.1)
        # timeout reached, resend chunk
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_socket.bind(('',0))
        self.get_chunk(new_socket ,[self.key], self.name, self.ip)
        return