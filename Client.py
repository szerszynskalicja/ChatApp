import socket
import threading
from GUI import Widget


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while True:
            data = self.sock.recv(1024)
            self.widget.text_box.append("received:" + str(data, 'utf-8'))
            print(str(data, 'utf-8'))
            if not data:
                break

    def send(self, message):
        self.sock.send(bytes(message, 'utf-8'))

    def __init__(self, widget):
        self.widget = widget
        self.sock.connect((socket.gethostbyname(socket.gethostname()), 10000))
        recThread = threading.Thread(target=self.receive)
        recThread.start()


