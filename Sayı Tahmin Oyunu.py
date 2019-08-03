print("""
#######################################################
        SAYI TAHMİN OYUNUNA HOŞ GELDİNİZ!
    ****  ****  ****  ****  ****  ****  ****  
  KURALLAR:
- Oyun 3 Raunttan oluşmakta ve her rauntta 1-100 (her 
ikisi de dahil) arasında seçilmiş olan bir sayıyı 
bilmeye çalışacaksınız.

- Her rauntta 8 adet tahmin hakkınız olacak. Her tahminden
sonra sayının tahmininizden büyük mü küçük mü olduğu
belirtilecek.

- Sayıyı doğru bilirseniz kalan tahmin hakkınız kadar 
puan alacaksınız, eğer haklarınız biter de bilemezseniz 
puan alamayıp bir sonraki raunda geçeceksiniz.

- Raundu sonlandırıp bir sonrakine geçmek için '*'; 
Oyundan tamamen çıkmak için ise '***' girebilirsiniz.

                ~by appleren (v1.03)~
#######################################################

	""")

from random import randint
from time import sleep
from sys import exit

oyuncu = input(" Oyuncu İsmi: ")
sleep(0.1)
print("\n  >>  Hoşgeldin {}!".format(oyuncu))

skor = 0 

#1
print("    #  1. RAUNT  #")
tahmin_hakkı = 8
sayı = randint(1,100)

while True:
	tahmin = input("\n Tahmin: ")

	if tahmin == "*" or tahmin == "geç":
		print("\n >>> Geçerli Raunt Sonlandırılıyor...")
		sleep(1)
		break
	
	elif tahmin == "***" or tahmin == "çık":
		print("\n >>> Oyundan Çıkılıyor...")
		sleep(1)
		exit(0)

	else:
		tahmin = int(tahmin)

		if tahmin<sayı:
			print(" > Bilemediniz. Daha YÜKSEK bir değer deneyin.")
			tahmin_hakkı -= 1	
		elif tahmin>sayı:
			print(" > Bilemediniz. Daha DÜŞÜK bir değer deneyin.")
			tahmin_hakkı -= 1	
		else:
			print(" > Tebrikler! Doğru Cevap:",sayı)
			skor += tahmin_hakkı
			break

		if tahmin_hakkı == 0:
			print(" > Tahmin Hakkınız bitti. Doğru Cevap:",sayı)	
			break
#1

#2
print("\n  >>  1. Raunt bitti. 2. Raunt Geliyor!")
sleep(0.25)
print("  >>  Şuanki Skorunuz:",skor)
sleep(0.25)
print("  >>  Sayı yenileniyor...")
sleep(2)
print("\n\n    #  2. RAUNT  #")
tahmin_hakkı = 8
sayı = randint(1,100)

while True:
	tahmin = input("\n Tahmin: ")

	if tahmin == "*" or tahmin == "geç":
		print("\n >>> Geçerli Raunt Sonlandırılıyor...")
		sleep(1)
		break
	
	elif tahmin == "***" or tahmin == "çık":
		print("\n >>> Oyundan Çıkılıyor...")
		sleep(1)
		exit(0)
	
	else:
		tahmin = int(tahmin)

		if tahmin<sayı:
			print(" > Bilemediniz. Daha YÜKSEK bir değer deneyin.")
			tahmin_hakkı -= 1	
		elif tahmin>sayı:
			print(" > Bilemediniz. Daha DÜŞÜK bir değer deneyin.")
			tahmin_hakkı -= 1	
		else:
			print(" > Tebrikler! Doğru Cevap:",sayı)
			skor += tahmin_hakkı
			break

		if tahmin_hakkı == 0:
			print(" > Tahmin Hakkınız bitti. Doğru Cevap:",sayı)	
			break
#2

#3
print("\n  >>  2. Raunt bitti. 3. Raunt Geliyor!")
sleep(0.25)
print("  >>  Şuanki Skorunuz:",skor)
sleep(0.25)
print("  >>  Sayı yenileniyor...")
sleep(2)
print("\n\n    #  3. RAUNT  #")
tahmin_hakkı = 8
sayı = randint(1,100)

while True:
	tahmin = input("\n Tahmin: ")

	if tahmin == "*" or tahmin == "geç":
		print("\n >>> Geçerli Raunt Sonlandırılıyor...")
		sleep(1)
		break
	
	elif tahmin == "***" or tahmin == "çık":
		print("\n >>> Oyundan Çıkılıyor...")
		sleep(1)
		exit(0)
	
	#elif tahmin == oyuncu:
	#	print("\n BAŞARIM KAZANILDI: ")	

	else:
		tahmin = int(tahmin)

		if tahmin<sayı:
			print(" > Bilemediniz. Daha YÜKSEK bir değer deneyin.")
			tahmin_hakkı -= 1	
		elif tahmin>sayı:
			print(" > Bilemediniz. Daha DÜŞÜK bir değer deneyin.")
			tahmin_hakkı -= 1	
		else:
			print(" > Tebrikler! Doğru Cevap:",sayı)
			skor += tahmin_hakkı
			break

		if tahmin_hakkı == 0:
			print(" > Tahmin Hakkınız bitti. Doğru Cevap:",sayı)	
			break
#3
sleep(2)
print("\n\n >>  OYUN BİTTİ. SON SKORUNUZ: {}. TEBRİKLER {}!".format(skor,oyuncu))


kapat = input("") 

