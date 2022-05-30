from pydoc import plain
from cryptography.fernet import Fernet

class crypto_code():

    def encrypt(val):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        byt_val=str(val).encode()
        cipher_text = cipher_suite.encrypt(byt_val)
        return cipher_text

    def decrypt(val_d):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        byt_val=str(val_d).encode()
        plain_text=cipher_suite.decrypt(byt_val)
        return plain_text
        
