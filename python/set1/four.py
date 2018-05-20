from set1.three import decode
import binascii

import pprint
pp = pprint.PrettyPrinter(indent=4)

freqs = {'u': 2.88, 'c': 2.71, 'b': 1.49, 'w': 2.09, 'q': 0.11, 'n': 6.95, 'x': 0.17, 'z': 0.07, 'e': 12.02, 'f': 2.30, 'd': 4.32, 'm': 2.61, 'l': 3.98, 'p': 1.82, 'i': 7.31,
         'g': 2.03, 'r': 6.02, 't': 9.10, 'v': 1.11, 'o': 7.68, 'h': 5.92, 's': 6.28, 'a': 8.12, 'y': 2.11, 'k': 0.69, 'j': 0.10}
englishFingerprint = list(freqs.values())

def hexToFingerprint(hexString):
    lowered = str(binascii.unhexlify(hexString)).lower()
    freqDict = {l : lowered.count(l)/len(lowered) for l in lowered}
    return list(freqDict.values())

def compareSortedFingerprints(fingerprint1, fingerprint2):
    score = 0
    for one,two in list(zip(fingerprint1, fingerprint2)):
        score += (one-two)**-2
    return score

def compareFingerprints(f1, f2):
    f1.sort()
    f2.sort()
    return compareSortedFingerprints(f1,f2)

def main():
    with open('four_files.txt', 'r') as f:
        strings = [s for s in f.readlines()]
    parsedStrings = [s.strip() for s in strings]
    print(len(parsedStrings))

    scores = {compareFingerprints(englishFingerprint, hexToFingerprint(s)) : s for s in parsedStrings}
    topSortedScores = list(sorted(scores.items()))
    for score,hexStr in topSortedScores[-3:]:
        print('\n' + hexStr)
        xorDecoded = decode(hexStr)
        pp.pprint(xorDecoded[-10:])

if __name__ == '__main__':
    main()
