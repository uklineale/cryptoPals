from python.set1.eight import getBlocks
from python.set2.ten import encryptCbc, encryptEcb
from python.set2.nine import pad_pkcs7, unpad_pkcs7
import os
import random as r

def hidden_oracle(encryption_func, test_isCbc=None):
    bStr = b'aaaaaaaaaaaaaaaaaaaaaaaaaa' * 20 #Low entropy will show up in ECB
    ct = encryption_func(bStr) if test_isCbc == None else encryption_func(bStr, test_isCbc)
    if detect_entropy(ct) < .2:
        return 'ECB'
    else:
        return 'CBC'

def detect_entropy(ct):
    blocks = getBlocks(ct)
    repeated_blocks_freq = {}

    for block in blocks:
        repeated_blocks_freq[block] = repeated_blocks_freq.get(block, 0) + 1

    entropy = len(repeated_blocks_freq) / len(blocks)
    return entropy


def crouching_cipher(bStr, isCbc=r.randrange(0,2)):
    key = generate_key(16)
    padded_pt = pad_plaintext(bStr)

    if isCbc is 1:
        iv = os.urandom(16)
        return encryptCbc(padded_pt, key, iv)
    else:
        return encryptEcb(padded_pt, key)


def pad_plaintext(pt):
    num_prepend = r.randrange(5,11)
    num_append = r.randrange(5,11)

    prepend_str = os.urandom(num_prepend)
    append_str = os.urandom(num_append)

    padded_pt = prepend_str + pt + append_str

    return pad_pkcs7(padded_pt)

def generate_key(length):
    return os.urandom(length)

if __name__ == '__main__':
    for i in range(100):
        test = r.randrange(0,2)
        expected = 'ECB' if test == 0 else 'CBC'
        actual = hidden_oracle(crouching_cipher, test_isCbc=test)
        assert expected == actual