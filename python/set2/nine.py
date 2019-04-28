from python.common.pad import pad_pkcs7

if __name__ == "__main__":
    assert(len(pad_pkcs7(b'YELLOW SUBMARINE', 20)) is 20)
    assert(len(pad_pkcs7(b'HELLO, GOODBYE', 10)) is 20)
    assert(len(pad_pkcs7(b'abcd', 4)) is 8) # adds empty pad block


    print(pad_pkcs7(b'YELLOW SUBMARINE', 16))