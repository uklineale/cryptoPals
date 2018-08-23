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


if __name__ == "__main__":
    assert(len(pad_pkcs7(b'YELLOW SUBMARINE', 20)) is 20)
    assert(len(pad_pkcs7(b'HELLO, GOODBYE', 10)) is 20)
    assert(len(pad_pkcs7(b'abcd', 4)) is 8) # adds empty pad block


    print(pad_pkcs7(b'YELLOW SUBMARINE', 16))