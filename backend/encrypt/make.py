# from Crypto.PublicKey import RSA
from Cryptodome.PublicKey import RSA

# 生成私钥
key = RSA.generate(2048)
private_key = key.export_key()
with open("keys/private_key.pem", "wb") as file_out:
    file_out.write(private_key)
    file_out.close()

# 生成公钥
public_key = key.publickey().export_key()
with open("keys/public_key.pem", "wb") as file_out:
    file_out.write(public_key)
    file_out.close()
