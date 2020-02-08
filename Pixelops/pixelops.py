import cv2		# image operations
import numpy as np 	# arrays
from random import randint	# random integer
import os	# scan directory 
import sys	# exit program

def random_pixel(rows, cols):
	row = randint(0, rows-1)
	col = randint(0, cols-1)
	return (row, col)

### Default values:
mode = "1"
speed = 100
brush_shape = "snowflake"
filename = "watch.jpg"

filename = input("??> Enter filename for the image, or '0' for random selection: ")
if filename == "":
	filename = "watch.jpg"
elif filename == "0":
	pass	# TODO

try:
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	if img.size == 0:
		raise Exception
except Exception as e:
	print("!!> Image file cannot be opened, quiting...")
	sys.exit(0)

print(">>> Image: {}".format(filename))

while 1:
	mode = input("??> Select Mode:\n(1)Create image\n(2)Erase image\n")
	if mode in ["1", "2"]:
		break

while 1:
	try:
		speed = int(input("??> Enter speed (Brush strokes per second, max 1000): "))
		break
	except ValueError as e:
		print("!!> Speed must be integer")
		continue



dimensions = img.shape
rows = dimensions[0]; cols = dimensions[1]

img_black = np.zeros(dimensions, np.uint8)

res = img_black


if mode == "2":
	img, res = res, img

while 1:
	c = random_pixel(rows, cols) # coordinate
	res[c] = img[c]

	if brush_shape == "snowflake":
		for i in range(1, randint(2,10)):
			try:
				c2 = (c[0]+i,c[1])
				res[c2] = img[c2]
				c2 = (c[0]+i,c[1]+i)
				res[c2] = img[c2]
				c2 = (c[0],c[1]+i)
				res[c2] = img[c2]
				c2 = (c[0]-i,c[1])
				res[c2] = img[c2]
				c2 = (c[0]-i,c[1]-i)
				res[c2] = img[c2]
				c2 = (c[0],c[1]-i)
				res[c2] = img[c2]
				c2 = (c[0]+i,c[1]-i)
				res[c2] = img[c2]
				c2 = (c[0]-i,c[1]+i)
				res[c2] = img[c2]
			except IndexError as e:
				break

	if brush_shape == "square":
		try:
			size = randint(1,10)
			roi = img[ c[0]:c[0]+size, c[1]:c[1]+size ]
			res[ c[0]:c[0]+size, c[1]:c[1]+size ] = roi
		except IndexError as e:
			pass


	if brush_shape == "circle":
		pass

	
	cv2.imshow("res", res)
	
	k = cv2.waitKey(1000//speed) & 0xFF
	if k==27:
		break

cv2.destroyAllWindows()
cv2.imshow("Final Image", res)
print("\n>>> Final image is on the screen. Press any key on the image window to continue.")
cv2.waitKey(0)


save = input("??> Do you want to save this image?\n")
if save.lower() in ["y", "yes", "yep", "1", "true", "ok"
	"olur", "tamam", "yaparım", "usta"]:	### :) :)
	outfilename = input("??> Enter filename:\n")
	try:
		cv2.imwrite(outfilename + ".png", res)
		print(">>> The image is saved!")
	except Exception as e:
		print("!!> An error occured.")

print(">>> Press ESC on the image window to exit.")
cv2.waitKey(0)
