import cv2
import sys
import pytesseract
import numpy as np


def cropImage(image):
	w,h,c = image.shape
	xmin,xmax,ymin,ymax = w,0,h,0

	for x in range(w):
		for y in range(h):
			if np.all(image[x,y] == 0):
				if x < xmin : xmin = x
				if y < ymin : ymin = y
				if x > xmax : xmax = x
				if y > ymax : ymax = y

	croppedWidth = xmax - xmin + (9 - (xmax - xmin) % 9)
	croppedHeight = ymax - ymin + (9 - (ymax - ymin) % 9)

	crop_img = image[ymin:ymin + croppedHeight , xmin:xmin + croppedWidth]

	return crop_img


def split_sudoku_cells(img):
	cells = []
	
	rows = np.split(img, 9)

	for r in rows:
		splitRow = np.split(r,9,axis = 1)
		for p in splitRow:
			cells.append(p)
	
			
	return cells

def getDigit(image):
	image = image[5:-5,5:-5]
	# image = cv2.Canny(image,100,100)
	custom_config = r'--oem 3 --psm 6 '
	

	dig = (pytesseract.image_to_string(image, config=custom_config))
	dig = [d for d in dig if d.isdigit()]
	
	if len(dig) == 0:
		return 0


	return dig[0]

def extractDigits(cells):
	soduku = ""
	for c in cells:

		soduku += str(getDigit(c))


	return soduku

def getOneLineSoduku(filename):
	img = cv2.imread(filename)
	
	img = cropImage(img)



	cells = split_sudoku_cells(img)

	oneLineSoduku = extractDigits(cells)
	return oneLineSoduku

def main(filename):	
	return (getOneLineSoduku(filename))


if __name__ == "__main__":
	main()

