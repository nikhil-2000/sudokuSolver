import cv2
import sys
import pytesseract
import numpy as np

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
	return crop_img, lineThickness

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

def cropToNumber(image):
	img = image # Read in the image and convert to grayscale
	gray = 255*(img < 128).astype(np.uint8) # To invert the text to white
	coords = cv2.findNonZero(gray) # Find all non-zero points (text)
	x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
	emptyImage = all([i == 0 for i in [w,h]])
	extra = 4
	if not emptyImage:
		#x,y,w,h = x-extra,y-extra,w + 2*extra, h + 2*extra #Dont crop to close to edges of number

		# print("Found Digit")
		rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image

		# cv2.imshow("Cropped", rect) # Show it
		# cv2.waitKey(3000)
		return rect
	
	return None

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

	for c in cells:
		# cv2.imshow("Cropped",c)
		# cv2.waitKey(1000)
		c = c[top:-bottom, left:-right]
		
		# cv2.imshow("Cropped",c)
		# cv2.waitKey(1000)
		d = getDigit(c)
	
		
		# kernel = np.ones((2,2),np.uint8)
		#c = cv2.dilate(c,kernel,iterations = 1)
		
		sudoku += str(d)

	return sudoku

def getOneLineSudoku(filename):
	print("Entering Function")
	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


	print("Converted To BW")
	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	print("Cropping Image")
	img,lineThickness = cropImage(img)

	print("Reading Cells")
	cells = split_sudoku_cells(img)
	oneLineSudoku = extractDigits(cells,lineThickness)
	
	
	return oneLineSudoku

def showCroppedImage(filename):

	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	(thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


	# cv2.imshow("Disp",img)
	# cv2.waitKey(3000)
	img,lineThickness = cropImage(img)
	cv2.imshow("After Border Clipping ", img)
	cv2.waitKey(1000)

	cells = split_sudoku_cells(img)
	oneLineSudoku = extractDigits(cells,lineThickness)
	
	# cv2.imshow("Disp 2",img)
	# cv2.waitKey(3000)
	print(oneLineSudoku)
	return oneLineSudoku


	
def main(filename):
	# return showCroppedImage(filename)

	oneLineSudoku = getOneLineSudoku(filename)
	print(oneLineSudoku)

	return oneLineSudoku

def compareSudokus(expected,result):
	assert(len(expected) == 81)
	assert(len(expected) == len(result))
	correct = 0
	wrong = 0
	for i,dig in enumerate(expected):
		if dig == result[i]:
			correct += 1
		else:
			wrong += 1
			r,c = rowCol(i)
			print("Wrong at row %d col %d" % (r,c))
			print("Expected %s , Read: %s" % (dig,result[i]))
			print()
		
	return wrong == 0


if __name__ == "__main__":
	test0Actual = "000000070000050801006410035607000520000209000041000609970021400105030000080000000"
	test1Actual = "900000050000506100000700000070000000000090400063000000500020000000300006010000007"
	test2Actual = "006481300020000040700000009800090004600342001500060002300000005090000070005716200"
	test3Actual = "000400080190600450020080000000000097002000600810000000000070060073005019040009000"

	# borderImage = cv2.imread("test0.jpg")
	# borderImage = cv2.cvtColor(borderImage,cv2.COLOR_BGR2GRAY)
	# cropped = cropImage(borderImage)
	# cv2.imshow("cropped",cropped)
	# cv2.waitKey(2000)
	test0Result = showCroppedImage("test0.jpg")
	print(compareSudokus(test0Actual,test0Result))


	test1Result = showCroppedImage("test1.jpg")
	print(compareSudokus(test1Actual,test1Result))
	
	test2Result = showCroppedImage("test2.png")
	print(compareSudokus(test2Actual,test2Result))

	test3Result = showCroppedImage("test3.png")
	print(compareSudokus(test3Actual,test3Result))


	#main()

