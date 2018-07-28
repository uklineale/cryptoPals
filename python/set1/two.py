import binascii

def xor(b1, b2):
    assert len(b1) == len(b2)
    result = bytes([x ^ y for x,y in zip(bytearray(b1),bytearray(b2))])
    return result

if __name__ == "__main__":
    b1 = binascii.a2b_hex("1c0111001f010100061a024b53535009181c")
    b2 = binascii.a2b_hex("686974207468652062756c6c277320657965")
    expected = binascii.a2b_hex('746865206b696420646f6e277420706c6179')

    result = xor(b1, b2)

    print(':'.join("{:02x}".format(c) for c in result))
    assert result == expected

