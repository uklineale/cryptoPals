def binary_assert_equals(bstr1, bstr2, printStats=False):
    if printStats:
        print("Length binary 1: " + str(len(bstr1)))
        print("Length binary 2: " + str(len(bstr2)))
        for i in range(len(bstr1)):
            if bstr1[i] != bstr2[i]:
                print("Byte {} \nExpectFed: {} | Actual: {}".format(i, bstr1[i], bstr2[i]))

    assert bstr1 == bstr2


def unpad_pcks7(pt, blocksize=16):
    padding = pt[-1]
    pad_len = blocksize if padding == b'\x00' else ord(padding)
    for i in range(len(pt) - 1, len(pt) - pad_len, -1):
        if pt[i] != padding:
            raise Exception("Bad PKCS#7 Padding")
    return pt.strip(padding)


'''
:param1  - a bytearray
:param2  - another bytearray
:returns - bytearray of xored values
'''
def xor(ba1, ba2):
    assert len(ba1) == len(ba2)
    xored_ba = bytearray([x ^ y for x,y in zip(ba1, ba2)])
    return xored_ba

