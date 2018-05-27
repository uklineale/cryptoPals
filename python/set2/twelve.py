from python.set2.ten import encryptEcb
from python.set2.nine import pad_pkcs7
import os, binascii

key = os.urandom(16)

def pad(bStr):
    pad_b64 = '''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
                aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
                dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
                YnkK'''
    pad_bytes = binascii.a2b_base64(pad_b64)
    full_metal_padchemist = pad_pkcs7(pad_bytes)

    return full_metal_padchemist

def encrypt(bStr):
    padded = pad(bStr)
    return encryptEcb(padded, key)

def decrypt_oracle(encrypt_func, text):
    print('Not Implemented')

if __name__ == "__main__":
    print(encrypt(b'hello'))
