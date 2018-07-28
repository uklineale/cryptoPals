from python.set1.eight import getBlocks
import binascii, random, os
from python.set2.ten import decryptCbc, encryptCbc
from python.set2.nine import pad_pkcs7, unpad_pkcs7

key = os.urandom(16)

strings = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
           'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
           'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
           'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
           'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
           'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
           'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
           'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
           'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
           'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93]']

# Returns ct and iv
def encrypt():
    iv = os.urandom(16)

    choice = random.choice(strings)
    choice_bytes = binascii.a2b_base64(choice)
    padded_bytes = pad_pkcs7(choice_bytes)

    ct = encryptCbc(padded_bytes, key, iv)

    return (iv, ct)


def padding_oracle(ct, iv):
    pt = decryptCbc(ct, key, iv)
    try:
        unpad_pkcs7(pt)
        return True
    except:
        return False

# Can't do first block
def padding_oracle_attack():
    # So figure out intermediate state byte by byte, then xor i2 with c1 to find pt2
    # Use c1' to find out valid padding, xor c1' and valid pad position
