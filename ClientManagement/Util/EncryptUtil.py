#  Copyright (c)  Ong Wi Yi .
from fernet import Fernet


class EncryptUtil:

    @staticmethod
    def encrypt(message):
        key = open("secret.key", "rb").read()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_msg = f.encrypt(encoded_message)
        return encrypted_msg

    @staticmethod
    def decrypt(message):
        key = open("secret.key", "rb").read()
        f = Fernet(key)
        decrypted_msg = f.decrypt(message)
        return decrypted_msg