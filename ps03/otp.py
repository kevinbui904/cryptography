import random

CHAR_LEN = 8

def ltr2bin(ch):
    '''Translate characters to length 8 binary strings.
    Turn anything with a value over 255 into a space.'''
    if ord(ch) > 255:
        ch = " "
    return format(ord(ch), '0' + str(CHAR_LEN) + 'b')

def bin2ltr(bin_str):
    '''Translate binary string of length 8 to character'''
    if len(bin_str) != CHAR_LEN:
        raise Exception("Binary string should be length " + str(CHAR_LEN))
    return chr(int(bin_str, 2))

def text_to_binary(text):
    '''Convert text to a binary string''' 
    return ''.join(ltr2bin(ch) for ch in text)

def binary_to_text(bin_str):
    '''Convert binary string to text.'''
    if len(bin_str) % CHAR_LEN != 0:
        raise Exception("Binary string length should be divisible by " + str(CHAR_LEN))
    return ''.join(bin2ltr(bin_str[i:i+CHAR_LEN]) for i in range(0, len(bin_str), CHAR_LEN))

def char_xor(a, b):
    ''' Return the xor of two binary characters.'''
    return '1' if a != b else '0'