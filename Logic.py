import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import main
import os
import time
BUFFER_SIZE = 1024

def create_keys(password):
    hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
    keys = RSA.generate(2048)
    public_key = keys.publickey().export_key()
    private_key = keys.export_key()
    private_key_encrypted = AES_encrypt(private_key, hashed_password, AES.MODE_CBC)

    f = open("privateKey.key", "wb")
    f.write(private_key_encrypted)
    f.close()

    f = open("publicKey.key", "wb")
    f.write(public_key)
    f.close()


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

def generate_session_key():
    main.SESSION_KEY = Random.get_random_bytes(AES.block_size)

def send_file(file_name, mode, client):
    name_start = str(file_name).rfind('/')  # find title
    name = str(file_name)[name_start:]
    name = name[1:]
    if mode == "CBC":
        mode_type = AES.MODE_CBC
        current_mess = "01" # type mode CBC = 0, files =1
        message =bytes(name, 'utf-8')
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, mode_type)
        iv = message_encrypted[:AES.block_size]
        client.send(bytes(current_mess, 'utf-8') + message_encrypted)
    else:
        mode_type = AES.MODE_ECB
        current_mess = "11"  # type mode ECB = 1, files =1
        message =bytes(name, 'utf-8')
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, mode_type)
        client.send(bytes(current_mess, 'utf-8') + message_encrypted)
    f = open(file_name, 'rb')
    l = f.read(BUFFER_SIZE-17)  #substracting 17 because of padding
    filesize = os.stat(file_name).st_size
    steps = filesize//(BUFFER_SIZE-17) + 1
    step = 1
    while True:
        if mode_type == AES.MODE_CBC:
            encrypt_file = AES_encrypt(l, main.SESSION_KEY, mode_type, iv)
        else:
            encrypt_file = AES_encrypt(l, main.SESSION_KEY, mode_type)
        if step == steps:
            mess = bytes("1", 'utf-8') + encrypt_file
            print(len(mess))
            client.send(mess)
            break
        else:
            mess = bytes("0", 'utf-8') + encrypt_file
            print(len(mess))
            client.send(mess)
        l = f.read(BUFFER_SIZE-17)
        time.sleep(0.05) #sleeping is always good for bugs :)
        step += 1
    print('sending finished')
    f.close()

def send_message(message, mode, client):
    if mode == "CBC":
        message_encrypted = AES_encrypt(bytes(message, "utf-8"), main.SESSION_KEY, AES.MODE_CBC)
        type_mode = "0"
    else:
        message_encrypted = AES_encrypt(bytes(message, "utf-8"), main.SESSION_KEY, AES.MODE_ECB)
        type_mode = "1"
    current_mess = type_mode + "0"  #for messages not files
    if len(message_encrypted) > BUFFER_SIZE-3:
        current_mess += "0" #not the last one
        mess = bytes(current_mess, 'utf-8')
        mess += message_encrypted[:BUFFER_SIZE-3]  # get first BUFFER size of message
        message = message_encrypted[BUFFER_SIZE-3:]
        client.send(mess)
        while len(message) >= BUFFER_SIZE:  # > BUFFER_SIZE - 1
            mess = bytes("0", 'utf-8')  #not the last one
            mess += message[:BUFFER_SIZE - 1]
            client.send(mess)
            message = message[BUFFER_SIZE - 1:]
        mess = bytes("1", 'utf-8') #the last one
        mess += message
        client.send(mess)
    else:
        current_mess += "1"  #the last one
        mess = bytes(current_mess, 'utf-8')
        mess += message_encrypted
        client.send(mess)

def check_password(password):
    hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
    with open('publicKey.key', mode='rb') as public_file:
        main.PUBLIC_KEY = RSA.import_key(public_file.read())

    with open('privateKey.key', mode='rb') as private_file:
        try:
            key_data = AES_decrypt(private_file.read(), hashed_password, AES.MODE_CBC)
            main.PRIVATE_KEY = RSA.import_key(key_data)
        except ValueError:
            # if password was wrong then generate random private key
            main.PRIVATE_KEY = RSA.generate(2048).export_key()
