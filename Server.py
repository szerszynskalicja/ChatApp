import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def create_keys(password):
    hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
    keys = RSA.generate(2048)
    public_key = keys.publickey().export_key()
    private_key = keys.export_key()
    public_key_encrypted = AES_encrypt(public_key, hashed_password, AES.MODE_CBC)
    private_key_encrypted = AES_encrypt(private_key, hashed_password, AES.MODE_CBC)

    f = open("privateKey.pem", "wb")
    f.write(private_key_encrypted);
    f.close()

    f = open("publicKey.pem", "wb")
    f.write(public_key_encrypted);
    f.close()


def AES_encrypt(message, key, mode):
    cipher = AES.new(key, mode)
    # iv is generated randomly and we read it from cipher.iv
    return cipher.encrypt(pad(message, AES.block_size))


def AES_decrypt(ciphertext, key, iv, mode):
    cipher = AES.new(key, mode, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


def check_password(password):
    print("check")
    return True
     #   hashed_password = hashlib.sha256(bytes(password, "utf-8")).digest()
     #   with open('publicKey.pem', mode='rb') as public_file:
     #       try:
     #           key_data = AES_decrypt(public_file.read(), hashed_password, AES.MODE_CBC)
     #           PRIVATE_KEY = RSA.import_key(key_data)
     #       except ValueError:  # if password was wrong then generate random private key
     #           PRIVATE_KEY = RSA.generate(2048)
     #   with open('privateKey.key', mode='rb') as private_file:
     #       try:
     #           key_data = decrypt(private_file.read(), hashed_password, "CBC").decode()
     #           PRIVATE_KEY = RSA.import_key(key_data)
     #       except ValueError:  # if password was wrong then generate random private key
     #           PRIVATE_KEY = RSA.generate(2048)

