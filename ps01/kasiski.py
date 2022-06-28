# kasiski.py
# Kasiski examination to decode Vigenere Ciphers
#
# CS 341 Cryptography, Carleton College
# David Liben-Nowell (dln@carleton.edu)
# Adela Dujsikova and Thien K. M. Bui

from collections import defaultdict

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
def getShift(str, r_freq):
    '''Returns both the shift amount and the score for that shift for a specific string and reference frequencies.'''
    c_freq = count_Ngram_frequency(str, 1)
    max = 0
    my_shift = 0
    for shift in range(26):
        curr = test(shift, c_freq, r_freq)
        if curr > max:
            max, my_shift = curr, shift

    return (my_shift, max)

def get_key_shifts(l, c_mod, r_freq):
    categories = [""]*l
    for i in range(len(c_mod)):
        categories[i%l] += c_mod[i]

    shifts = [getShift(str, r_freq) for str in categories]
    return shifts
def main():
    cipher = load_file("vigenere.txt")
    reference = processFile("shakespeare.txt")

    #for frequency analysis later
    r_freq = getLetterFreq(reference)

    #find all the repeating strings
    freq_dict = count_Ngram_frequency(cipher, 3)

    sorted_by_freq=dict(sorted(freq_dict.items(),key= lambda x:x[1], reverse=True))

    print(sorted_by_freq)
    #figure out how far apart these bigrams are 
    for key in freq_dict:
        freq_dict[key] = []
        space_btw = 1
        for i in range(len(cipher)):
            ngram = cipher[i:i+3].upper()
            if ngram == key:
                freq_dict[key].append(space_btw)
                space_btw = 1
            else:
                space_btw += 1
 
    combined_distances = []
    lst = list(sorted_by_freq.keys())

    for i in range(10):
        combined_distances = combined_distances + freq_dict[lst[i]][1:]
    

    min_distance = int(min(combined_distances))
    print(min_distance)
    factors_lst = []
    for i in range(1,min_distance+1):
        if min_distance % i == 0:
            factors_lst.append(i)
    
    cur_biggest = factors_lst[0]
    for i in factors_lst:
        for j in combined_distances:
            if j % i == 0 and i > cur_biggest:
                cur_biggest = i
            elif j % i != 0:
                break
    print(cur_biggest)

    #break vigenere
    shifts = get_key_shifts(cur_biggest, cipher, r_freq)
    key = []
    for s in shifts:
        key.append(s[0])

    letterKey = ""
    for num in key:
        letterKey += int2ltr(26-num)
    print(letterKey)

    plaintext = ""
    for i in range(len(cipher)):
        shift = key[i % len(key)]
        if cipher[i] in ALPHABET:
            plaintext += int2ltr(ltr2int(cipher[i]) + shift).upper()
        elif cipher[i] in alphabet:
            plaintext += int2ltr(ltr2int(cipher[i]) + shift).lower()
        else:
            plaintext += cipher[i]
    print(plaintext)
    
    return plaintext




if __name__ == "__main__":
    main()