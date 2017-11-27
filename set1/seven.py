from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

key = b'YELLOW SUBMARINE'
defaultBackend = default_backend()
with open(seven_ct.txt) as f:
    ct = binascii.a2b_base64(f.read())

cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
decryptor = cipher.decryptor()
pt = decryptor.update(ct) + decryptor.finalize()

print(pt)
