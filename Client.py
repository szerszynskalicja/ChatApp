import socket
import threading
from Crypto.Cipher import AES
import Logic
import main
BUFFER_SIZE = 1024

class Client:

    def receive(self):
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            if data[1] == "0":  # message
                if data[0] == "0":
                    type_mode = AES.MODE_CBC
                    iv = data[3:AES.block_size+3]
                    message = iv
                    message += data[AES.block_size+4:BUFFER_SIZE-1]

                elif data[0] == "1":
                    type_mode = AES.MODE_EBC
                    message = data[3:]

                else:
                    print("wrong mode of encryption")
                    break

                if data[2] == "1":  # the last one
                    decrypted_mess = Logic.AES_decrypt(message, main.SESSION_KEY, type_mode)
                else:
                    while True:
                        data = self.sock.recv(BUFFER_SIZE)
                        message += data[1:]
                        if data[0] == "1":
                            break
                    decrypted_mess = Logic.AES_decrypt(message, main.SESSION_KEY, type_mode)

            self.widget.text_box.append("received:" + str(decrypted_mess, 'utf-8'))
            print(str(decrypted_mess, 'utf-8'))
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


