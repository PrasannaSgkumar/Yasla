
import base64
from Crypto.Cipher import AES
from hashlib import md5

BLOCK_SIZE = 16

def pad(data: str) -> bytes:
    print(data)
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return (data + chr(pad_len) * pad_len).encode("utf-8")   # 👈 return bytes

def unpad(data: bytes) -> str:
    return data[:-data[-1]].decode("utf-8")  # 👈 decode back to string

def get_cipher(key: str):
    m = md5()
    m.update(key.encode("utf-8"))
    return AES.new(m.digest(), AES.MODE_CBC, iv=b"\0" * 16)

def encrypt(plain_text: str, working_key: str) -> str:
    cipher = get_cipher(working_key)
    encrypted = cipher.encrypt(pad(plain_text))
    return encrypted.hex()  # 👈 return hex, not base64

def decrypt(cipher_text: str, working_key: str) -> str:
    cipher = get_cipher(working_key)
    decoded_bytes = bytes.fromhex(cipher_text)  # 👈 decode from hex
    decrypted = cipher.decrypt(decoded_bytes)
    return unpad(decrypted)

