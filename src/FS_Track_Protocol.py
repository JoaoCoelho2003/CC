import socket
from TCP_Message import *
from UDP_Message import PACKET_SIZE
from dataToBytes import *
from SafeMap import *
import os
import math
import hashlib

class Node_Connection:
    def __init__ (self, name_server, port, path):
        self.name_server = name_server
        self.port = port
        self.path = path
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((socket.gethostbyname(name_server),self.port))
        print(f"Conexão FS Track Protocol com servidor {self.name_server} porta {port}")

    # send_name_files: send the name of files and respective hashes of every chunk in the path to tracker
    def send_name_files(self):
        # get name of files in path
        files = [f for f in os.listdir(self.path) if os.path.isfile(self.path + f)]
        result = b""
        for file_name in files:

            # get hash of file in chunks
            sha1_hashes = []
            # Open file in binary mode and read all the chunks calculating the hash of each one
            with open(self.path + file_name, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    sha1_hash = hashlib.sha1(data)
                    sha1_hashes.append(sha1_hash.hexdigest().encode('utf-8'))

            # Get the size of the file in bytes and calculate the number of chunks
            size = os.path.getsize(self.path + file_name)
            number_of_chunks = math.ceil(size / PACKET_SIZE)

            result += file_name.encode('utf-8') + b'\t' # name of file
            result += number_of_chunks.to_bytes(4, byteorder='big') + b'\t' # number of chunks
            result += b''.join(sha1_hashes) + b'\t' # array of hashes of chunks

        # send the information to tracker
        packet = TCP_Message.create_message(STORAGE, result[:-1])
        self.client_socket.send(packet)

    # update_file: send the update of a chunk of a file to tracker
    def update_file(self, file_name, chunk):
        message = TCP_Message.create_message(UPDATE,chunk.to_bytes(4, byteorder= 'big') + file_name.encode('utf-8'))
        self.client_socket.send(message)

    # handle_order: handle the order of a file
    def handle_order(self, payload):
        # send order to tracker and receive the information of the nodes that have the file
        self.client_socket.send(TCP_Message.create_message(ORDER, payload.encode('utf-8')))
        _ , nodes = TCP_Message.receive_message(self.client_socket)

        if not nodes:
            print(f"Arquivo {payload} não encontrado")
            return None, None

        number_chunks = int.from_bytes(nodes[:4], byteorder="big")

        # the hashes come in the end of the message and have 40 bytes each, the rest is the information of the nodes
        bytes_hashes = -40 * number_chunks
        information = nodes[4:bytes_hashes - 1]
        hashes = nodes[bytes_hashes:]
        
        # transform the hashes in a list of strings
        hashes_list = []
        for i in range(0, len(hashes), 40):
            hashes_list.append(hashes[i:i+40].decode('utf-8'))
        
        # transform the information in a dict of chunks and ips
        chunks_ips = {}
        i = 0
        chunks_read = 0 
        while chunks_read < number_chunks:
            chunk = int.from_bytes(information[i:i + 4], byteorder='big')
            j = i + 4
            while j < len(information) and information[j] != 32:  # 32 is the ASCII code for space
                j += 1
            ips = arrayBytesToString(information[i + 4: j])
            chunks_ips[chunk] = ips
            i = j + 1
            chunks_read += 1
        return chunks_ips, hashes_list
    
    # close_connection: close the connection with tracker
    def close_connection (self):
        self.client_socket.close()