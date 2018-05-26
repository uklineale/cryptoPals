# A common padding scheme is PKCS#7. Apparently
def pad_pkcs7(plaintext, blockSize=16, paddingValue=b'\x04'):
    numPaddingBytes = blockSize - (len(plaintext) % blockSize)
    return plaintext + (paddingValue * numPaddingBytes)

def unpad_pkcs7(plaintext, paddingValue=b'\x04'):
    return plaintext.strip(paddingValue)


if __name__ == "__main__":
    assert(len(pad_pkcs7(b'YELLOW SUBMARINE', 20)) is 20)
    assert(len(pad_pkcs7(b'HELLO, GOODBYE', 10)) is 20)
    assert(len(pad_pkcs7(b'abcd', 4)) is 8) # adds empty pad block


    print(pad_pkcs7(b'YELLOW SUBMARINE', 16))