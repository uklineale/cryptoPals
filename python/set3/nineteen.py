from operator import itemgetter

from python.common.aes import xcryptCtr
import binascii
import os, sys

# Might just say fuck this
# The first thing that comes to mind is breaking each block up
# and doing something similar to the repeating key xor problem (#6)
from python.common.freq import scoreForPlaintext
from python.common.util import xor

if __name__ == "__main__":
    key = os.urandom(16)

    # Works for both 'nineteen.txt' and 'twenty.txt'
    with open('twenty.txt') as f:
        cts = [xcryptCtr(binascii.a2b_base64(l.strip('\n')), key, 1) for l in f.readlines()]
        min = sys.maxsize

        for ct in cts:
            if len(ct) < min:
                min = len(ct)

        # Trim to smallest text len
        cts = [ct[:min] for ct in cts]

        # Group bytes by order
        # There's probably a way to do this in a comprehension
        grouped_bytes = list()
        for i in range(len(cts[0])):
            a = bytearray()
            for ct in cts:
                a.append(ct[i])
            grouped_bytes.append(a)

        grouped_pt = []
        for group in grouped_bytes:
            scores = []
            for guess in range(256):
                guess_stream = bytes([guess]) * len(group)
                possible_pt = bytes(xor(group, bytearray(guess_stream)))
                scores.append((possible_pt, scoreForPlaintext(str(possible_pt))))

            scores.sort(key=itemgetter(1), reverse=True)
            grouped_pt.append(scores[0][0])


        # This conversion feels really bulky
        # I've lost my python touch
        pts = []
        for i in range(len(cts)):
            pts.append(b'')

        for i in range(len(grouped_pt)):
            pt = grouped_pt[i]
            for j in range(len(pt)):
                pts[j] += bytes([pt[j]])

        for pt in pts:
            print(pt)














