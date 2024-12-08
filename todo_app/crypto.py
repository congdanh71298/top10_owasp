from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

def get_encryption_key():
    key = os.environ.get('ENCRYPTION_KEY')
    if not key:
        # Generate a valid Fernet key
        key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        with open('.env', 'a') as f:
            f.write(f'\nENCRYPTION_KEY={key}')
    return key

cipher_suite = Fernet(get_encryption_key().encode())

def encrypt_text(text):
    if not text:
        return text
    return cipher_suite.encrypt(str(text).encode()).decode()

def decrypt_text(encrypted_text):
    if not encrypted_text:
        return encrypted_text
    return cipher_suite.decrypt(encrypted_text.encode()).decode()