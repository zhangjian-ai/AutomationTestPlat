import os

from Cryptodome.PublicKey import RSA

path = os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'keys/')


def produce():
    """
    生成公钥、私钥对
    :return: 公钥字符串
    """
    # 生成私钥
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(path + "private_key.pem", "wb") as file_out:
        file_out.write(private_key)

    # 生成公钥
    public_key = key.publickey().export_key()
    with open(path + "public_key.pem", "wb") as file_out:
        file_out.write(public_key)


def load_public_key():
    # 读取公钥
    with open(path + "public_key.pem", 'r', encoding='utf-8') as f:
        content = f.read()

    return content
