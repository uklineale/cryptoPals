from python.set2.eleven import detect_ecb_or_cbc
from python.set2.ten import encryptEcb
from python.set2.nine import pad_pkcs7, unpad_pkcs7
import os, binascii

key = os.urandom(16)

def pad(bStr, prepend=None):
    pad_b64 = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
                aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
                dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
                YnkK'''
    if prepend == None:
        pad_bytes = bStr + binascii.a2b_base64(pad_b64)
    else:
        pad_bytes = prepend + bStr + binascii.a2b_base64(pad_b64)

    full_metal_padchemist = pad_pkcs7(pad_bytes)

    return full_metal_padchemist

def encrypt(bStr, prepend=None, key=key):
    padded = pad(bStr, prepend=prepend)
    return encryptEcb(padded, key)

def decrypt_oracle(encrypt_func):
    blocksize = find_block_size(encrypt_func)
    mode = detect_ecb_or_cbc(encrypt_func)
    if mode == 'ECB':
        secret_len = len(encrypt_func(b''))
        known_bytes = b''

        new_byte = b''
        while len(known_bytes) < secret_len:
            new_byte = decrypt_byte(encrypt_func, blocksize, known_bytes)
            known_bytes += bytes([new_byte])

        return known_bytes

def decrypt_byte(encrypt_func, blocksize, known_bytes):
    # Space the decrypted byte
    shim = b'A' * (blocksize - (len(known_bytes) % blocksize) - 1)
    # Map of ciphertext to byte
    stencils = {}

    # Make a buuunch of stencils, see which one fits the next byte
    for i in range(256):
        stencil = encrypt_func(shim + known_bytes + bytes([i]))
        stencils[stencil[0:len(shim) + len(known_bytes) + 1]] = i

    unencrypted = encrypt_func(shim)[0:len(shim) + len(known_bytes) + 1]
    if unencrypted in stencils:
        return stencils[unencrypted]
    return None


def find_block_size(encrypt_func):
    lastBlock = len(encrypt_func(b'A'))
    for i in range(100):
        guess = b'A' * i
        num_bytes = len(encrypt_func(guess))
        if num_bytes != lastBlock:
            blocksize = num_bytes - lastBlock
            return blocksize


if __name__ == "__main__":
    print(unpad_pkcs7(decrypt_oracle(encrypt)))
