import cv2
import sys
import pytesseract
import numpy as np

def checkHorizontalBlackLine(image,currentY,dimensions):
	h,w = dimensions



	xPoints = np.arange(0, w)
	colours = {'black': 0 , 'other': 0}
	for x in xPoints:
		# x,y = int(x),int(y)
		pixel = image[currentY,x]

		if pixel == 0:
			colours['black'] += 1
		else:
			colours['other'] += 1
	

	return colours['black'] > colours['other']

def checkVerticalBlackLine(image,currentX,dimensions):
	h,w = dimensions


	yPoints = np.arange(0, h)
	colours = {'black': 0 , 'other': 0}
	for y in yPoints:
		# x,y = int(x),int(y)
		pixel = image[y,currentX]

		if pixel == 0:
			colours['black'] += 1
		else:
			colours['other'] += 1
	

	return colours['black'] > colours['other']

def cropImage(image):
	h,w = image.shape[0]-1,image.shape[1]-1
	
	xmin,xmax,ymin,ymax = 0,w,0,h

	
	currentY = ymin
	while not checkHorizontalBlackLine(image,currentY,(h,w)) and currentY < h:
		currentY += 1

	ymin = currentY
	
	currentY = ymax
	while not checkHorizontalBlackLine(image,currentY,(h,w)) and currentY > 0:
		currentY -= 1

	ymax = currentY

	currentX = xmin
	while not checkVerticalBlackLine(image,currentX,(h,w)) and currentX < w:
		currentX += 1
	
	xmin = currentX

	currentX = xmax
	while not checkVerticalBlackLine(image,currentX,(h,w)) and currentX > 0:
		currentX -= 1
	
	xmax = currentX


	croppedWidth = xmax - xmin
	croppedHeight = ymax - ymin


	crop_img = image[ymin:ymin + croppedHeight , xmin:xmin + croppedWidth]
	return crop_img


def split_sudoku_cells(img):
	cells = []
	
	rows = np.array_split(img, 9)

	for r in rows:
		splitRow = np.array_split(r,9,axis = 1)
		for p in splitRow:
			cells.append(p)
	
			
	return cells

def getDigit(image):
	# image = cv2.Canny(image,100,100)
	custom_config = r'--oem 3 --psm 6 '
	

	dig = (pytesseract.image_to_string(image, config=custom_config))
	dig = [d for d in dig if d.isdigit()]
	
	if len(dig) == 0:
		return "0"


	return dig[0]

def extractDigits(cells):
	sudoku = ""
	leftCutoff = cells[0].shape[0]//5
	topCutoff = cells[0].shape[1]//5

	for c in cells:
		print("DoingCells")
		c = c[leftCutoff:-leftCutoff,topCutoff:-topCutoff]
		kernel = np.ones((2,2),np.uint8)
		c = cv2.dilate(c,kernel,iterations = 1)

		d = getDigit(c)
		sudoku += str(d)


	return sudoku

def getOneLineSudoku(filename):
	print("Entering Function")
	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	print("Converted To BW")
	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	print("Cropping Image")
	img = cropImage(img)

	print("Reading Cells")
	cells = split_sudoku_cells(img)
	oneLineSudoku = extractDigits(cells)
	
	
	return oneLineSudoku

def showCroppedImage(filename):

	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	# cv2.imshow("Disp",img)
	# cv2.waitKey(3000)
	img = cropImage(img)


	cells = split_sudoku_cells(img)
	oneLineSudoku = extractDigits(cells)
	
	# cv2.imshow("Disp 2",img)
	# cv2.waitKey(5000)
	print(oneLineSudoku)
	return oneLineSudoku


	
def main(filename):
	# return showCroppedImage(filename)

	oneLineSudoku = getOneLineSudoku(filename)
	print(oneLineSudoku)

	return oneLineSudoku


if __name__ == "__main__":
	showCroppedImage("sudoku-puzzle-1.png")
	#main()

