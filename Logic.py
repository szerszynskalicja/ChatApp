import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import main

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

def send_message(message, mode):
    if mode == "CBC":
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, AES.MODE_CBC)
        iv = message_encrypted[:AES.block_size]
    else:
        message_encrypted = AES_encrypt(message, main.SESSION_KEY, AES.MODE_EBC)
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
