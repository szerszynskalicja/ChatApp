import hashlib
import os
import random
import socket
import threading

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

import Logic
import main

PLAINTEXT_SIZE = 2
CIPHER_LEN = 128
BUFFER_SIZE = 1024
BYTE_ZERO = 48
BYTE_ONE = 49
P = 26
Q = 6


class Client:
    def receive(self):
        while True:
            data = self.sock.recv(BUFFER_SIZE)
            if data[1] == BYTE_ZERO:  # message
                if data[0] == BYTE_ZERO:
                    type_mode = AES.MODE_CBC
                    iv = data[3:AES.block_size + 3]
                    message = iv
                    message += data[AES.block_size + 3:BUFFER_SIZE]
                elif data[0] == BYTE_ONE:
                    type_mode = AES.MODE_ECB
                    message = data[3:]
                else:
                    print("wrong mode of encryption")
                    break
                if data[2] == BYTE_ONE:  # the last one
                    decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode)
                else:
                    while True:
                        data = self.sock.recv(BUFFER_SIZE)
                        message += data[1:]
                        if data[0] == BYTE_ONE:  # the last one
                            break
                    decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode)

                self.widget.text_box.append("received:" + str(decrypted_mess, 'utf-8'))
                print(str(decrypted_mess, 'utf-8'))
            elif data[1] == BYTE_ONE:  # file
                if data[0] == BYTE_ZERO:
                    type_mode = AES.MODE_CBC
                    iv = data[2:AES.block_size + 2]
                    message = iv
                    message += data[AES.block_size + 2:]
                    decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode)
                elif data[0] == BYTE_ONE:
                    type_mode = AES.MODE_ECB
                    message = data[2:]
                    decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode)
                else:
                    print("wrong mode of encryption")
                    break
                f = open(decrypted_mess, 'wb')
                while True:
                    data = self.sock.recv(BUFFER_SIZE)
                    message = data[1:]
                    if type_mode == AES.MODE_ECB:
                        decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode)
                    else:
                        decrypted_mess = Logic.AES_decrypt(message, self.session_key, type_mode, iv)
                    f.write(decrypted_mess)
                    if data[0] == BYTE_ONE:  # the last one
                        break
                f.close()
                self.widget.text_box.append("received: " + str(f.name) + " file")
            else:
                print("wrong type of message")
                break
            if not data:
                break

    def send(self, message):
        self.sock.send(message)

    def __init__(self, password):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.widget = None
        self.a = random.randint(0, 100)
        self.password = password

    def set_widget(self, widget):
        self.widget = widget

    def run(self):
        self.diffie_hellman()
        recThread = threading.Thread(target=self.receive)
        recThread.start()

    def diffie_hellman(self):
        tmp = str(self.sock.recv(1), 'utf-8')
        if tmp[0] == 'j':
            self.session_key = int(str(self.sock.recv(BUFFER_SIZE), 'utf-8'))
            print(self.session_key)
            self.session_key.to_bytes(AES.block_size, byteorder='big')
        elif tmp[0] == 'n':
            self.session_key_exchange()
            A = (Q ** self.a) % P
            public_key = Logic.get_rsa_keys('otherPublicKey.pem')
            A = A.to_bytes(PLAINTEXT_SIZE, byteorder='big')
            cipher = Logic.RSA_encrypt(A, public_key)
            self.send(cipher)
            B = self.sock.recv(CIPHER_LEN)
            #private_key = Logic.get_rsa_keys('privateKey.pem')
            with open('privateKey.pem', 'rb') as f:
                private_key = f.read()
                hash_pass = hashlib.sha256(bytes(self.password, "utf-8")).digest()
                private_key = Logic.AES_decrypt(private_key, hash_pass, AES.MODE_ECB)
            private_key = RSA.import_key(private_key, passphrase=None)
            B = Logic.RSA_decrypt(B, private_key)
            B = int.from_bytes(B, byteorder='big')
            s = (B ** self.a) % P
            print(s)
            self.session_key = s.to_bytes(AES.block_size, byteorder='big')
        print(self.session_key)

    def session_key_exchange(self):
        with open('./publicKey.pem', 'rb') as f:
            public_key = f.read()
            public_key = RSA.import_key(public_key)
            self.send(public_key.exportKey(format='PEM', passphrase=None, pkcs=1))
        other_public_key = RSA.import_key(self.sock.recv(BUFFER_SIZE), passphrase=None)
        print(other_public_key)
        f = open("./otherPublicKey.pem", "wb")
        f.write(other_public_key.exportKey('PEM'))
        f.close()
