import cv2
import sys
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def rowCol(i):
	return i//9 + 1, i%9 + 1

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
	lineThickness = []

	currentY = ymin
	while not checkHorizontalBlackLine(image,currentY,(h,w)) and currentY < h:	currentY += 1


	topLine = 0
	while checkHorizontalBlackLine(image,currentY,(h,w)) and currentY < h:	
		topLine += 1
		currentY += 1

	lineThickness.append(topLine)
	ymin = currentY
	

	currentY = ymax
	while not checkHorizontalBlackLine(image,currentY,(h,w)) and currentY > 0:	currentY -= 1


	bottomLine = 0
	while checkHorizontalBlackLine(image,currentY,(h,w)) and currentY > 0:	
		bottomLine += 1
		currentY -= 1
		
	lineThickness.append(bottomLine)
	ymax = currentY


	currentX = xmin
	while not checkVerticalBlackLine(image,currentX,(h,w)) and currentX < w:	currentX += 1


	leftLine = 0
	while checkVerticalBlackLine(image,currentX,(h,w)) and currentX < w:	
		leftLine += 1
		currentX += 1
	
	lineThickness.append(leftLine)

	xmin = currentX

	currentX = xmax
	while not checkVerticalBlackLine(image,currentX,(h,w)) and currentX > 0:	currentX -= 1


	rightLine = 0
	while checkVerticalBlackLine(image,currentX,(h,w)) and currentX > 0:	
		rightLine += 1
		currentX -= 1
	
	lineThickness.append(rightLine)
	xmax = currentX


	croppedWidth = xmax - xmin
	croppedHeight = ymax - ymin

	crop_img = image[ymin:ymin + croppedHeight , xmin:xmin + croppedWidth]
	print(lineThickness)
	return crop_img, [max(lineThickness) for i in lineThickness]

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

def isWhiteImage(image):
	colours = {'white':0,'black':0}
	h,w = image.shape
	for i in range(h):
		for j in range(w):
			if image[i,j] != 0:
				colours['white'] += 1
			else:
				colours ['black'] += 1
	

	return colours['black'] < 100


def getNumberRect(image):
	img = image # Read in the image and convert to grayscale
	gray = 255*(img < 128).astype(np.uint8) # To invert the text to white
	coords = cv2.findNonZero(gray) # Find all non-zero points (text)
	x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
	return (x,y,w,h)

def cropBlackBorder(image):
	#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret, thresh= cv2.threshold(image,127,255,cv2.THRESH_BINARY)
	contours,hierachy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]
	x,y,w,h = cv2.boundingRect(cnt)

	crop = image[y:y+h,x:x+w]

	return crop


def extractDigits(cells,lineThickness):
	sudoku = ""
	top,bottom,left,right = lineThickness
	i = 0
	for c in cells:

		c = c[top:-bottom, left:-right]
		numberRect = getNumberRect(c)
		x,y,w,h = numberRect
		x,y,w,h = x - left, y - top, w + left + right,h + top + bottom


		if w > 0 and h > 0 and x >= 0 and y >= 0:
			c = c[y:y+h,x:x+w]

		d = getDigit(c)
	
		sudoku += str(d)
		i+= 1

	return sudoku

def getOneLineSudoku(filename):
	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


	print("Converting To Black and White")
	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	print("Cropping Image")
	img,lineThickness = cropImage(img)

	print("Splitting Cells")
	cells = split_sudoku_cells(img)

	print("Reading Cells")
	oneLineSudoku = extractDigits(cells,lineThickness)
	
	
	return oneLineSudoku

def showCroppedImage(filename):

	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


	# cv2.imshow("Disp",img)
	# cv2.waitKey(3000)
	img,lineThickness = cropImage(img)
	# cv2.imshow("After Border Clipping ", img)
	# cv2.waitKey(1000)

	cells = split_sudoku_cells(img)
	oneLineSudoku = extractDigits(cells,lineThickness)

	# cv2.imshow("Disp 2",img)
	# cv2.waitKey(3000)
	print(oneLineSudoku)
	return oneLineSudoku


	
def main(filename):
	return getOneLineSudoku(filename)

		
	return wrong == 0
