import socket
import threading
import sys
from TCP_Message import *
from dataToBytes import *
from SafeMap import *
class fs_tracker():

    def __init__(self, port):
        # added .cc to the name of the tracker because of zone in bind9
        self.name = socket.gethostname() + ".cc"
        self.port = int(port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((socket.gethostbyname(self.name), self.port))
        self.server_socket.listen(5)
        # dict of nodes and files: Key = name file; Value = {node : [chunks]}
        self.nodes = SafeMap()
        # dict of hashes: Key = name file : {chunks : hash}
        self.hashes = SafeMap()

    # handle_storage: handle the storage of files that a node has in the tracker
    def handle_storage(self, _,name_node, payload):
        if not payload:
            return 
        files = payload.split(b'\t')
        for i in range(0, len(files), 3):
            file = files[i].decode('utf-8')
            # assuming that the file is whole, the tracker only needs to know the number of chunks
            chunks = list(range(0,int.from_bytes(files[i+1], byteorder='big')))
            
            # read hashes in hex (40 bytes). The hashes are in order of the chunks
            hashes = files[i+2]
            hashes_list = []
            while (len(hashes) > 0):
                hashes_list.append(hashes[:40])
                hashes = hashes[40:]

            # if the file is not in the tracker, add it to the nodes and hashes dict
            if not self.hashes.exists(file):
                self.hashes.put(file,{})
            if not self.nodes.exists(file):
                self.nodes.put(file,SafeMap())

            # add the hashes to the hashes dict
            dict_files = self.hashes.get(file)
            for chunk, hash in zip(chunks, hashes_list):
                dict_files[chunk] = hash
            
            # add the chunks to the nodes dict
            self.nodes.get(file).put(name_node,chunks)
            print (f"Armazenado {file} do node {name_node} com sucesso")

    # handle_update: handle the update of chunks of a file that a node has in the tracker
    def handle_update(self, _, name_node, payload):
        if not payload:
            return
        file_name, chunks = payload[4:], payload[:4]
        chunk = int.from_bytes(chunks, byteorder='big')
        file_name = file_name.decode('utf-8')
        nodes = self.nodes.get(file_name)
        
        if nodes.exists(name_node):
            nodes.get(name_node).append(chunk)
        else:
            nodes.put(name_node, [chunk])
        print (f"Node {name_node} atualizou o chunk {chunk} do arquivo {file_name}")

    # handle_order: handle the order of a file that a node wants to download
    def handle_order(self, socket_node, _, payload):
        # result is a dict (chunk,[names])
        result = {}
        file = payload.decode('utf-8')

        nodes = self.nodes.get(file)
        if nodes:
            # get the nodes that have the file and divide the chunks between them
            for node, chunks in nodes.get_items():
                for chunk in chunks:
                    if chunk not in result:
                        result[chunk] = [node]
                    else:
                        result[chunk].append(node)
        self.handle_ship(socket_node, result, file)

    # handle_ship: handle the shipping of the nodes that have the chunks of the file
    def handle_ship(self, socket_node, payload, file):
        # if payload is empty, the file was not found
        if not payload:
            socket_node.send(TCP_Message.create_message(SHIP,b''))
            return
        nodes = []
        # transform the dict into a list of bytes that has the format: chunk + names and, in the end, the hashes ordered by chunk
        for chunk, names in payload.items():
            nodes.append(chunk.to_bytes(4, byteorder='big') + arrayStringToBytes(names))
        if nodes:
            nodes.append(b''.join(self.hashes.get(file).values()))
        socket_node.send(TCP_Message.create_message(SHIP, (len(nodes) - 1).to_bytes(4, byteorder="big") + b' '.join(nodes)))

    # close_client: close the connection with the node and remove it from the nodes and hashes dict
    def close_client(self, socket_node, name_node):
        print(f"Node {name_node} desconectado")
        for file_name,nodes in self.nodes.get_items():
            if nodes.exists(name_node):
                nodes.remove(name_node)
            if nodes.isEmpty():
                self.nodes.remove(file_name)
                self.hashes.remove(file_name)
        socket_node.close()

    # handle_client: handle the connection with the node
    def handle_client(self, socket_node, name_node):

        # dict of flags: Key = flag; Value = function to handle the flag
        handle_flags = {
            STORAGE: self.handle_storage,
            UPDATE: self.handle_update,
            ORDER: self.handle_order,
        }

        while True:
            message_type, payload = TCP_Message.receive_message(socket_node)
            # if the message_type is empty, the node disconnected
            if not (payload or message_type):
                break
            handle_flags[message_type](socket_node, name_node, payload)

        self.close_client(socket_node, name_node)

    # start_connections: wait for the connections with the nodes and handle the connections
    def start_connections(self):
        print(f"Servidor ativo em {self.server_socket.getsockname()[0]} porta {self.port}")
        try:
            while True:
                socket_node, address_node = self.server_socket.accept()
                name_node = socket.gethostbyaddr(address_node[0])[0][:-20]
                print(f"O Node {name_node} conectou-se ao servidor")
                # create a thread to handle the connection with the node
                thread_node = threading.Thread(target=self.handle_client, args=(socket_node,name_node,))    
                thread_node.start()
                
        except KeyboardInterrupt:
            print("\nServer disconnected")
            self.server_socket.close()
            sys.exit(0)

if __name__ == "__main__":
    tracker = fs_tracker(sys.argv[1])
    tracker.start_connections()