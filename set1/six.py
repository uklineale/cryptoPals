import sys
import binascii
from three import decode

#Hamming distances are edit distances are those not just xor?
#Right, because that returns an integer, not the number of set bits.
test1 = b'this is a test'
test2 = b'wokka wokka!!!'
expected = 37
with open('s1c06_ciphertext.txt','r') as f:
    target = binascii.a2b_base64(f.read())

def numberSetBits(i):
    setBits = 0
    while(i):
        setBits += i & 1
        i >>= 1
    return setBits

def hammingDist(bStr0, bStr1):
    xors = [a ^ b for a,b in zip(bStr0, bStr1)]
    dist = sum([numberSetBits(val) for val in xors])
    return dist

def guessKeySize(ct):
    keyLen_minDist = [0, sys.maxsize]
    for kl in range(2,41):
        #avg of edit dist between 4 blocks
        dist = (hammingDist(ct[:kl], ct[kl:kl*2]) \
                + hammingDist(ct[:kl], ct[kl*2:kl*3]) \
                + hammingDist(ct[:kl], ct[kl*3:kl*4]) \
                + hammingDist(ct[kl:kl*2], ct[kl*2:kl*3]) \
                + hammingDist(ct[kl:kl*2], ct[kl*3:kl*4]) \
                + hammingDist(ct[kl*2:kl*3], ct[kl*3:kl*4])) / (6 * kl)

        if dist < keyLen_minDist[1]:
            keyLen_minDist[0] = kl
            keyLen_minDist[1] = dist

    return keyLen_minDist[0]

def transposeBlocks(ct, keyLen):
    blocks = [ct[i::keyLen] for i in range(keyLen)]
    return blocks

def decodeTransposedBlocks(blocks):
    key = ''
    for block in blocks:
        results = decode(binascii.b2a_hex(block))
        key += chr(results[-1][0])
    return key

def repeatingKeyXor(bStr, bKey):
    xor = []
    keyLen = len(bKey)
    for i in range(len(bStr)):
        xor.append(bStr[i] ^ bKey[i % keyLen])

    return bytes(xor)

if (__name__ == '__main__'):
    print(hammingDist(test1, test2) == expected)

    keySize = guessKeySize(target)
    print('Key size: ' + str(keySize))

    blocks = transposeBlocks(target, keySize)
    print(type(blocks))

    key = decodeTransposedBlocks(blocks)
    print(key)

    plainText = repeatingKeyXor(target, key.encode('ascii'))
    print(plainText.decode('ascii'))



