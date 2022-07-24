import otp


def decrypt(m,l):
    m_binary = otp.text_to_binary(m)
    decrypted_bin = ""

    for i in range(len(m_binary)):
        decrypted_bin += otp.char_xor(m_binary[i],l[i])
    return otp.binary_to_text(decrypted_bin)

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

    c1c2 = ""
    c2c3 = ""
    c3c1 = ""    
    for i in range(len(c1)):
        c1c2 += otp.char_xor(c1[i],c2[i])
        c2c3 += otp.char_xor(c2[i], c3[i])
        c3c1 += otp.char_xor(c3[i], c1[i])
    
    words_file = open("dictionary.txt","r")
    words_binary = set()
    for line in words_file:
        line = line.replace("\n","")
        line = line.lower()
        word = otp.text_to_binary(line)
        words_binary.add(word)
    
    print(len(words_binary))

    possible1 = set()
    possible2 = set()
    possible3 = set()

    #scan the alphabet for words that matches XOR 

    # for bin_wrd in words_binary:
    #     cipher12 = ""
    #     cipher23 = ""
    #     cipher31 = ""
    #     for i in range(len(bin_wrd)):
    #         cipher12 += otp.char_xor(bin_wrd[i], c1c2[i])
    #         cipher23 += otp.char_xor(bin_wrd[i], c2c3[i])
    #         cipher31 += otp.char_xor(bin_wrd[i], c3c1[i])
    #     if cipher12 in words_binary:
    #         word = otp.binary_to_text(cipher12)
    #         possible1.add(word)
    #         possible2.add(word)
    #     elif cipher23 in words_binary:
    #         word = otp.binary_to_text(cipher23)
    #         possible2.add(word)
    #         possible3.add(word)
    #     elif cipher31 in words_binary:
    #         word = otp.binary_to_text(cipher31)
    #         possible3.add(word)
    #         possible1.add(word)
    
    # print(possible1.intersection(possible2), ": start of 3")
    # print(possible2.intersection(possible3), ": start of 2")
    # print(possible1.intersection(possible3), ": start of 1")

    plain_txt1 = "from the Cambridge Railway Station Wikipedia article\n\nAt 514 yards (470 m), Cambridge has the third-longest railway platform in the UK on the main railway network, after Colchester and Gloucester. This platform is divided into Platforms 1 and 4 with a scissors crossover in the middle to divide it in two, which allows trains from either direction to pass those already stopped there. Bay platforms exist at both ends of the station: Platforms 2 and 3 at the southern end of the station and Platforms 5 and 6 at the northern end. Platforms 7 and 8 are located on an island platform on the eastern side of the station. These came into use in December 2011.\n\nPlatform 1 is a 12-car bi-directional through platform generally used for southbound services to London King's Cross and northbound services to King's Lynn. It is also used for some early morning northbound services to Ely and for some late evening terminating services.\n\nPlatforms 2 (10-car) and 3 (8-car) are south-facing bay platforms generally used for services to and from London King's Cross or London Liverpool Street (with some Sunday services to Stratford).\n\nPlatform 4 is a bi-directional 12-car through platform generally used for northbound services to Ely, King's Lynn and Birmingham New Street. It is also used for some early morning southbound services to London King's Cross and London Liverpool Street and for some terminating late evening services.\n\nPlatform 5 is a 6-car north-facing bay platform generally used for services to and from Norwich (and occasional services to and from Birmingham New Street).\n\nPlatform 6 is a 6-car north-facing bay platform used for services to and from Ipswich (with occasional services to and from Harwich International).\n\nPlatforms 7 and 8 are bi-directional 12-car through platforms generally used for southbound services to London King's Cross, London Liverpool Street, Stansted Airport and Brighton via London St Pancras International. These platforms are also used for longer terminating trains from London Liverpool Street and London King's Cross.\n\n"

    plain_txt2 = "the source of this text is the Wikipedia article called Cambridge University Botanic Garden\n\nBotanic Garden\nIn 1825 John Stevens Henslow, Charles Darwin's teacher at Cambridge, succeeded Martyn as professor of botany and soon realized that a larger site, farther from the centre of Cambridge, was desirable for the Botanic Garden. In 1831 the University purchased the present site of about 40 acres to the south of the town on the Trumpington Road, and in 1846 the first tree was planted. It had been the intention to lay out the whole 40 acres as a Botanic Garden, but presumably funds were lacking, and in fact only 20 acres were planted, the remainder being let out as allotments.\n\nThe planning of the new Garden was carried out by Professor Henslow, assisted by young Cardale Babington. The land was flat and unpromising as a garden site, but the layout was planned with great skill, utilizing an old gravel pit to construct a lake with a high mound running into it. Trees and shrubs were planted according to their botanical sequence, a range of glasshouses was built in the 1860s, and a rock garden, one of the earliest of its kind in the country, was constructed about the same time. The Garden has also long been known for its many fine specimens of rare trees. By the 1870s the main features of the Garden had been developed and, it was ready to play its part in the great expansion of botanical teaching and research that was about to take place at Cambridge. During the early years of the 20th century much of the pioneer work of William Bateson, Charles Chamberlain Hurst, and Edith Rebecca Saunders on plant genetics was carried out at the Garden, and it was later used for researches on plant physiology by Frederick Blackman and George Edward Briggs, and on plant pathology by Frederick Tom Brooks and others.\n\n"

    plain_txt3 = "parker's Piece\nWikipedia\n\nParker's Piece is a 25-acre flat and roughly square green common located near the centre of Cambridge, England, regarded by some as the birthplace of the rules of Association Football. The two main walking and cycling paths across it run diagonally, and the single lamp-post at the junction is colloquially known as Reality Checkpoint. The area is bounded by Park Terrace, Parkside, Gonville Place, and Regent Terrace. The Cambridge University Football Club Laws were first used on Parker's Piece and adopted by the Football Association in 1863. \"They embrace the true principles of the game, with the greatest simplicity\" (E. C. Morley, F.A. Hon. Sec. 1863). 'The Cambridge Rules appear to be the most desirable for the Association to adopt' (C. W. Alcock 1863, FA committee member and founder of the FA Cup).\n\nThe grass is mown and the area is known today chiefly as a spot for picnics and games of football and cricket, and serves as the games field for nearby Parkside Community College. Fairs tend to be held on the rougher ground of Midsummer Common. Daytime events and concerts are occasionally held on the Regent's Terrace side of Parker's Piece, while north-western quarter is still maintained as a venue for league cricket.\n\nIn 1838, a feast for 15,000 guests was held on Parker's Piece to celebrate the coronation of Queen Victoria. There is a blue plaque dedicated to Jack Hobbs on the wall of the building known locally as Hobbs Pavilion.\n\nHistory\n\nBefore 1613, Parker's Piece was owned by Trinity College. In that year, the college exchanged it with the town of Cambridge for Garrett Hostel Green, a site east of the River Cam where the Wren Library of Trinity College now stands. Parker's Piece takes its name from Edward Parker, a Trinity College cook who had leased the land from the college since 1587.\n\nAs a cricket ground, Parker's Piece was used for first-class matches from 1817 to 1864.\n\nIn the 19th century, it was one of the principal sports grounds used by students at the University of Cambridge and the site of numerous Varsity Matches against Oxford."

    # print(decrypt(plain_txt1,c1c2), ":", "cipher2")
    # print(decrypt(plain_txt1,c3c1), ":", "cipher3")
    # print("======================")
    # print(decrypt(plain_txt2,c2c3), ":", "cipher3")
    # print(decrypt(plain_txt2,c1c2), ":", "cipher1")
    # print("======================")
    print(decrypt(plain_txt3,c2c3), ":", "cipher2")
    print(decrypt(plain_txt3,c3c1), ":", "cipher1")



    
    
  




        

        



if __name__ == "__main__":
    main()