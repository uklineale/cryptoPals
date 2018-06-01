def binary_assert_equals(bstr1, bstr2, printStats=False):
    if printStats:
        print("Length binary 1: " + str(len(bstr1)))
        print("Length binary 2: " + str(len(bstr2)))
        for i in range(len(bstr1)):
            if bstr1[i] != bstr2[i]:
                print("Byte {} \nExpected: {} | Actual: {}".format(i, bstr1[i], bstr2[i]))

    assert bstr1 == bstr2

def get_block_number(i, blocksize):
    return i // blocksize