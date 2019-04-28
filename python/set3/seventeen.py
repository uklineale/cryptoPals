from python.common.pad import pad_pkcs7, unpad_pkcs7
from python.set1.eight import getBlocks
import binascii, random, os

from python.set1.two import xor
from python.set2.ten import decryptCbc, encryptCbc

BLOCKSIZE = 16
key = os.urandom(BLOCKSIZE)

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

    ct = bytearray(encryptCbc(padded_bytes, key, iv))

    return (ct, iv)


def padding_oracle(ct, iv):
    pt = decryptCbc(bytes(ct), key, iv)
    try:
        unpad_pkcs7(pt)
        return True
    except:
        return False

'''
ct (bytearray) - the ciphertext to decrypt
iv (bytearray) - the initialization vector
blocksize=16 (int) - the block size
'''
def crack(ct, iv, blocksize=16):
    pt = bytearray()
    for block_num in range(0, len(ct) // blocksize): # per block
        start_of_block = block_num * blocksize
        block = ct[start_of_block:start_of_block+blocksize]
        intermediate_bytes = bytearray()

        for i in range(len(block)-1, -1, -1):# valid padding starts backwards
            pre_shim = b'a' * i
            pad_byte = blocksize - i
            post_shim = bytearray([x ^ pad_byte for x in intermediate_bytes]) # TODO this doesn't work

            for guess in range(256):
                modified_prev_block = pre_shim + bytearray([guess]) + post_shim
                if (padding_oracle(modified_prev_block + block, b'I don\'t givefuck')):
                    intermediate_byte = guess ^ pad_byte
                    intermediate_bytes = bytearray([intermediate_byte]) + intermediate_bytes # prepend
                    break

        prev_block = iv if start_of_block == 0 else ct[start_of_block - blocksize: start_of_block]
        pt += xor(prev_block, intermediate_bytes)

    return bytes(pt)



# Can't do first block PSYCH, we're given that because chops
def po_attack():
    ct_and_iv = encrypt()
    return crack(ct_and_iv[0], ct_and_iv[1])



if __name__ == "__main__":
    pts = []
    for i in range(4):
        a = po_attack()
        pts.append(a)
    pts.sort(key=lambda pts: pts[5]) #Implement a sort on the 6th byte in each bytearray
    print(set(pts))



