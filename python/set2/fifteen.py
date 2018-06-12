from python.set2.nine import unpad_pkcs7

# Just edited the unpad function in 9
if __name__ == '__main__':
    fails = [b'YELLOW SUBMARINE\x01\x02\x03', b'your buy tencent\x02', b'YELLOW SUBMARI'+ b'\x02' + b'\x01']
    for i in fails:
        try:
            unpad_pkcs7(i)
            assert False == True
        except:
            continue
    assert True == True

    passes = [b'YELLOW SUBMARINE' + b'\x10' * 16, b'abcd' + b'\x0c' * 12]
    for i in passes:
        try:
            unpad_pkcs7(i)
        except:
            assert False == True

