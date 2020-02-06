import random
import string

def Scramble(max_len,string):
	i=0
	string_scr = str()
	string_list = string.split(" ")
	while i<max_length:
		w = str()
		for word in string_list:
			try:
				w += word[i]
			except IndexError:
				w += "_"
		string_scr += w + " "
		i+=1
	string_scr = string_scr[:-1]
	return string_scr[::-1]

def Arrange(max_len,string):
	string_arr = Scramble(max_len,string).replace("_","")
	string_arr_list = string_arr.split(" ")
	words = len(string_arr_list)
	n = max_length + (max_length - words) + 1
	return string_arr[n:]

s = "benim adım alperen gencoglu"

s_list = s.split(" ")
max_length = len(s_list[0])

for word in s_list:
	if len(word)>max_length:
		max_length=len(word)	
q = str()
for i in range(max_length):
	q += random.choice(string.ascii_letters)

s = q + " " + s

print(max_length)
print(s)

s_scr = Scramble(max_length,s)
print(s_scr)

s_arr = Arrange(max_length,s_scr)
print(s_arr)