import time

ORDER = 0x1
DATA = 0x2

PACKET_SIZE = 1024
class UDP_Message:
    # create_message_udp: create a message to send
    def create_message_udp(flag, payload,chunk = 0, timestamp= round(time.time() * 1000)):  
        return bytearray([flag]) + chunk.to_bytes(4, byteorder='big') + timestamp.to_bytes(8, byteorder='big') + payload
    
    # receive_message_udp: receive a message and return the flag, the chunk, the timestamp and the payload
    def receive_message_udp(socket):
        data, ip = socket.recvfrom(1037) # 1024 bytes do chunk + 13 bytes do cabeçalho
        if not data:
            return None, None, None, None, None
        message_type, chunk, timestamp, payload = data[0], data[1:5], data[5:13], data[13:]
        return message_type, int.from_bytes(chunk, byteorder='big'), int.from_bytes(timestamp,byteorder='big'), payload, ip
    
    # send_message: send a message
    def send_message (socket, message, ip):
        socket.sendto(message, ip)

    # send_chunk: send a chunk of a file
    def send_chunk (socket, ip, porta, chunk, payload, timestamp):
        message = UDP_Message.create_message_udp(DATA, payload, chunk, timestamp)
        print(f"Enviando chunk {chunk}")
        UDP_Message.send_message(socket, message, (ip, porta))