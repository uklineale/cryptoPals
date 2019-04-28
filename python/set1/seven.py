import binascii

from python.common.aes import decryptEcb

if __name__ == '__main__':
    key = b'YELLOW SUBMARINE'
    with open('seven_ct.txt') as f:
        ct = binascii.a2b_base64(f.read())

    pt = decryptEcb(ct, key)
    print(pt)