from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from python.common.block import getBlocks
from python.common.util import xor


def encryptEcb(pt, key):
    defaultBackend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()
    return ct

def decryptEcb(ct, key):
    defaultBackend = default_backend()

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=defaultBackend)
    decryptor = cipher.decryptor()

    pt = decryptor.update(ct) + decryptor.finalize()
    return pt

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

# The operation is the same for encryption and decryption
def xcryptCtr(text, key, nonce, blocksize=16):
    ctr = 0
    output = b''

    for block_start in range(0, len(text), blocksize):
        keystream = generateKeystream(key, nonce, ctr, blocksize)
        block = text[block_start: block_start + blocksize]
        output += bytearray([a ^ b for a,b in zip(block, keystream)])
        ctr += 1

    return bytes(output)

# We're concatenating the nonce and counter because the nonce
# isn't randomly generated. Apparently if it is randomly generated
# you can just xor them together
def generateKeystream(key, nonce, ctr, blocksize=16):
    ctr_block = nonce.to_bytes(int(blocksize/2), byteorder='little') \
                + ctr.to_bytes(int(blocksize/2), byteorder='little')

    return encryptEcb(ctr_block, key)



