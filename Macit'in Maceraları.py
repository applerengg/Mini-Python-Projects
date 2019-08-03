from random import randint
from random import choice
from time import sleep


def mücadele(macit,m1,m2,düşman,d1,d2):
    durum = 0
    sayaç = 0
    while True:
        sayaç += 1
        macit_vuruş = randint(m1,m2)
        print("\n{} {} vuruyor".format(macit,macit_vuruş))
        sleep(0.3)
        düşman_vuruş = randint(d1,d2)
        print("{} {} vuruyor".format(düşman,düşman_vuruş))
        sleep(0.3)
        
        fark = macit_vuruş - düşman_vuruş
        durum += fark
        durum -= 0.2

        print("Durum:","{0:.2f}".format(durum))
        sleep(1)

        if durum >= 10:
            sleep(1)
            print("\nMacit Kazandı!")
            return macit
            
        elif durum <= -10:
            sleep(1)
            print("\nMacit Öldü :(")
            return düşman
               
        if sayaç==30:
            sleep(1)
            print("\n{} kaçtı!".format(düşman))    
            return düşman
            
macit="macit"
svy1düşman = ["Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi","Zombi",]

while True:
    eylem = input("\n 1-savaş    2-shop\n")
    if eylem == "1":

        while True:
            sonuç = mücadele(macit,10,10,"canavar",3,5)
            if sonuç == macit:
                break
            else:
                continue    

    elif eylem == "2":
        print("\nshop")    

    else:
        print("GEÇERSİZ EYLEM")            






