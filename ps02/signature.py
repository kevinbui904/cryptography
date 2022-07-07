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

#signature()
# @param lst, dictionary of nodes
# @return list of ints detailing the length of each nodes cycle

def signature(lst):
    node_graph = lst
    signature = []

    keys = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q'
            ,'R','S','T','U','V','W','X','Y','Z']

    cycle = []
    
    for key in keys:
        if key in node_graph.keys():
            while key in node_graph.keys():
                cycle.append(key)
                value = node_graph[key]
                del node_graph[key]
                key = value
            signature.append(len(cycle))
            cycle = []
    
    return signature

#calc
def main():
    rotors = ['I','II','III','IV','V']
    helptext = "Compute the signature given the config of an enigma machine.  " + \
        "Specify rotors from left to right (slow to fast).\n" + \
        "E.g. III is the slow rotor in [python enigma.py ABCDEF III II I ADO]"

    parser = argparse.ArgumentParser(description=helptext)
    parser.add_argument('slow_rotor', help="slow [left] rotor", choices=rotors)
    parser.add_argument('medium_rotor', help="middle rotor", choices=rotors)
    parser.add_argument('fast_rotor', help="fast [right] rotor", choices=rotors)
    parser.add_argument('initial_rotor_settings', type=str)

    args = parser.parse_args()
    if len(set([args.slow_rotor,args.medium_rotor,args.fast_rotor])) != 3:
        raise ValueError("You cannot reuse a rotor.")
        
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
    

if __name__ == "__main__":
    main()