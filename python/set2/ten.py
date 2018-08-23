from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from python.set2.nine import pad_pkcs7, unpad_pkcs7
from python.set1.seven import decryptEcb
from python.set1.eight import getBlocks
from python.set1.two import xor
from python.util.util import binary_assert_equals
import binascii

def encryptEcb(pt, key):
    defaultBackend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()
    return ct

def encryptCbc(pt, key, iv, blocksize=16):
    blocks = getBlocks(pt, blocksize)
    out_blocks = []

    for i in range(len(blocks)):
        curr = blocks[i]
        chaining_block = iv if i == 0 else out_blocks[i-1]

        pre_cipher = xor(chaining_block, curr)
        post_cipher = encryptEcb(pre_cipher, key)

        out_blocks.append(post_cipher)

    return b''.join(out_blocks)

def decryptCbc(ct, key, iv, blocksize=16):
    blocks = getBlocks(ct, blocksize)
    out_blocks = []

    for i in range (len(blocks)):
        curr = blocks[i]
        chaining_block = iv if i == 0 else blocks[i-1]
        post_cipher = decryptEcb(curr, key)
        post_add = xor(post_cipher, chaining_block)


        out_blocks.append(post_add)

    return b''.join(out_blocks)

if __name__ == "__main__":
    blocksize = 16
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * blocksize

    with open('ten_ct.txt', 'r') as f:
        ct = binascii.a2b_base64(f.read())

        # Test decrypt
        pt = unpad_pkcs7(decryptCbc(ct, key, iv))
        [print(i) for i in pt.split(b'\n')]

        # Test encrypt
        expected = pad_pkcs7(b'baghra, our boy')
        actual = unpad_pkcs7(decryptCbc(encryptCbc(expected, key, iv), key, iv))
        binary_assert_equals(expected, actual)


