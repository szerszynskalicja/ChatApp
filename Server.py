import socket
import threading
BUFFER_SIZE = 20


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)


    def handler(self, connection, address):
        print(f"{address} has connected")
        while True:
            data = connection.recv(BUFFER_SIZE)
            print(f"Data received from {address}")
            for c in self.connections:
                if c != connection:
                    c.send(data)
            if not data:
                print(f"{address} has disconnected ")
                self.connections.remove(connection)
                connection.close
                break

    def start(self):
        print('Server is running...')
        while True:
            connection, address = self.sock.accept()
            connThread = threading.Thread(target=self.handler, args=(connection, address))
            connThread.daemon = True
            connThread.start()
            self.connections.append(connection)


server = Server()
server.start()
