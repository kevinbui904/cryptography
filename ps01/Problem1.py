# Problem1.py
# Caesar, Substitution, Vigenere, and Homophonic Substitition ciphers
#
# CS 341 Cryptography, Carleton College
# David Liben-Nowell (dln@carleton.edu)
# Adela Dujsikova and Kevin Bui

import sys
from collections import defaultdict

from substitution_ciphers import vigenere

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def ltr2int(ch):
    '''Translate letters (upper or lower case) to indices {0, 1, ..., 25}'''
    return ord(ch.upper()) - ord('A')

def int2ltr(i):
    '''Translate indices {0, 1, ..., 25, 26=0, 27=1, ...} to (upper case)
       letters, wrapping around as necessary.'''
    return chr(i % 26 + ord('a'))

def load_file(filename):
    '''Load all of the text from the given file into a single string.'''
    with open(filename, "r") as f:
        s = "".join(line for line in f)
    return s

def count_Ngram_frequency(text, n=1):
    '''Count all sequences of N consecutive letters in the given string,
       and return a (default) dictionary of those counts.  Does NOT
       maintain case; all counts are for the input string converted to
       all upper case.  (So n=1 is unigrams, n=2 is bigrams, etc.)'''
    ct = 0
    counts = defaultdict(int)
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n].lower()
        if ngram.isalpha():
            ct+=1
            counts[ngram.lower()] += 1
    return {key: v/ct for key, v in counts.items()}

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

def test(k, c_freq, r_freq):
    '''Takes in the proposed shift, and the cipher and reference files letter frequencies. Tests the shift by calculating the sum of the products of corresponding letter frequences, considering shift k.'''
    '''Instead of taking in the cipher and reference files as stated in the instructions, the function uses the letter frequency dictionaries. This way we avoid recalculating the same information multiple times.'''
    sum = 0
    for letter in alphabet:
        c_letter_pos = (alphabet.find(letter) - k) % 26
        c_letter = alphabet[c_letter_pos]
        if c_letter in c_freq:
            sum += r_freq[letter] * c_freq[c_letter]
    
    return sum

def breakCaesar(c, r):
    '''Takes in the cipher and reference files. Tests all shifts and chooses the one with the highest sum, then uses the associated shift to decode the ciphertext, which is returned.'''
    r_mod, c_mod = processFile(r), processFile(c)

    if len(r_mod) < 1 or len(c_mod) < 1:
        print("File is empty")
        quit()
        
    r_freq, c_freq= getLetterFreq(r_mod), getLetterFreq(c_mod)

    # find the best shift
    max = 0
    my_shift = 0
    for shift in range(26):
        curr = test(shift, c_freq, r_freq)
        if curr > max:
            max, my_shift = curr, shift

    # load the original ciphertext
    with open(c) as ciphertext:
        str = "".join(line for line in ciphertext)

    # translate the ciphertext into plaintext
    message = ""
    for ch in str:
      if ch in alphabet:
        letter_pos = (alphabet.find(ch) + my_shift) % 26
        ch = alphabet[letter_pos]
      if ch in ALPHABET:
        letter_pos = (ALPHABET.find(ch) + my_shift) % 26
        ch = ALPHABET[letter_pos]
      message += ch
    
    return message

#print(breakCaesar('caesar.txt', 'shakespeare.txt'))

### second part starting here
def getShift(str, r_freq):
    '''Returns both the shift amount (int) and the score for that shift for a specific string and reference frequencies.'''
    c_freq = count_Ngram_frequency(str, 1)
    max = 0
    my_shift = 0
    for shift in range(26):
        curr = test(shift, c_freq, r_freq)
        if curr > max:
            max, my_shift = curr, shift

    return (my_shift, max)

def getKeyLengthScore(l, c_mod, r_freq):
    '''Calculates the score for a key of given length. For a key of length l, there are l different shifts and shif scores that are calculated. The score for the key length is the average of this scores. Both the individual shift values and the overall score are returned.'''
    # divide the text into trenches
    categories = [""]*l
    for i in range(len(c_mod)):
        categories[i%l] += c_mod[i]

    # collect the individual shift scores and average them
    shifts = [getShift(str, r_freq) for str in categories]
    sum = 0
    for item in shifts:
        sum += item[1]
    score = sum/len(shifts)
    
    return shifts, score

def getFactors(num):
    '''Finds al factors of a given number.'''
    factors = []
    for i in range(1, num+1):
        if num%i == 0:
            factors.append(i)
    return factors

def findPattern(list):
    '''Finds the shortest repeating pattern in a list of elements.'''
    shortest = [] 
    if len(list) <= 1: 
        return list
    if len(set(list)) == len(list): 
        return list
    factors = getFactors(len(list))
    # loop through factors until pattern is found
    for f in factors:
        if list[0:f]*(int(len(list)/f)) == list:
            return list[0:f] 
    return shortest

def breakVigenere(c, r):
    r_mod, c_mod = processFile(r), load_file(c)

    if len(r_mod) < 1 or len(c_mod) < 1:
        print("File is empty")
        quit()

    r_freq = getLetterFreq(r_mod)


    #find most probable key length (1-100) and the shift associated with it
    max = 0
    shifts = []
    for i in range(1,100):
        curr_sh, curr_score = getKeyLengthScore(i, c_mod, r_freq)
        if curr_score > max:
            max, shifts = curr_score, curr_sh

    #find pattern of key
    key = []
    for s in shifts:
        key.append(s[0])
    key = findPattern(key)

    #decipher key
    letterKey = ""
    for num in key:
        letterKey += int2ltr(26-num)

    #translating
    plaintext = ""
    for i in range(len(c_mod)):
        shift = key[i % len(key)]
        if c_mod[i] in ALPHABET:
            plaintext += int2ltr(ltr2int(c_mod[i]) + shift).upper()
        elif c_mod[i] in alphabet:
            plaintext += int2ltr(ltr2int(c_mod[i]) + shift).lower()
        else:
            plaintext += c_mod[i]
    
    return plaintext

def main():
    caesarian = open("decrypted_caesar.txt", "w")
    deciphered = breakCaesar('caesar.txt', "shakespeare.txt")
    caesarian.write(deciphered)
    caesarian.close()

    vigenere = open("decrypted_vigenere.txt", "w")
    deciphered2 = breakVigenere("vigenere.txt", "shakespeare.txt")
    vigenere.write(deciphered2)
    vigenere.close()


if __name__ == "__main__":
    main()
