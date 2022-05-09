import socket
import threading


class Client:

    def receive(self):
        while True:
            data = self.sock.recv(1024)
            self.widget.text_box.append("received:" + str(data, 'utf-8'))
            print(str(data, 'utf-8'))
            if not data:
                break

    def send(self, message):
        self.sock.send(bytes(message, 'utf-8'))

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.widget = None

    def set_widget(self, widget):
        self.widget = widget

    def run(self):
        recThread = threading.Thread(target=self.receive)
        recThread.start()


