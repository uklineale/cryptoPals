import binascii

from python.common.aes import decryptCbc, encryptCbc
from python.common.util import binary_assert_equals
from python.set2.nine import pad_pkcs7, unpad_pkcs7

if __name__ == "__main__":
    blocksize = 16
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * blocksize

    with open('ten_ct.txt', 'r') as f:
        ct = binascii.a2b_base64(f.read())

        # Test decrypt
        pt = unpad_pkcs7(decryptCbc(ct, key, iv))
        [print(i) for i in pt.split(b'\n')]

        # Test encrypt
        expected = pad_pkcs7(b'baghra, our boy')
        actual = unpad_pkcs7(decryptCbc(encryptCbc(expected, key, iv), key, iv))
        binary_assert_equals(expected, actual)


