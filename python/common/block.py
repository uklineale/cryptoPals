def get_block_number(i, blocksize):
    return i // blocksize

def getBlocks(bStr, blocksize=16):
    blocks = []
    carry = 0 if len(bStr) % blocksize == 0 else 1
    numBlocks = (len(bStr) // blocksize) + carry
    for i in range(numBlocks):
        start = i * blocksize
        end = start + blocksize
        blocks.append(bStr[start:end])

    return blocks
