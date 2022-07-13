#parse_more.py
#given a full suite of signatures, calculate the
#secondary and tertiary signatures
#and write out onto another file

ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q'
            ,'R','S','T','U','V','W','X','Y','Z']

#get_next()
#return the next key in the sequence (e.g. AAA --> AAB, ZZZ --> AAA)
def get_next(key):
    reversed = key[::-1]
    next = ""
    for ch in reversed:
        index = ALPHABET.index(ch)

        if index == 25:
            next += "A"
        else:
            next += ALPHABET[index+1]
            break
    
    if len(next) == 3:
        return next[::-1]
    else:
        return key[0:3-len(next)] + next[::-1]
    
def main():
    file = open("signatures.txt", "r")

    #parse signatures into big dictionary of format
    #configuration

    sig_map = {}

    for line in file:
        ln = line
        ln = ln.replace("[","")
        ln = ln.replace("]","")
        ln = ln.replace("\n","")
        ln = ln.split(",")

        #turn signature into a hashable string for dict
        sort = []
        for ch in ln[1:]:
            sort.append(int(ch))

        sort = sorted(sort, reverse=True)
        
        value = ""
        for ch in sort:
            value += str(ch) + " "
        
        key = ln[0]

        sig_map[key] = value
    
    #construct the secondary (1 and 4) and tertiary (2 and 5)
    #signatures
    rotors = ['I','II','III','IV','V']

    histogram = {}    
    
    for slow in rotors:
        for med in rotors:
            if med != slow:
                for fast in rotors:
                    if fast != slow and fast != med:
                        for first_ltr in ALPHABET:
                            for second_ltr in ALPHABET:
                                for third_ltr in ALPHABET:
                                    prim_key = first_ltr+second_ltr+third_ltr
                                    sec_key = get_next(prim_key)
                                    ter_key = get_next(sec_key)

                                    first = slow + " " + med + " " + fast + " " + "\""+ prim_key+"\""
                                    second = slow + " " + med + " " + fast + " " + "\""+ sec_key+"\""
                                    third = slow + " " + med + " " + fast + " " + "\""+ ter_key+"\""

                                    key = sig_map[first] + sig_map[second] + sig_map[third]

                                    if key in histogram.keys():
                                        histogram[key] += 1
                                    else:
                                        histogram[key] = 1

    histogram = dict(sorted(histogram.items(),key= lambda x:x[1], reverse=True))

    result_file = open("parsed_more.txt", "w")
    for key in histogram:
        txt = key + ":" + str(histogram[key]) + "\n"
        result_file.write(txt)
    
    #percentage of most common keys
    cur_max = 0
    for key in histogram:
        cur_max = max(histogram[key], cur_max)
    
    print(cur_max / 1054560)

    expected_value = 0
    for key in histogram:
        keys_shared = histogram[key]
        expected_value += keys_shared * keys_shared
    
    expected_value = expected_value / 1054560
    
    print(expected_value)  
                                       
if __name__ == "__main__":
    main()