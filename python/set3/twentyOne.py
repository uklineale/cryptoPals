#Implement the Mersenne Twister. Well, this was a jump, but not a bad one. I got this.

# w - word size
# n - degree of recurrence
# m - middle word, an offset of some sort
# r - lower bitmask, seperator
import binascii

w, n, m, r = 32, 624, 397, 31
a = binascii.a2b_hex('9908B0DF')
u, d = 11, binascii.a2b_hex('FFFFFFFF')
s, b = 7, binascii.a2b_hex('9D2C5680')
t, c = 15, binascii.a2b_hex('EFC60000')
l = 18
f =  1812433253

# Seeds MT if unseeded
C_FIXED_SEED = 5489

MT = [0] * n
index = n+1
upper_mask = (1 << r) - 1
lower_mask = binascii.a2b_hex('FFFF')

def seed_mt(seed):
    # Initialize index for some reason
    index = n
    MT[0] = seed
    for i in range(1,n):
        prev = MT[i-1]
        MT[i] = f * (prev ^ (prev >> (w-2))) + i

def extract_number():
    if index >= n:
        if index > n:
            # Uninitialized, used fixed seed
            seed_mt(C_FIXED_SEED)
        twist()
        index = 0

    y = MT[index]
    y = y ^ ((y >> u) & d) #since d is commonly all 1s, technically not needed
    y = y ^ ((y >> s) & b)
    y = y ^ ((y >> t) & c)
    y = y ^ (y >> 1)

    index = index + 1
    return y & 0xffff

def twist():
    for i in range(1,n):
        x =

