import socket
import threading

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while True:
            data = self.sock.recv(1024)
            print(str(data, 'utf-8'))
            if not data:
                break

    def send(self, message):
        self.sock.send(bytes(message, 'utf-8'))

    def __init__(self):
        self.sock.connect((socket.gethostbyname(socket.gethostname()), 10000))
        recThread = threading.Thread(target=self.receive)
        recThread.start()

client = Client()
while True:
    mess = input()
    client.send(mess)
