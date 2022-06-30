# Problem1.py
# Caesar, Substitution, Vigenere, and Homophonic Substitition ciphers
#
# CS 341 Cryptography, Carleton College
# David Liben-Nowell (dln@carleton.edu)

from collections import defaultdict


def load_file(filename):
    '''Load all of the text from the given file into a single string.'''
    with open(filename, "r") as f:
        s = "".join(line.rstrip() for line in f)
    return s.split(" ")

def count_Ngram_frequency(text, n=1):
    '''Count all sequences of N consecutive letters in the given string,
       and return a (default) dictionary of those counts.  Does NOT
       maintain case; all counts are for the input string converted to
       all upper case.  (So n=1 is unigrams, n=2 is bigrams, etc.)'''
    counts = defaultdict(int)
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        if n == 1 and len(ngram[0])>0:
            counts[int("".join(ngram))] += 1
        elif len(ngram[0])>0:
            counts[tuple(ngram)] += 1
    return counts

def analyze(c):
    ciphertext = load_file(c)
    unigrams = count_Ngram_frequency(ciphertext, 1)
    bigrams = count_Ngram_frequency(ciphertext, 2)
    trigrams = count_Ngram_frequency(ciphertext, 3)
    quadgram = count_Ngram_frequency(ciphertext, 4)

    unigrams_sorted = dict(sorted(unigrams.items(),key= lambda x:x[1]))
    bigrams_sorted = dict(sorted(bigrams.items(),key= lambda x:x[1]))
    trigrams_sorted = dict(sorted(trigrams.items(), key = lambda x:x[1]))
    quadgrams_sorted = dict(sorted(quadgram.items(), key = lambda x:x[1]))

    print("=====UNIGRAM=====")
    print(unigrams_sorted)

    print("=====TRIGRAM=====")
    for key in trigrams_sorted.keys():
        if trigrams_sorted[key] > 20:
            print(key, trigrams_sorted[key])


def breakHomophonic(c):
    cipher_map = {
        "0": "t",
        "1": "o",
        "2": "m",
        "3": "r",
        "4": "t",
        "5": "n",
        "6": "j",
        "7": "o",
        "8": "t",
        "9": "o",
        "10": "x",
        "11": "n",
        "12": "p",
        "13": "o",
        "14": "g",
        "15": "n",
        "16": "s",
        "17": "s",
        "18": "a",
        "19": "d",
        "20": "c",
        "21": "e",
        "22": "b",
        "23": "i",
        "24": "o",
        "25": "k",
        "26": "m",
        "27": "a",
        "28": "s",
        "29": "e",
        "30": "n",
        "31": "h",
        "32": "u",
        "33": "d",
        "34": "r",
        "35": "n",
        "36": "i",
        "37": "d",
        "38": "h",
        "39": "e",
        "40": "l",
        "41": "n",
        "42": "l",
        "43": "t",
        "44": "b",
        "45": "f",
        "46": "t",
        "47": "a",
        "48": "l",
        "49": "s",
        "50": "w",
        "51": "o",
        "52": "e",
        "53": "i",
        "54": "c",
        "55": "r",
        "56": "t",
        "57": "a",
        "58": "r",
        "59": "z",
        "60": "u",
        "61": "e",
        "62": "h",
        "63": "m",
        "64": "i",
        "65": "e",
        "66": "a",
        "67": "t",
        "68": "e",
        "69": "i",
        "70": "e",
        "71": "e",
        "72": "s",
        "73": "h",
        "74": "q",
        "75": "d",
        "76": "l",
        "77": "y",
        "78": "h",
        "79": "v",
        "80": "t",
        "81": "e",
        "82": "t",
        "83": "o",
        "84": "p",
        "85": "a",
        "86": "e",
        "87": "a",
        "88": "u",
        "89": "o",
        "90": "g",
        "91": "r",
        "92":"y",
        "93": "r",
        "94": "i",
        "95": "w",
        "96": "s",
        "97": "h",
        "98": "e",
        "99": "f",
    }

    deciphered = ""
    with open("homophonic_substitution.txt", "r") as f:
        for line in f:
            new_ln = ""
            for word in line.split():
                # print(word)  # word = "19 82 34" -> ["19", "82", "34"]
                if word in cipher_map.keys() and cipher_map[word] is not None:
                    new_ln += cipher_map[word]
                else:
                    new_ln += " "+ word + " "
       
            deciphered += new_ln + "\n"
    
    return deciphered

def main():
    new_file = open("decrypted_homophonic.txt", "w")

    deciphered = breakHomophonic('homophonic_substitution.txt')
    
    new_file.write(deciphered)
    new_file.close()


if __name__ == "__main__":
    main()

