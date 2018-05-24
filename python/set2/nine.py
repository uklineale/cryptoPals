# A common padding scheme is PKCS#7. Apparently
def pad_pkcs7(plaintext, blockSize, paddingValue=b'\x04'):
    numPaddingBytes = blockSize - (len(plaintext) % blockSize)
    return plaintext + (paddingValue * numPaddingBytes)

if __name__ == "__main__":
    assert(len(pad_pkcs7('YELLOW SUBMARINE', 20)) is 20)
    assert(len(pad_pkcs7('HELLO, GOODBYE', 10)) is 20)

    print(pad_pkcs7('YELLOW SUBMARINE', 16))