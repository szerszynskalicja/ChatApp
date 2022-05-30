import hashlib
import os
import random
import socket
import threading

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import Logic
BUFFER_SIZE = 1024
P = 26
CIPHER_LEN = 128
Q = 6
PLAINTEXT_SIZE = 2


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)
        self.b = random.randint(0, 100)
        self.s = None
        self.password = 'serverpassword'

    def diffie_hellman(self, connection):
        if self.s:
            connection.send(bytes("j", "utf-8"))
            connection.send(self.s)
        else:
            connection.send(bytes("n", "utf-8"))
            self.session_key_exchange(connection)
            self.create_diffie_hellman(connection)
        print(self.s)

    def create_diffie_hellman(self, connection):
        B = (Q ** self.b) % P
        public_key = Logic.get_rsa_keys('./server/othersPublicKey.pem')
        B = B.to_bytes(PLAINTEXT_SIZE, byteorder='big')
        cipher = Logic.RSA_encrypt(B, public_key)
        connection.send(cipher)
        #private_key = Logic.get_rsa_keys('./server/privateKey.pem')
        with open('./server/privateKey.pem', 'rb') as f:
            private_key = f.read()
            hash_pass = hashlib.sha256(bytes(self.password, "utf-8")).digest()
            private_key = Logic.AES_decrypt(private_key, hash_pass, AES.MODE_ECB)
        private_key = RSA.import_key(private_key, passphrase=None)
        A = connection.recv(CIPHER_LEN)
        A = Logic.RSA_decrypt(A, private_key)
        A = int.from_bytes(A, byteorder='big')
        self.s = (A ** self.b) % P
        self.s = self.s.to_bytes(AES.block_size, byteorder='big')

    def handler(self, connection, address):
        print(f"{address} has connected")
        while True:
            data = connection.recv(BUFFER_SIZE)
            print(f"Data received from {address}")
            print(len(data))
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
        if not os.path.isfile('./privateKey.key') and not os.path.isfile('./publicKey.key'):
            Logic.create_keys(self.password, './server/')
        while True:
            connection, address = self.sock.accept()
            self.diffie_hellman(connection)
            connThread = threading.Thread(target=self.handler, args=(connection, address))
            connThread.daemon = True
            connThread.start()
            self.connections.append(connection)

    def session_key_exchange(self, connection):
        with open('server/publicKey.pem', 'rb') as f:
            public_key = f.read()
            public_key = RSA.import_key(public_key)
            connection.send(public_key.exportKey(format='PEM', passphrase=None, pkcs=1))
        other_public_key = RSA.import_key(connection.recv(BUFFER_SIZE), passphrase=None)
        print(other_public_key)
        f = open("server/othersPublicKey.pem", "wb")
        f.write(other_public_key.exportKey(format='PEM'))
        f.close()


server = Server()
server.start()
