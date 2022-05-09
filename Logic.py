import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import main
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


def AES_encrypt(message, key, mode):
    plaintext = pad(message, AES.block_size)
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
        return cipher
    else:
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, mode, iv)
        return iv + cipher.encrypt(plaintext)


def AES_decrypt(ciphertext, key, mode):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode, ciphertext[:AES.block_size])
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    else:
        cipher = AES.new(key, mode)
        plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, AES.block_size)

def generate_session_key():
    main.SESSION_KEY = Random.get_random_bytes(AES.block_size)

def send_message(message, mode, client):
    if mode == "CBC":
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, AES.MODE_CBC)
        iv = message_encrypted[:AES.block_size]
        type_mode = "0"
    else:
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, AES.MODE_EBC)
        type_mode = "1"
    current_mess = type_mode + "0"  #for messages not files
    current_mess += "0" #not the last one
    current_mess += message[:BUFFER_SIZE-3]  # get first BUFFER size of message
    message = message[BUFFER_SIZE - 3:]
    if message:  # if message is longer than BUFFER_SIZE - 3
        client.send(current_mess)
        current_mess = "0"
        current_mess += message[:BUFFER_SIZE-1]
        while current_mess:
            message = message[BUFFER_SIZE - 1:]
            if message:
                client.send(current_mess)
                current_mess = "0"
                current_mess += message[:BUFFER_SIZE-1]
            else:
                current_mess[0] = "1"  #the last one
                client.send(current_mess)
                break
    else:
        current_mess[2] = "1"  #the last one
        client.send(current_mess)
            #logic with message sending TODO

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
