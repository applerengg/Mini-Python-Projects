print("""
#######################################################
        ADAM ASMACA OYUNUNA HOŞ GELDİNİZ!
    ****  ****  ****  ****  ****  ****  ****  
  KURALLAR:

- Oyun başladığında bir kategori seçmeniz istenir. istediğiniz
kategorinin yanındaki rakamı girerek seçim yapmış olursunuz. 
Program, seçtiğiniz kategoriden rastgele bir kelime seçer. 
Amacınız, harf tahminlerinde bulunarak kelimeyi bulmaya çalışmak.

- Harf tahmin hakkı her kelime için standart 8'dir.
Sadece yanlış tahminlerde hak azalır. 

- İpucu almak için '+' girebilirsiniz. Bu 2 hakkınıza mâl 
olacaktır ve sadece 2den fazla hakkınız varsa çalışır.Bütün
kelimelerde ipucu mevcut değildir.

- Oyundan çıkmak için '*' girebilirsiniz.

  KATEGORİLER
1. Ülkeler/Başkentler	2. Filmler
3. Meyveler/Sebzeler 	4. Hayvanlar

! Şimdilik sadece küçük harf ile çalışıyor. Program Büyük 
harfleri doğru bile olsa kabul etmez !

                ~by appleren (v1.1.3)~ 
#######################################################

	""")


from random import choice
from time import sleep
from sys import exit
sleep(0.3)
isim = input(" Oyuncu İsmi: ")
sleep(0.3)
print("\n  >>  Hoş Geldin {}!".format(isim))
sleep(0.3)

havuz_ülkeşehir = ["afganistan","kabil","arnavutluk","tiran","cezayir","cezayir","arjantin","buenosaires","avusturya","viyana","azerbaycan","bakü","bangladeş","dakka","belçika","brüksel","bolivya","lapaz","bosnahersek","saraybosna","brezilya","brasilia","bulgaristan","sofya","kanada","ottawa","şili","santiago","çin","pekin","hırvatistan","zagveb","küba","havana","kıbrıs","lefkoşa","danimarka","kopenhag","cibuti","cibuti","mısır","kahire","fransa","paris","finlandiya","helsinki","gürcistan","tiflis","almanya","berlin","yunanistan","atina","macaristan","budapeşte","hindistan","delhi","endonezya","cakarta","iran","tahran","ırak","bağdat","israil","telaviv","italya","roma","japonya","tokyo","kazakistan","astana","kuveyt","kuveyt","fas","rabat","hollanda","amsterdam","norveç","oslo","pakistan","islamabat","polonya","varşova","portekiz","lizbon","romanya","bükreş","rusya","moskova","suudiarabistan","riyad","sırbistan","belgrad","somali","mogadişu","ispanya","madrid","isveç","stokholm","isviçre","bern","suriye","şam","tayland","bangkok","tunus","tunus","türkiye","ankara","ukrayna","kiev","amerika","washington","özbekistan","taşkent","vatikan","vatikan"]



while True:
	seçim = input("\n Kategori Seçimi: ")
	if seçim == "1":
		print("\n  >>  Seçim: Ülkeler ve Başkentler")
		sleep(0.3)
		kelime = choice(havuz_ülkeşehir)
		break
	elif seçim == "2":
		print("\n  >>  Malesef bu seçenek şimdilik mevcut değil. Çok yakında gelecek!\n      Şimdilik Lütfen başka bir seçim yapın.")	
		sleep(0.3)
	elif seçim == "3":
		print("\n  >>  Malesef bu seçenek şimdilik mevcut değil. Çok yakında gelecek!\n      Şimdilik Lütfen başka bir seçim yapın.")
		sleep(0.3)
	elif seçim == "4":
		print("\n  >>  Malesef bu seçenek şimdilik mevcut değil. Çok yakında gelecek!\n      Şimdilik Lütfen başka bir seçim yapın.")
		sleep(0.3)
	else:
		print("\n  >>  Geçersiz bir değer girdiniz. Lütfen kategorileri kontrol edip tekrar deneyin.")
		sleep(0.3)

print("  >>  Rastgele Kelime Hazırlanıyor...")
sleep(1.5)


uzunluk = len(kelime)

bunu_bil = "-"*uzunluk
print("\n",bunu_bil,"|    {} Harfli".format(uzunluk))

kullanılan_harfler = []
harf_hakkı = 8
print(" > Harf Hakkı:",harf_hakkı)



while True:
	harf = input("\n\n Harf: ")
	sleep(0.3)

	if harf == "+":
		for i in range(len(havuz_ülkeşehir)):
			if i % 2 == 1 and kelime == havuz_ülkeşehir[i] and harf_hakkı > 2:
				print(" >",havuz_ülkeşehir[i-1],"başkenti")
				if not "+" in kullanılan_harfler:
					harf_hakkı -= 1
				break	
			elif i % 2 == 1 and kelime == havuz_ülkeşehir[i] and not harf_hakkı > 2:
				print("\n > Gösterilecek ipucu yok")		
				if not "+" in kullanılan_harfler:
					harf_hakkı += 1
				break
			elif i%2 == 0 and kelime == havuz_ülkeşehir[i]:
				print("\n > Gösterilecek ipucu yok")		
				if not "+" in kullanılan_harfler:
					harf_hakkı += 1
				break

	if harf == "*":
		print("\n  >>  Doğru kelime:",kelime)
		print("  >>  Oyundan Çıkılıyor...")
		sleep(1)
		exit(0)

	for i in range(0,uzunluk):
		if harf == kelime[i]:
			bunu_bil = list(bunu_bil)
			bunu_bil[i] = harf
			bunu_bil = "".join(bunu_bil)
			
		else:
			continue

	if not(harf in kullanılan_harfler):
		kullanılan_harfler.append(harf)
		if not harf in kelime:
			harf_hakkı-=1

	print("\n",bunu_bil,"|    {} Harfli".format(uzunluk))	
	print(kullanılan_harfler)
	print(" > Kalan Harf Hakkı:",harf_hakkı)

	if not "-" in bunu_bil:
		sleep(1.2)
		print("\n  >>  Kazandın, Tebrikler {}!".format(isim))
		print("  >>  Skorun:",harf_hakkı*10)
		break

	if harf_hakkı == 0:
		sleep(1.2)
		print("\n  >>  Harf Hakkın Bitti. Malesef Kaybettin {}!".format(isim))
		sleep(0.4)
		print("  >>  Doğru kelime: {}".format(kelime))
		break	


kapat = input("")

