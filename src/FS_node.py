import sys
from FS_Track_Protocol import *
from FS_Transfer_Protocol import *
import threading

class fs_node():
    def __init__(self,path, host, port):
        if path[-1] != '/':
            path += '/'
        self.tcp_connection = Node_Connection(host, int(port), path)
        self.udp_connection = Node_Transfer(int(port), path, self.tcp_connection)
    
    # handle_order: handle the order of a file
    def handle_order(self, payload):
        # check if the file already exists
        if payload[0] in os.listdir(self.tcp_connection.path):
            print("Arquivo já existe")
            return
        # send order to tracker	
        chunks_ips, hashes = self.tcp_connection.handle_order(payload[0])
        if chunks_ips:
            # start download of file in udp protocol
            self.udp_connection.set_waitingchunks(hashes)
            self.udp_connection.set_downloading_file(payload[0])
            self.udp_connection.get_file(chunks_ips)

    # handle_quit: handle the quit of the user closing the connections
    def handle_quit(self, _):
        self.tcp_connection.close_connection()
        self.udp_connection.close_connection()
        sys.exit(0)

    # handle_input: handle the input of the user
    def handle_input(self,input):
        inputs = {
            'order' : self.handle_order,
            'quit' : self.handle_quit,
            'q' : self.handle_quit
        }
        command = input.split(' ')
        if (command[0] not in inputs):
            print("Comando inválido")
            return
        inputs[command[0]](command[1:])
    
def main():
    if len(sys.argv) != 4:
        print("Erro nos argumentos: FS_node.py <path> <host> <port>")
    # path = sys.argv[1], host = sys.argv[2], port = sys.argv[3]
    node = fs_node(sys.argv[1],sys.argv[2],sys.argv[3])

    # send name files in the path to tracker
    node.tcp_connection.send_name_files()

    # start udp protocol as a server to receive requests of files
    udpprotocol = threading.Thread(target=node.udp_connection.handle_udp)
    udpprotocol.daemon = True  # Mark as a daemon thread
    udpprotocol.start()
    try:
        while True:
            user_input = input("> ")
            if user_input:
                node.handle_input(user_input)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        node.handle_quit(None)

if __name__ == "__main__":
    main()