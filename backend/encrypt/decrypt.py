import base64
import os

from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA


def decrypt(cipher_text):    # 传入前端加密后的密文串
    path = os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'keys', 'private_key.pem')
    with open(path, 'r', encoding='utf8') as f:
        rsa_private_key = f.read()

    rsa_key = RSA.importKey(rsa_private_key)  # 导入私钥
    cipher = PKCS1_v1_5.new(rsa_key)
    text = cipher.decrypt(base64.b64decode(cipher_text), None)

    return text.decode('utf8')
