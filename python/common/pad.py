EXCEPTION_MESSAGE = "Bad PKCS#7 Padding"

# A common padding scheme is PKCS#7. Apparently
def pad_pkcs7(plaintext, blocksize=16):
    padding = blocksize - (len(plaintext) % blocksize)
    numPadding = padding
    return plaintext + (bytes([padding]) * numPadding)

def unpad_pkcs7(plaintext, blocksize=16):
    padding = plaintext[-1]

    if padding > blocksize:
        raise Exception(EXCEPTION_MESSAGE)

    for char in plaintext[-padding:]:
        if char != padding:
            raise Exception(EXCEPTION_MESSAGE)

    return plaintext.strip(bytes([padding]))
