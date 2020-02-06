from random import randint
from math import log
import sys

# ord(): convert a character to its ascii value
# chr(): convert an ascii value to the character 
# bin() can be used instead of DecToBnry function
# int() can be used instead of BnryToDec function

def DecToBnry(dec):
	if dec==0:
		return 0
	result = ""
	negative = False
	if dec<0:
		negative = True
		dec = abs(dec)
	while dec > 0:
		result += str(dec%2)
		dec //= 2
	if negative:
		result += "-"
	result = int(result[::-1])
	return result

def BnryToDec(bnry):
	result = 0
	ctr = 0
	negative = False
	if bnry<0:
		negative = True
		bnry = abs(bnry)
	while bnry>0:
		result += (bnry%10) * (2**ctr)
		bnry //= 10
		ctr+=1
	if negative:
		result = -result
	return result

def encrypt(s,level,key):
	s_list = list(s)
	for i in range(len(s_list)):
		leveltemp = level
		if 'a' <= s_list[i] <= 'z':
			if (ord(s_list[i])-leveltemp < ord('a')):
				leveltemp -= ord('a')-(ord(s_list[i])-leveltemp)
			if (ord(s_list[i])+leveltemp > ord('z')):
				leveltemp -= (ord(s_list[i])+leveltemp)-ord('z')
			randomize = randint(-leveltemp,leveltemp)
			key.append( keyEncrypt(randomize) )
			s_list[i] = chr(ord(s_list[i])+randomize)
		elif 'A' <= s_list[i] <= 'Z':
			if (ord(s_list[i])-leveltemp < ord('A')):
				leveltemp -= ord('A')-(ord(s_list[i])-leveltemp)
			if (ord(s_list[i])+leveltemp > ord('Z')):
				leveltemp -= (ord(s_list[i])+leveltemp)-ord('Z')
			randomize = randint(-leveltemp,leveltemp)
			key.append( keyEncrypt(randomize) )
			s_list[i] = chr(ord(s_list[i])+randomize)
		else:
			key.append(0)
	s_crypted = "".join(s_list)
	return s_crypted

def encryptAll(s,level,key):
	s_list = list(s)
	for i in range(len(s_list)):
		leveltemp = level
		if (ord(s_list[i])-leveltemp < 0):
			leveltemp -= 0 - (ord(s_list[i])-leveltemp)
		if (ord(s_list[i])+leveltemp > 127):
			leveltemp -= (ord(s_list[i])+leveltemp) - 127
		#try	
		randomize = randint(-leveltemp,leveltemp)
		key.append( keyEncrypt(randomize) )
		s_list[i] = chr(ord(s_list[i])+randomize)
	s_crypted = "".join(s_list)
	return s_crypted
	

def decrypt(s,key):
	s_list = list(s)
	for i in range(len(s_list)):
		s_list[i] = chr( ord(s_list[i]) - keyDecrypt(key[i]) )
	s_decrypted = "".join(s_list)
	return s_decrypted

def keyEncrypt(num):
	if num<0:
		return "-" + hex( DecToBnry(DecToBnry(num)) ).split('x')[-1]
	else:
		return hex( DecToBnry(DecToBnry(num)) ).split('x')[-1]
		
def keyDecrypt(key):
	return BnryToDec(BnryToDec(int(str(key),16)))










# main
print("""
####                                   ####
#### Welcome to Encryptor, by appleren ####
####                                   ####""")

# "pijamalı hasta yağız şoföre çabucak güvendi"

invalid_ctr = 0
while True:

	operation = input("\nSelect Operation: (1)Encryption | (2)Decryption\n> ")

	# Encryption
	if operation=="1":
		print("\n\n~~~ ENCRYPTION ~~~")
		string = input("> Enter the string to be encrypted:\n> ")
		enc_type = int(input("> Select the encryption type: (1)Letters Only | (2)All characters \n> ")) - 1
		key = list()
		level = -1
		while not (1<=level<=5):
			try:
				level = int(input("> Set a level (1 to 5) for encryption:\n> "))
			except ValueError:
				print("Level must be an integer!")
				
		if not enc_type: # letters only
			if level==1:
				level=1
			elif level==2:
				level=3
			elif level==3:
				level=6
			elif level==4:
				level=9
			elif level==5:
				level=12
			string_encrypted = encrypt(string,level,key)							

		else: # all characters
			if level==1:
				level=1
			elif level==2:
				level=6
			elif level==3:
				level=16
			elif level==4:
				level=32
			elif level==5:
				level=63
			string_encrypted = encryptAll(string,level,key)
		
		string_decrypted = decrypt(string_encrypted,key)

		print("\n--> Encrypted string:\n",string_encrypted,sep="")
		print("\n--> Key:")
		print(*key,sep=",")
		print("\n--> Decrypted string:\n",string_decrypted,sep="")
		print("\n")
	# Encryption end
	
	# Decryption
	elif operation=="2":
		print("\n\n~~~ DECRYPTION ~~~")
		string_encrypted = input("> Enter the encrypted string:\n> ")
		key = input("> Enter the key:\n> ").split(",")

		string_decrypted = decrypt(string_encrypted,key)
		print("\n--> Decrypted string:\n",string_decrypted,sep="")
		print("\n")
	# Decryption end

	# Quit
	elif operation=="*" or operation=="q" or operation=="Q":
		print("Quiting...")
		sys.exit(0)
	# Quit end
		
	# Invalid selection
	else:
		invalid_ctr+=1
		print("Invalid selection. Please try again.")

		if invalid_ctr>100:
			print("Over 100 invalid selections, Congratulations!!\nYou can quit if you do not want to use the app. Let me help you.")
			sys.exit(0)
	# Invalid selection end




