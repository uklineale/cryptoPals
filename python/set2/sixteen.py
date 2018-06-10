import os

from python.set2.nine import pad_pkcs7, unpad_pkcs7
from python.set2.ten import encryptCbc, decryptCbc
from python.set1.two import xor

key = os.urandom(16)
iv = os.urandom(16)

def encryption_oracle(pt):
    stripped = pt.replace(b';', b'%3B').replace(b'=', b'%3D')
    unpadded = b'comment1=cooking%20MCs;userdata=' + \
               stripped + \
                b';comment2=%20like%20a%20pound%20of%20bacon'
    padded = pad_pkcs7(unpadded)
    return encryptCbc(padded, key, iv)

def decryption_oracle(ct):
    pt = decryptCbc(ct, key, iv)
    unpad = unpad_pkcs7(pt)
    return b';admin=true' in unpad

# Second block counts
# Gotta do orig_ct xor known output block xor chosen output
# xoring by known output cancels out that output, and xoring 0 is identity
def bit_flip(ct):
    prev_ct_block = ct[16:32]
    current_pt_block = b'%3Badmin%3Dtrue;'
    desired_pt_block = b';admin=trueFiveC'
    payload_block = xor(xor(prev_ct_block, current_pt_block), desired_pt_block)

    payload_ct = ct[:16] + payload_block + ct[32:]

    return payload_ct

if __name__ == '__main__':
    ct = encryption_oracle(b';admin=true')
    evil_ct = bit_flip(ct)
    print(decryption_oracle(evil_ct))