#my_test.py
#Author: Adela Dujsikova and Thien K. M. Bui
#To be used for testing legend.txt with caesar and vigenere encryption


from collections import defaultdict
import random
# ----- UTILITY FUNCTIONS ---------------------------------------------------- #

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet = "abcdefghijklmnopqrstuvwxyz"

def ltr2int(ch):
    '''Translate letters (upper or lower case) to indices {0, 1, ..., 25}'''
    return ord(ch.upper()) - ord('A')

def int2ltr(i):
    '''Translate indices {0, 1, ..., 25, 26=0, 27=1, ...} to (upper case)
       letters, wrapping around as necessary.'''
    return chr(i % 26 + ord('A'))

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
    counts = defaultdict(int)
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n].upper()
        if ngram.isalpha():
            counts[ngram.upper()] += 1
    return counts


# ----- SUBSTITUTION CIPHERS-------------------------------------------------- #
#
# Note: all of these functions are "curried", in the sense that they
# take a key as an argument first, and then return a function that
# enciphers plaintext.  So the usage is
#
#     ciphertext = cipher(key)(plaintext)  # note:  NOT cipher(key,plaintext).
#
# This allows the slow-to-compute ciphers [e.g., one that counts frequencies
# in a reference text] to be reused on multiple plaintexts without recompution.
#
# Also note that all non-alphabetical characters, including spaces, remain
# intact in these implementations.  This would be easy to fix but introduces
# the problem of segmentation of any computationally cracked ciphers -- a pain!


def caesar(shift):
    '''Caesar Cipher: each letter in the plaintext is shifted forward in
       the alphabet by the designated number of letters, wrapping
       around as necessary.  E.g., with a shift of 2, we have A -> C,
       B -> D, ..., X -> Z, Y -> A.  This version maintains plaintext's case.'''

    def encipher(plaintext):
        ciphertext = ""
        for ch in plaintext:
            if ch in ALPHABET:
                ciphertext += int2ltr(ltr2int(ch) + shift)
            elif ch in alphabet:
                ciphertext += int2ltr(ltr2int(ch) + shift).lower()
            else:
                ciphertext += ch
        return ciphertext
    return encipher


def substitution_cipher(starter_key):
    '''Substitution Cipher: the key is a permutation of the alphabet; each
       letter in the plaintext is replaced by its corresponding letter
       in the permutation.  For example, the key "HJDAXGFYBMWONTCVLRQUKSZEPI"
       causes A->H, B->J, C->D, etc.  This code can be used in two ways:

        1) random mode.  If called with key=None, then a random permutation 
           of the alphabet is chosen and used.

        2) key mode.  If called with key != None, then the key
           permutation is derived from the letters in the given key in
           order (deleting duplicates), with any letters missing
           filled in alphabetical order.  For example, for the key ADALOVELACE:
           ADALOVELACE -> ADLOVEC -> ADLOVECBFGHIJKMNPQRSTUWXYZ.

       In either case, this encryption maintains plaintext's case.'''

    if starter_key == None:   
        key = "".join(random.sample(list(ALPHABET),26))  # randomization mode.
    else:                     
        key = starter_key + ALPHABET                     # starter key mode. 
        key = "".join(key[i] for i in range(len(key))    
                      if key[i] not in starter_key[:i])  # (removes duplicates.)

    def encipher(plaintext):
        ciphertext = ""
        for ch in plaintext:
            if ch in ALPHABET:
                ciphertext += key[ltr2int(ch)]
            elif ch in alphabet:
                ciphertext += key[ltr2int(ch)].lower()
            else:
                ciphertext += ch
        return ciphertext
    return encipher


def vigenere(key):
    '''Vigenere Cipher: an interleaved sequence of Caesar shifts; the key
       tells us WHICH Caesar shift to apply to each letter of the plaintext.
       Specifically, the (i)th letter of plaintext is shifted by the (i)th 
       letter of the key -- or, really, by the (i % len(key))th letter of the 
       key.  For example, with the key GRACE and the plaintext HOPPERHOPPER:

          H O P P E R H O P P E R
        + G R A C E|G R A C E|G R
        -------------------------
          N F P R I X Y O R T K I     (For example, P + C = 15 + 2 = 17 = R.)

       This encryption maintains plaintext's case.'''
    
    def encipher(plaintext):
        ciphertext = ""
        for i in range(len(plaintext)):
            shift = ltr2int(key[i % len(key)])
            if plaintext[i] in ALPHABET:
                ciphertext += int2ltr(ltr2int(plaintext[i]) + shift)
            elif plaintext[i] in alphabet:
                ciphertext += int2ltr(ltr2int(plaintext[i]) + shift).lower()
            else:
                ciphertext += plaintext[i]
        return ciphertext
    return encipher
    
def main():

    with open("legend.txt", "r") as f:
        raw_txt = "".join(line for line in f)

    caesar_file = open("enciphered_caesar.txt", "w")
    enciphered_caesar = caesar(random.randint(0,25))(raw_txt)
    caesar_file.write(enciphered_caesar)
    caesar_file.close()

    vigenere_file = open("enc_vig.txt", "w")
    enc_vig = vigenere("T")(raw_txt)
    vigenere_file.write(enc_vig)
    vigenere_file.close()

if __name__ == "__main__":
    main()