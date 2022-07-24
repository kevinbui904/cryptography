import otp

def main():
    f1 = open("ciphertext1.txt","r")
    # for line in c1:
    #     bin = ""
    #     for i in range(len(line)):
    #         bin += line[i]
    #         if len(bin) == 8:
    #             print(otp.bin2ltr(bin))
    #             bin = ""
    c1 = ""
    c2 = ""
    c3 = ""
    for line in f1:
        c1 += line

    f1.close()

    f2 = open("ciphertext2.txt", "r")
    for line in f2:
        c2 += line

    f2.close()

    f3 = open("ciphertext3.txt","r")

    for line in f3:
        c3 += line

    f3.close()

    if len(c1) == len(c2) and len(c2) == len(c3):
        print("ok")
        print(len(c1))
    
    xor = otp.char_xor(c1,c2)
    xor2 = otp.char_xor(c2,c3)
    xor3 = otp.char_xor(c1,c3)

    if xor == xor2 and xor2 == xor3:
        print("key are the same")
    
    words_file = open("dictionary.txt","r")
    words_binary = []
    for line in words_file:
        word = otp.text_to_binary(line)
        words_binary.append(word)
    
    print(len(words_binary))
    
        


    print("hello world")

if __name__ == "__main__":
    main()