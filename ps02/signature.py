#signature.py
#compute Enigma signature give na configuration

import argparse
from enigma import enigma 

KEYS = [
    "AAAAAA",
    "BBBBBB",
    "CCCCCC",
    "DDDDDD",
    "EEEEEE",
    "FFFFFF",
    "GGGGGG",
    "HHHHHH",
    "IIIIII",
    "JJJJJJ",
    "KKKKKK",
    "LLLLLL",
    "MMMMMM",
    "NNNNNN",
    "OOOOOO",
    "PPPPPP",
    "QQQQQQ",
    "RRRRRR",
    "SSSSSS",
    "TTTTTT",
    "UUUUUU",
    "VVVVVV",
    "WWWWWW",
    "XXXXXX",
    "YYYYYY",
    "ZZZZZZ"
]

ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q'
            ,'R','S','T','U','V','W','X','Y','Z']

#build_graph()
# @param lst , list of messages
# @return graph, dictionary graph containing all links from each encryption
#look at the 0th and 3rd letter of each message in the lst
#to build out a graph
def build_graph(lst):
    graph = {}
    for message in lst:
        graph[message[0]] = message[3]
    return graph

def signature(lst):
    node_graph = lst
    signature = []


    cycle = []
    
    for letter in ALPHABET:
        if letter in node_graph.keys():
            while letter in node_graph.keys():
                cycle.append(letter)
                value = node_graph[letter]
                del node_graph[letter]
                letter = value
            signature.append(len(cycle))
            cycle = []
    
    return signature


#calc
def main():
    rotors = ['I','II','III','IV','V']
    helptext = "Compute the signature given the config of an enigma machine.  " + \
        "Specify rotors from left to right (slow to fast).\n" + \
        "E.g. III is the slow rotor in [python enigma.py ABCDEF III II I ADO]"


    config = ['m', 'c']
    parser = argparse.ArgumentParser(description=helptext)
    parser.add_argument('config', help="m for manual testing, c for problem 4. -c will ignore all subsequent inputs", choices=config)
    parser.add_argument('slow_rotor', help="slow [left] rotor", choices=rotors)
    parser.add_argument('medium_rotor', help="middle rotor", choices=rotors)
    parser.add_argument('fast_rotor', help="fast [right] rotor", choices=rotors)
    parser.add_argument('initial_rotor_settings', type=str)

    args = parser.parse_args()
    if len(set([args.slow_rotor,args.medium_rotor,args.fast_rotor])) != 3:
        raise ValueError("You cannot reuse a rotor.")
        
    if args.config == 'm':

        machine = enigma(args.slow_rotor, args.medium_rotor, args.fast_rotor,
                        [], "AAA", args.initial_rotor_settings)
        
        messages = []

        #have to reset the machine after every encryption
        for key in KEYS:
            messages.append(machine(key))
            machine = enigma(args.slow_rotor, args.medium_rotor, args.fast_rotor,
                        [], "AAA", args.initial_rotor_settings)                    
        node_graph = build_graph(messages)
        print(signature(node_graph))
    
    else:    
        #write out the signature for all configuration into a new file
        #every triplet of rotors and every initial setting (5*4*3*26^3 signatures)
        file = open("signatures.txt", "w")
        
        count = 0
        #rotors
        for slow in rotors:
            for med in rotors:
                if med != slow:
                    for fast in rotors:
                        if fast != slow and fast != med:
                            for first_ltr in ALPHABET:
                                for second_ltr in ALPHABET:
                                    for third_ltr in ALPHABET:
                                        if count < 10000:
                                            count += 1
                                            messages = []

                                            machine = enigma(slow, med, fast,
                                                            [], "AAA", first_ltr+second_ltr+third_ltr)  
                                            #have to reset the machine  after every encryption
                                            for key in KEYS:
                                                messages.append(machine(key))
                                                machine = enigma(slow, med, fast,
                                                            [], "AAA", first_ltr+second_ltr+third_ltr)                    
                                            node_graph = build_graph(messages)
                                            sig = signature(node_graph)
                                            txt = slow + " " + med + " " + fast + " " + "\""+ first_ltr+second_ltr+third_ltr+"\"" + "\n" + str(sig) + "\n"
                                            file.write(txt)
                                        else:
                                            file.close()
                                            exit(1)

                                          
    

if __name__ == "__main__":
    main()