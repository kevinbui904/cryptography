# enigma.py
# A partial implementation of an Enigma machine
#
# CS 341 Cryptography, Carleton College
# David Liben-Nowell (dln@carleton.edu)

import argparse
from substitution_ciphers import ltr2int, int2ltr, ALPHABET

# Details on the rotors as listed here are from a variety of online
# sources.  Rotor details come from Tony Sale's Codes and Ciphers.
# The "double stepping" action is explained by David Hamer and by the
# Crypography Musuem site.  Wikipedia is also (somewhat) helpful for
# some portions of this.  For more:
#
#   https://www.codesandciphers.org.uk/enigma/
#   http://web.archive.org/web/*/www.intelligenia.org/downloads/rotors1.pdf
#   https://en.wikipedia.org/wiki/Enigma_rotor_details
#   https://www.cryptomuseum.com/crypto/enigma/working.htm

ROTOR_PERMUTATIONS = {
    "I"   :       "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II"  :       "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III" :       "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV"  :       "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V"   :       "VZBRGITYUPSDNHLXAWMJQOFECK",
    "reflector" : "YRUHQSLDPXNGOKMIEBFZCWVJAT"
}

ROTOR_TURNOVERS = {
    "I"   :       "R",  # rotor I's causes its neighbor wheel to step on 
    "II"  :       "F",  #    transition from Q -> R.  Similarly, II steps
    "III" :       "W",  #    its neighbor on E -> F, III on V -> W, etc.
    "IV"  :       "K",  # Royal Flags Wave Kings Above!   
    "V"   :       "A",  # 
    "reflector" :  ""   # (reflectors never rotate)
}

class Rotor:
    def __init__(self, name, ring_setting, initial_window_setting):
        self.perm = ROTOR_PERMUTATIONS[name]
        self.notches = ROTOR_TURNOVERS[name]
        self.position = ltr2int(initial_window_setting)

        # We'll also need the inverse permutation for the letters
        # coming back through this rotor.  E.g., the inverse of
        # ABCDEFGHIJKLMNOPQRSTUVWXYZ    ABCDEFGHIJKLMNOPQRSTUVWXYZ
        # EKMFLGDQVZNTOWYHXUSPAIBRCJ is UWYGADFPVZBECKMTHXSLRINQOJ
        # as (for example) pi[A] = E <==> pi_inverse[E] = A.
        self.inverse = [None for i in range(26)]
        for i in range(26):
            self.inverse[ltr2int(self.perm[i])] = int2ltr(i)
        self.inverse = "".join(self.inverse)

    def __repr__(self):
        '''Returns the letter showing in the rotor's window.'''
        return int2ltr(self.position)

    def advance(self):
        '''Steps the rotor one position forwards.'''
        self.position = (self.position + 1) % 26

    def in_notch(self):
        '''Reports whether the rotor is sitting in a notch position, 
           aka if we and our left-hand neighbor should step on the 
           next move.'''
        return int2ltr((self.position + 1) % 26) in self.notches

    def encode(self, ch, inverted=False):
        '''Transforms ch by the rotor's permutation (or its inverse).'''
        incoming = (ltr2int(ch) + self.position) % 26
        if not inverted:
            out = (ltr2int(self.perm[incoming]) - self.position) % 26
        else:
            out = (ltr2int(self.inverse[incoming]) - self.position) % 26
        return int2ltr(out)


def enigma(slow, medi, fast,
           plugboard_pairs, ring_setting, initial_position):
    slowR = Rotor(slow, ring_setting[0], initial_position[0])
    mediR = Rotor(medi, ring_setting[1], initial_position[1])
    fastR = Rotor(fast, ring_setting[2], initial_position[2])
    reflector  = Rotor("reflector", "A", "A")

    plugboard = generate_plugboard(plugboard_pairs)

    def encipher(message, debug=False):
        output = ""
        windows, transformations = ["%s%s%s" % (slowR,mediR,fastR)], ""
        for ch in message:
            if ch in plugboard.keys():
                ch = plugboard[ch]
            transformations = transformations + ch
            mfLeverActive = fastR.in_notch()
            smLeverActive = mediR.in_notch()
            if smLeverActive: slowR.advance()
            if smLeverActive or mfLeverActive: mediR.advance()
            fastR.advance()

            windows.append("%s%s%s" % (slowR,mediR,fastR))
            for rotor in [fastR, mediR, slowR, reflector]:
                ch = rotor.encode(ch)
                transformations = transformations + " -> " + ch
            for rotor in [slowR, mediR, fastR]:
                ch = rotor.encode(ch, inverted=True)
                transformations = transformations + " -> " + ch
            if ch in plugboard.keys():
                ch = plugboard[ch]
            output += ch
            transformations = transformations + "\n"
        if debug:
            return output, " ".join(windows), transformations
        return output
        
    return encipher

#example usage: enigma("I","II","III", [("G", "B"), ("X", "Z")], "AAA", "AAZ")("G", debug=True)
def generate_plugboard(config):
    if len(config) < 1:
        return {}
    plugboard = {}
    # #we add all inputs into a list to check for existence so that a letter don't get used twice
    used_lst = []

    for pair in config:
        if len(pair) < 2:
            raise ValueError("Invalid plugboard configuration, pair of < 2.")
        else:
            for ch in pair:
                if ch in used_lst:
                    raise ValueError("Invalid plugboard configuration.")
            else:
                used_lst.append(ch)
        plugboard[pair[0]] = pair[1]
        plugboard[pair[1]] = pair[0]
    
    return plugboard


    

def main():
    rotors = ['I','II','III','IV','V']
    helptext = "Simulate an Enigma machine.  " + \
        "Specify rotors from left to right (slow to fast).\n" + \
        "E.g. III is the slow rotor in [python enigma.py ABCDEF III II I ADO]"
    parser = argparse.ArgumentParser(description=helptext)
    parser.add_argument('plaintext', type=str)
    parser.add_argument('slow_rotor', help="slow [left] rotor", choices=rotors)
    parser.add_argument('medium_rotor', help="middle rotor", choices=rotors)
    parser.add_argument('fast_rotor', help="fast [right] rotor", choices=rotors)
    parser.add_argument('initial_rotor_settings', type=str)
    parser.add_argument('plugboard_config', help="plugboad config, example \"a:b,c:d\"", type=str)

    args = parser.parse_args()
    if len(set([args.slow_rotor,args.medium_rotor,args.fast_rotor,args.plugboard_config])) != 4:
        raise ValueError("You cannot reuse a rotor.")
    

    plugboard_pairs = []

    #parse cli input so that it fits 
    #"a:b,c:d"
    #our format of [("G", "B"), ("X", "Z")]
    
    if len(args.plugboard_config) > 0:
        pairing_lst = args.plugboard_config.split(",")
        for pair in pairing_lst:
            pair = pair.split(":")
            if len(pair) < 2:
                raise ValueError("Invalid pairing format: len < 2.")

        plugboard_pairs.append((pair[0].upper(), pair[1].upper()))

    machine = enigma(args.slow_rotor, args.medium_rotor, args.fast_rotor,
                     plugboard_pairs, "AAA", args.initial_rotor_settings)
    
    print(machine(args.plaintext))




if __name__ == "__main__":
    main()

