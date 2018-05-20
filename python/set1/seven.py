from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii


def pycaDecryptECB(ct, key):
    defaultBackend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
    decryptor = cipher.decryptor()
    pt = str(decryptor.update(ct) + decryptor.finalize()).split('\\n')
    return pt


if __name__ == '__main__':
    key = b'YELLOW SUBMARINE'
    with open('seven_ct.txt') as f:
        ct = binascii.a2b_base64(f.read())

    pt = pycaDecryptECB(ct, key)
    print(pt)