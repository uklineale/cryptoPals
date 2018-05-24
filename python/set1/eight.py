from python.set1.sixth import guessBlockSize, hammingDist
import math, binascii, sys

#EXTERN
def getBlocks(bStr, blockSize):
    blocks = []
    for i in range(blockSize):
        start = i * blockSize
        end = start + blockSize
        blocks.append(bStr[start:end])

    return blocks

# Both work, but counting repeating blocks is simple
def countRepeatedBlocks(blocks):
    counts = {}
    for block in blocks:
        ascii = binascii.b2a_hex(block)
        counts[ascii] = counts.get(ascii, 0) + 1

    return max(counts.items(), key=lambda i:i[1])[1]

def averageHammingDistBetweenBlocks(blocks):
    numBlocks = len(blocks)
    accumulator = 0

    for i in range(numBlocks):
        for j in range(i + 1,numBlocks):
            accumulator += hammingDist(blocks[i], blocks[j])

    accumulator /= math.factorial(numBlocks)

    return accumulator

if __name__ == "__main__":
    likelyEcb = ''
    minDist = sys.maxsize

    with open('eight_ct.txt','r') as f:
        for str in f.readlines():
            bStr = binascii.a2b_hex(str[:-1])
            blockSize = guessBlockSize(bStr)
            dist = averageHammingDistBetweenBlocks(getBlocks(bStr, blockSize))
            if dist < minDist:
                minDist = dist
                likelyEcb = str

    print(likelyEcb)






