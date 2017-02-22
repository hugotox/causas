from django.conf import settings
from cryptography.fernet import Fernet


def encrypt(text):
    f = Fernet(settings.MASTER_KEY)
    return f.encrypt(bytes(text, encoding='utf8')).decode('utf8')


def decrypt(token):
    f = Fernet(settings.MASTER_KEY)
    return f.decrypt(token.encode('utf8')).decode('utf8')
