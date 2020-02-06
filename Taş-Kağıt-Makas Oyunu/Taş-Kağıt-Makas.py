print("""

	""")

from time import sleep
from random import choice

klasik = ["TAŞ","KAĞIT","MAKAS"]
modern = ["TAŞ","KAĞIT","MAKAS","KERTENKELE","UZAYLI"]

#FONKSİYONLAR
def skorYazdır(oyuncu,bilgisayar):
	print("Oyuncu {} | {} Bilgisayar".format(oyuncu,bilgisayar))
def turSonu(hamle1_sayı,hamle2_sayı,hamle1,hamle2):
	if hamle1_sayı == hamle2_sayı:
		durum = "Tur Berabere"
	elif (hamle1_sayı == hamle2_sayı+1) or (hamle1_sayı == hamle2_sayı-2):
		durum = "Turu Oyuncu Kazandı"
	elif (hamle1_sayı+1 == hamle2_sayı) or (hamle1_sayı-2 == hamle2_sayı):
		durum = "Turu Bilgisayar Kazandı"
	print("Oyuncu: {} ---  Bilgisayar: {} | {}".format('%-5s'%hamle1, '%-5s'%hamle2, durum))	
	if durum == "Turu Oyuncu Kazandı":
		return 1
	elif durum == "Turu Bilgisayar Kazandı":
		return 2
	else:
		return 0	
#FONKSİYONLAR BİTİŞ

while True:
	seçim = input("\n Oyun Modu Seçin (1/2)\n ? ")
	
	#KLASİK OYUN MODU
	if seçim == "1":
		print("  >> Oyun Modu: Klasik\n  >> Çıkmak İçin '*' Girebilirsiniz")

		#AYARLAR
		oyuncu = 0
		bilgisayar = 0
		bitiş = int(input("Oyunun Biteceği Puan Sınırını Girin: "))
		uzatma = input("Uzatmalar olsun mu (E/H)? ")
		if uzatma=="e" or uzatma=="E" or uzatma=="1":
			uzatma=1
		else:
			uzatma=0
		#AYARLAR BİTİŞ	

		while True:
			hamle_sayı = input("\n Hamleniz (1/2/3)? ")
			if hamle_sayı=="*":
				print("Oyundan Çıkıldı.")
				break
			hamle_sayı = int(hamle_sayı)
			hamle = klasik[hamle_sayı-1]
			pchamle = choice(klasik)
			pchamle_sayı = klasik.index(pchamle)+1
			
			tur_sonu = turSonu(hamle_sayı,pchamle_sayı,hamle,pchamle)
			if tur_sonu == 1:
				oyuncu+=1
			elif tur_sonu==2:
				bilgisayar+=1

			skorYazdır(oyuncu,bilgisayar)	
			
			if (uzatma) and (oyuncu==bitiş-1) and (bilgisayar==bitiş-1):
				bitiş+=1
			if oyuncu==bitiş:
				print("\n   Oyun Bitti. OYUNCU KAZANDI!")
				break
			elif bilgisayar==bitiş:
				print("\n   Oyun Bitti. BİLGİSAYAR KAZANDI!")
				break
	#KLASİK OYUN MODU BİTİŞ			

	#MODERN OYUN MODU
	elif seçim == "2":
		print("  >> Oyun Modu: Modern\n  >> Çıkmak İçin '*' Girebilirsiniz")

		#AYARLAR
		oyuncu = 0
		bilgisayar = 0
		bitiş = int(input("Oyunun Biteceği Puan Sınırını Girin: "))
		uzatma = input("Uzatmalar olsun mu (E/H)? ")
		if uzatma in ("e", "E", "1"):
			uzatma=1
		else:
			uzatma=0
		#AYARLAR BİTİŞ	

		while True:
			hamle_sayı = input("\n Hamleniz (1/2/3/4/5)? ")
			if hamle_sayı=="*":
				print("Oyundan Çıkıldı.")
				break
			hamle_sayı = int(hamle_sayı)
			hamle = modern[hamle_sayı-1]
			pchamle = choice(modern)
			pchamle_sayı = modern.index(pchamle)+1
			



	#MODERN OYUN MODU BİTİŞ	

	else:
		pass
