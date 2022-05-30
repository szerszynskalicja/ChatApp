import hashlib
import os
import time

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

import main

BUFFER_SIZE = 1024


def create_keys(password, path):
    hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
    keys = RSA.generate(BUFFER_SIZE)
    public_key = keys.publickey().export_key(format='PEM', passphrase=None, pkcs=1)
    private_key = keys.export_key(format='PEM', passphrase=None, pkcs=1)
    private_key_encrypted = AES_encrypt(private_key, hashed_password, AES.MODE_ECB)

    f = open(f"{path}privateKey.pem", "wb")
    f.write(private_key_encrypted)
    f.close()

    f = open(f"{path}publicKey.pem", "wb")
    f.write(public_key)
    f.close()


def get_rsa_keys(path):
    f = open(f"{path}", "rb")
    key = RSA.import_key(f.read())
    f.close()
    return key


def RSA_decrypt(message, key):
    cipher = PKCS1_OAEP.new(key=key)
    return cipher.decrypt(message)


def RSA_encrypt(message, key):
    cipher = PKCS1_OAEP.new(key=key)
    return cipher.encrypt(message)


def AES_encrypt(message, key, mode, iv=None):
    plaintext = pad(message, AES.block_size)
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
        return cipher.encrypt(plaintext)
    else:
        if iv is None:
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, mode, iv)
            return iv + cipher.encrypt(plaintext)
        else:
            cipher = AES.new(key, mode, iv)
            return cipher.encrypt(plaintext)


def AES_decrypt(ciphertext, key, mode, iv=None):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
        plaintext = cipher.decrypt(ciphertext)
    else:
        if iv is None:
            cipher = AES.new(key, mode, ciphertext[:AES.block_size])
            plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        else:
            cipher = AES.new(key, mode, iv)
            plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, AES.block_size)


def send_file(file_name, mode, client, widget):
    widget.progress_bar_actualization(0)
    name_start = str(file_name).rfind('/')  # find title
    name = str(file_name)[name_start:]
    name = name[1:]
    if mode == "CBC":
        mode_type = AES.MODE_CBC
        current_mess = "01"  # type mode CBC = 0, files =1
        message = bytes(name, 'utf-8')
        message_encrypted = AES_encrypt(message, client.session_key, mode_type)
        iv = message_encrypted[:AES.block_size]
        client.send(bytes(current_mess, 'utf-8') + message_encrypted)
    else:
        mode_type = AES.MODE_ECB
        current_mess = "11"  # type mode ECB = 1, files =1
        message = bytes(name, 'utf-8')
        message_encrypted = AES_encrypt(message, client.session_key, mode_type)
        client.send(bytes(current_mess, 'utf-8') + message_encrypted)
    f = open(file_name, 'rb')
    l = f.read(BUFFER_SIZE - 17)  # substracting 17 because of padding
    filesize = os.stat(file_name).st_size
    steps = filesize // (BUFFER_SIZE - 17) + 1
    step = 1
    while True:
        if mode_type == AES.MODE_CBC:
            encrypt_file = AES_encrypt(l, client.session_key, mode_type, iv)
        else:
            encrypt_file = AES_encrypt(l, client.session_key, mode_type)
        if step == steps:
            mess = bytes("1", 'utf-8') + encrypt_file
            print(len(mess))
            client.send(mess)
            widget.progress_bar_actualization(100)
            break
        else:
            mess = bytes("0", 'utf-8') + encrypt_file
            print(len(mess))
            client.send(mess)
            widget.progress_bar_actualization(round((step / steps) * 100))
        l = f.read(BUFFER_SIZE - 17)
        time.sleep(0.05)  # sleeping is always good for bugs :)
        step += 1
    print('sending finished')
    f.close()


def send_message(message, mode, client, widget):
    widget.progress_bar_actualization(0)
    if mode == "CBC":
        message_encrypted = AES_encrypt(bytes(message, "utf-8"), client.session_key,
                                        AES.MODE_CBC)  # first 16 bytes - vector IV
        type_mode = "0"
    else:
        message_encrypted = AES_encrypt(bytes(message, "utf-8"), client.session_key, AES.MODE_ECB)
        type_mode = "1"
    value, length = progress_bar_value(message_encrypted)
    current_mess = type_mode + "0"  # for messages not files
    if len(message_encrypted) > BUFFER_SIZE - 3:  # message has to be divided
        current_mess += "0"  # not the last one
        mess = bytes(current_mess, 'utf-8')
        mess += message_encrypted[:BUFFER_SIZE - 3]  # get first BUFFER size of message
        message = message_encrypted[BUFFER_SIZE - 3:]
        client.send(mess)
        # wysylanie progress bara
        widget.progress_bar_actualization(value)
        while len(message) >= BUFFER_SIZE:  # > BUFFER_SIZE - 1
            mess = bytes("0", 'utf-8')  # not the last one
            mess += message[:BUFFER_SIZE - 1]
            client.send(mess)
            widget.progress_bar_actualization(value)
            # wysylanie progress bara
            message = message[BUFFER_SIZE - 1:]
        mess = bytes("1", 'utf-8')  # the last one
        mess += message
        client.send(mess)
        # wysylanie progress bara
        widget.progress_bar_actualization(value)
    else:  ### message will be send in one buffer
        current_mess += "1"  # the last one
        mess = bytes(current_mess, 'utf-8')
        mess += message_encrypted
        client.send(mess)
        # wysylanie progress bara
        widget.progress_bar_actualization(value)


def check_password(password):
    hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
    with open('publicKey.pem', mode='rb') as public_file:
        main.PUBLIC_KEY = RSA.import_key(public_file.read())

    with open('privateKey.pem', mode='rb') as private_file:
        try:
            key_data = AES_decrypt(private_file.read(), hashed_password, AES.MODE_CBC)
            main.PRIVATE_KEY = RSA.import_key(key_data)
        except ValueError:
            # if password was wrong then generate random private key
            main.PRIVATE_KEY = RSA.generate(2048).export_key()


def progress_bar_value(message_encrypted):
    length = len(message_encrypted) // BUFFER_SIZE
    if length == 0:
        length = 1
    length = 100 // length
    value = length
    return value, length
