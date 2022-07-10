#parser.py
#used to parse out signature and display relevant information
#Cryptography, Carleton College Summer '22

def main():
    file = open("signatures.txt", "r")

    sig_map = {}

    for line in file:
        ln = file.readline()
        ln = ln.replace("[","")
        ln = ln.replace("]","")
        ln = ln.replace("\n","")
        ln = ln.split(",")

        #turn signature into a hashable string for dict
        sort = []
        for ch in ln[1:]:
            sort.append(int(ch))

        sort = sorted(sort, reverse=True)
        
        key = ""
        for ch in sort:
            key += str(ch) + " "
        if key in sig_map.keys():
            sig_map[key].append(ln[0])
        else:
            new_lst = []
            new_lst.append(ln[0])
            sig_map[key] = new_lst

    histogram = {}
    for key in sig_map:
        histogram[key] = len(sig_map[key])
    
    histogram = dict(sorted(histogram.items(),key= lambda x:x[1], reverse=True))
    print(histogram)
    


if __name__ == "__main__":
    main()