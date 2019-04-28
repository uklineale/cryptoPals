# I think this is really how the hint was meant to be interpreted
# Plus I'll add extra useful stuff
import binascii

freqs = {'u': '2.88', 'c': '2.71', 'b': '1.49', 'w': '2.09', 'q': '0.11', 'n': '6.95', 'x': '0.17', 'z': '0.07', 'e': '12.02', 'f': '2.30', 'd': '4.32', 'm': '2.61', 'l': '3.98', 'p': '1.82', 'i': '7.31',
         'g': '2.03', 'r': '6.02', 't': '9.10', 'v': '1.11', 'o': '7.68', 'h': '5.92', 's': '6.28', 'a': '8.12', 'y': '2.11', 'k': '0.69', 'j': '0.10'}

fingerprint = [freqs.values()]

alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numeric = '0123456789'


def strToFreqDict(string):
    length = len(string)
    lowered = string.lower()
    freq = {letter: lowered.count(letter)/length for letter in lowered}
    return freq

# Returns fingerprint of string
def strToFingerprint(string):
    lowered = strToFreqDict(string.lower())
    return lowered.values()

def differenceBetweenFreqDicts(fd1, fd2):
    score = 0
    for c in fd1.keys():
        if c not in fd2.keys():
            score -= 30
        else:
            score += abs(float(fd2[c]) - float(fd1[c])) * 5
    return score

def strToFreqDict(string):
    length = len(string)
    lowered = string.lower()
    freq = {letter: lowered.count(letter)/length for letter in lowered}
    return freq

# First attempt at scoring function
def scoreForEnglish(decodedStr):
    score = 0
    freqDict = strToFreqDict(decodedStr)
    for c in freqDict.keys():
        if c not in freqs.keys():
            score += 100
        else:
            score += abs(float(freqs[c]) - freqDict[c]) * 5
    return score

# A better, simpler approach at scoring
def scoreForPlaintext(str):
    return len([c for c in str if c in alpha or c is ' '])/len(str)