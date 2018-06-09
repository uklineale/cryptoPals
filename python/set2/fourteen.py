import os, random, sys

from python.set1.eight import getBlocks
from python.set2.twelve import encrypt as encrypt12
from python.set2.twelve import find_block_size
from python.set2.ten import pad_pkcs7

# Unknowns
BLOCKSIZE = 16

key = os.urandom(BLOCKSIZE)
prepend_str = b'a' + os.urandom(random.randint(0, 100))

# Knowns
prepend_str_len = 0


def decrypt(encrypt_func):
    blocksize = find_block_size(encrypt)
    rand_info = find_random_str_len_and_padding(encrypt, blocksize)
    target_padding = find_target_str_padding(encrypt, rand_info[1]) # Puts the last byte of ct alone in it's own block

    known_bytes = b''

    while True:
        decrypted_byte = decrypt_byte(encrypt_func, rand_info, target_padding, blocksize, known_bytes)

        if decrypted_byte == b'\x03' or decrypted_byte is None : # A hacky solution to the halting problem
            break
        known_bytes = decrypted_byte + known_bytes

    return known_bytes

def encrypt(pt):
    return encrypt12(pt, prepend=prepend_str, key=key)

#
def decrypt_byte(encrypt_func, rand_info, target_padding, blocksize, known_bytes):

    # Append this shim to the random string to end on a block boundary
    rand_shim = b'\x03' * rand_info[1]

    # Prepend this shim to the target string to position the next unkown byte of ct
    target_shim = b'\x03' * (target_padding + (len(known_bytes) % blocksize) + 1)

    # The blocks containing the guess without the first byte
    guess_spacer = known_bytes + b'\x04' * (blocksize - (len(known_bytes) % blocksize) - 1)

    # Start of payload
    payload_start = rand_info[0]

    # Map of ct to byte
    byte_map = {}

    # Populate byte map
    for i in range(256):
        guess = bytes([i])
        ct = encrypt_func(rand_shim + guess + guess_spacer + target_shim)
        guess_block = ct[payload_start: payload_start + len(guess_spacer) + 1]
        byte_map[guess_block] = guess

    # Match byte
    if len(known_bytes) + 1 % 16 is 0: # Edge case, last block is all padding
        actual = encrypt_func(rand_shim + target_shim)[-(len(guess_spacer) + 1 + blocksize):-blocksize]
    else:
        actual = encrypt_func(rand_shim + target_shim)[-(len(guess_spacer) + 1):]
    if actual in byte_map:
        return byte_map[actual]
    return None

# Determines the length of string needed to pad the random string
# to a block boundary.
def find_random_str_len_and_padding(encrypt_func, blocksize):
    for i in range(100):
        ct = encrypt_func(b'a' * i)
        gemini_index = find_gemini(ct, blocksize)
        if gemini_index > 0:
            padding = i - blocksize * 2
            return (gemini_index, padding)

# Determines the length of string needed to pad the target string
# to one past a block boundary. Primes the ciphertext to get decrypted
def find_target_str_padding(encrypt_func, rand_padding):
    base_shim = b'a' * rand_padding
    base_len = len(encrypt_func(base_shim))
    for i in range(1, 100):
        ct_len = len(encrypt_func(base_shim + b'a' * i))
        if ct_len > base_len:
            return i


# Determines if the Gemini condition has been reached
# As in, if there are two consecutive, matching blocks
# Returns the index
def find_gemini(ct, blocksize):
    blocks = getBlocks(ct, blocksize=blocksize)
    for i in range(1, len(blocks)):
        if blocks[i-1] == blocks[i]:
            return ct.find(blocks[i])
    else:
        return -1

if __name__ == '__main__':
    str = decrypt(encrypt)

    print(str)