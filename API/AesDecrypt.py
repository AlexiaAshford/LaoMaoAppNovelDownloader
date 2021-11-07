import base64
import hashlib
from Crypto.Cipher import AES


iv = b'8yeywyJ45esysW8M'


def encrypt(text, key):
    """AES.MODE_CBC加密"""
    aes_key = hashlib.sha256(key.encode('utf-8')).digest()
    aes_key = AES.new(aes_key, AES.MODE_CFB, iv)
    return base64.b64encode(AES.AESMode.encrypt(text))


def decrypt(encrypted, key='b23c159r9t88hl2q'):
    """AES.MODE_CBC解密"""
    aes_key = hashlib.sha256(key.encode('utf-8')).digest()
    aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return pkcs7un_padding(aes.decrypt(base64.b64decode(encrypted)))


def pkcs7un_padding(data):
    """AES.MODE_CBC解密"""
    length = len(data)
    un_padding = ord(chr(data[length - 1]))
    return data[0:length - un_padding]


def example(express, result=None):
    """转十六进制为字典"""
    return eval(express)
