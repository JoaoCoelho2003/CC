# Define message flags
STORAGE = 0x01
UPDATE = 0x02
ORDER = 0x03
SHIP = 0x04

class TCP_Message:
    # create_message: create a message to send
    def create_message(flag,payload):
        return bytearray([flag]) + len(payload).to_bytes(4, byteorder='big') + payload
    
    # receive_message: receive a message and return the flag and the payload
    def receive_message(socket):
        data = socket.recv(5)
        if not data:
            return None, None
        message_type, length = data[0], data[1:5]
        # transform the length of the payload from bytes to int
        int_length = int.from_bytes(length, byteorder="big")
        payload = b''
        length = 0
        # receive the payload 
        while int_length > length:
            chunk = socket.recv(min(int_length - length, 1024))
            length += len(chunk)
            payload += chunk

        return message_type, payload