# kasiski.py
# Kasiski examination to decode Vigenere Ciphers
#
# CS 341 Cryptography, Carleton College
# David Liben-Nowell (dln@carleton.edu)
# Adela Dujsikova and Thien K. M. Bui

from collections import defaultdict

def load_file(filename):
    '''Load all of the text from the given file into a single string.'''
    with open(filename, "r") as f:
        s = "".join(line for line in f)
    return s


def processFile(file):
    '''Takes a txt file as an input and turns it into a string containing only letters in lower case.'''
    with open(file) as f:
        # remove white space
        str = "".join(line.strip() for line in f)
    str = str.lower()
    # only return lower-case letters, no other characters
    return "".join(c for c in str if ord(c) > 96 and ord(c) < 123)

def getLetterFreq(str):
    '''Creates a dictionary of frequencies of all letters in the input string. The string needs to be pre-processed so that all the letters are lower-case and there are no spaces (see processFile).'''
    dict = {}
    for i in str:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
    # change the counts stored in the dictionary into frequences before returning
    return {key: v/len(str) for key, v in dict.items()}

def count_Ngram_frequency(text, n=1):
    '''Count all sequences of N consecutive letters in the given string,
       and return a (default) dictionary of those counts.  Does NOT
       maintain case; all counts are for the input string converted to
       all upper case.  (So n=1 is unigrams, n=2 is bigrams, etc.)'''
    counts = defaultdict(int)
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n].upper()
        if ngram.isalpha():
            counts[ngram.upper()] += 1
    return counts

def main():
    reference = load_file("vigenere.txt")
    cipher = processFile("vigenere.txt")

    #for frequency analysis later
    r_freq, c_freq= getLetterFreq(reference), getLetterFreq(cipher)

    #find all the repeating strings
    freq_dict = count_Ngram_frequency(cipher, 2)

    #figure out how far apart these bigrams are 
    for key in freq_dict:
        freq_dict[key] = []
        space_btw = 0
        for i in range(len(cipher) + 1):
            ngram = cipher[i:i+2].upper()
            if ngram == key:
                freq_dict[key].append(space_btw)
                space_btw = 0
            else:
                space_btw += 2

    print(freq_dict)

if __name__ == "__main__":
    main()