import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def rowCol(i):
    return i // 9 + 1, i % 9 + 1


def checkHorizontalBlackLine(image, currentY, dimensions):
    h, w = dimensions

    xPoints = np.arange(0, w)
    colours = {'black': 0, 'white': 0}
    for x in xPoints:
        pixel = image[currentY, x]

        if pixel == 0:
            colours['black'] += 1
        else:
            colours['white'] += 1

    return colours['black'] > colours['white']


def checkVerticalBlackLine(image, currentX, dimensions):
    h, w = dimensions

    yPoints = np.arange(0, h)
    colours = {'black': 0, 'white': 0}
    for y in yPoints:
        pixel = image[y, currentX]

        if pixel == 0:
            colours['black'] += 1
        else:
            colours['white'] += 1

    return colours['black'] > colours['white']


def cropImage(image):
    h, w = image.shape[0] - 1, image.shape[1] - 1

    xmin, xmax, ymin, ymax = 0, w, 0, h

    currentY = ymin
    while not checkHorizontalBlackLine(image, currentY, (h, w)) and currentY < h:    currentY += 1

    while checkHorizontalBlackLine(image, currentY, (h, w)) and currentY < h:        currentY += 1
    ymin = currentY

    currentY = ymax
    while not checkHorizontalBlackLine(image, currentY, (h, w)) and currentY > 0:    currentY -= 1

    while checkHorizontalBlackLine(image, currentY, (h, w)) and currentY > 0:        currentY -= 1
    ymax = currentY

    currentX = xmin
    while not checkVerticalBlackLine(image, currentX, (h, w)) and currentX < w:    currentX += 1

    while checkVerticalBlackLine(image, currentX, (h, w)) and currentX < w:        currentX += 1
    xmin = currentX

    currentX = xmax
    while not checkVerticalBlackLine(image, currentX, (h, w)) and currentX > 0:    currentX -= 1

    while checkVerticalBlackLine(image, currentX, (h, w)) and currentX > 0:        currentX -= 1

    xmax = currentX

    croppedWidth = xmax - xmin
    croppedHeight = ymax - ymin

    crop_img = image[ymin:ymin + croppedHeight, xmin:xmin + croppedWidth]
    return crop_img


def split_sudoku_cells(img):
    cells = []

    rows = np.array_split(img, 9)

    for r in rows:
        splitRow = np.array_split(r, 9, axis=1)
        for p in splitRow:
            cells.append(p)

    return cells


def getDigit(image):
    custom_config = r'--oem 3 --psm 6 '

    dig = (pytesseract.image_to_string(image, config=custom_config))
    dig = [d for d in dig if d.isdigit()]
    if len(dig) == 0:
        return "0"

    return dig[0]


def isWhiteImage(image):
    colours = {'white': 0, 'black': 0}
    h, w = image.shape
    for i in range(h):
        for j in range(w):
            if image[i, j] != 0:
                colours['white'] += 1
            else:
                colours['black'] += 1

    return colours['black'] < sum(colours.values()) / 100


def draw_white_border(image):
    white = (255, 255, 255)
    h, w = image.shape[0] - 1, image.shape[1] - 1
    verticalEdge, horizontalEdge = h // 4, w // 4
    thickness = max([verticalEdge, horizontalEdge])

    return cv2.rectangle(image, (0, 0), (w, h), white, thickness)


def getNumberRect(img):
    gray = 255 * (img < 128).astype(np.uint8)  # To invert the text to white
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    return (x, y, w, h)


def extractDigits(cells):
    sudoku = ""
    i = 0
    for c in cells:
        c = draw_white_border(c)
        d = 0

        if not isWhiteImage(c):
            numberRect = getNumberRect(c)
            x, y, w, h = numberRect
            c = c[y:y + h, x:x + w]
            c = cv2.copyMakeBorder(c, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))

            d = getDigit(c)

        sudoku += str(d)
        i += 1

    return sudoku


def getOneLineSudoku(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("Converting To Black and White")
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    print("Cropping Image")
    img = cropImage(img)

    print("Splitting Cells")
    cells = split_sudoku_cells(img)

    print("Reading Cells")
    oneLineSudoku = extractDigits(cells)

    return oneLineSudoku


def main(filename):
    return getOneLineSudoku(filename)
