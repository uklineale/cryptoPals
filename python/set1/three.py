# How to score a piece of English plaintext
import binascii
import pprint
from operator import itemgetter

freqs = {'T': '9.10', 'N': '6.95', 'g': '2.03', 'f': '2.30', 'S': '6.28', 'G': '2.03', 'F': '2.30', 'E': '12.02',
         'U': '2.88', 'o': '7.68', 'I': '7.31', 'C': '2.71', 'K': '0.69', 'L': '3.98', 'e': '12.02', 'z': '0.07',
         'Y': '2.11', 'R': '6.02', 'h': '5.92', 'D': '4.32', 'm': '2.61', 'i': '7.31', 'J': '0.10', 't': '9.10',
         'O': '7.68', 'v': '1.11', 'W': '2.09', 'p': '1.82', 'P': '1.82', 'b': '1.49', 'j': '0.10', 'B': '1.49',
         'l': '3.98', 's': '6.28', 'H': '5.92', 'M': '2.61', 'n': '6.95', 'x': '0.17', 'd': '4.32', 'y': '2.11',
         'w': '2.09', 'c': '2.71', 'Q': '0.11', 'A': '8.12', 'u': '2.88', 'a': '8.12', 'X': '0.17', 'Z': '0.07',
         'k': '0.69', 'V': '1.11', 'q': '0.11', 'r': '6.02'}

alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
target = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
pp = pprint.PrettyPrinter(indent=4)

def strToFreqDict(string):
    length = len(string)
    lowered = string.lower()
    freq = {letter: lowered.count(letter)/length for letter in lowered}
    return freq

def scoreForEnglish(decodedStr):
    score = 0
    freqDict = strToFreqDict(decodedStr)
    for c in freqDict.keys():
        if c not in freqs.keys():
            score += 100
        else:
            score += abs(float(freqs[c]) - freqDict[c]) * 5
    return score

def scoreForPlaintext(decodedStr):
    return len([c for c in decodedStr if c in alpha or c is ' '])/len(decodedStr)

#Returns a list of tuples
def decode(encodedHex, plaintext=True):
    encoded = binascii.unhexlify(encodedHex)
    scores = []
    for c in range(256):
        decoded = ''.join(chr(c ^ b) for b in encoded)
        if plaintext:
            score = scoreForPlaintext(decoded)
        else:
            score = scoreForEnglish(decoded)
        scores.append((c, decoded, score))

    scores.sort(key=itemgetter(2))
    return scores

if __name__ == "__main__":
    pp.pprint(decode(target))