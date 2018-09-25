import binascii

from python.common.aes import xcryptCtr

# nonce = 0
# key = b'YELLOW SUBMARINE'
# text = binascii.a2b_base64('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')

nonce = 1
key = b'YELLOW SUBMARINE'
text = b'\x86kTQ\x8d\x8a\xf4\xc7\x84k\x8fU\xccN\xab\xb5j\xb4\x13\xa0y\xb4\xddc\xbb\xb1\x97\xfc\x83\x7f\xd8i'

if __name__ == '__main__':
    print(xcryptCtr(text, key, nonce))