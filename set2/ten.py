from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def pycaEncryptECB(pt, key):
    defaultBackend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
    enc = cipher.encryptor()
    ct = str(enc.update(pt) + enc.finalize()).split('\\n')
    return ct

if __name__ == '__main__':
    pt = '' 

    ct = pycaEncryptECB()
