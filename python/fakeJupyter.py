from cryptography.hazmat.primitives.padding import PKCS7 as pkcs7

def unpad(bstr, blocksize=16):
    u = pkcs7(blocksize * 8).unpadder()
    u.update(bstr)
    return u.finalize()

a = b'0123456789a\x04\x04\x04\x02\x02' + b'\x10' * 16
print(len(a))
assert len(a) % 16 == 0

unpad(a)

print('Valid')