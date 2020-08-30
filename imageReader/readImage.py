import cv2
import numpy as np
import pytesseract
import platform
from imageReader.croppingToBox import testing

COMMON_ERRORS = {
    'g' : '9',
    'fe)': '9',
    'e' : '9',
    'Q' : '9',
    'T' : '7',
    '|' : '1',
    'vA': '7',
    'o' : '5',
    'a' : '2'
}


if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def rowCol(i):
    return i // 9 + 1, i % 9 + 1

def order_corner_points(corners):
    # Separate corners into individual points
    # Index 0 - top-right
    #       1 - top-left
    #       2 - bottom-left
    #       3 - bottom-right
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    corners  = sorted(corners, key = lambda x : x[1])
    top_corners, bottom_corners = sorted(corners[0:2],key = lambda x:x[0]), sorted(corners[2:],key = lambda x:x[0])
    top_l,top_r = top_corners
    bottom_l,bottom_r = bottom_corners
    return (top_l, top_r, bottom_r, bottom_l)

def perspective_transform(image, corners):

    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    # Determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                    [0, height - 1]], dtype = "float32")

    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))

def cropImage(image):
    original = np.copy(image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    ROI_number = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        if len(approx) == 4:
            cv2.drawContours(image, [c], 0, (36, 255, 12), 3)
            transformed = perspective_transform(original, approx)
            # rotated = rotate_image(transformed,0)
            return transformed

def split_sudoku_cells(img):
    cells = []

    rows = np.array_split(img, 9)

    for r in rows:
        splitRow = np.array_split(r, 9, axis=1)
        for p in splitRow:
            cells.append(p)

    return cells


def fixCommonErrors(dig):

    if dig in COMMON_ERRORS.keys():
        return COMMON_ERRORS[dig]

    return dig

def getKernel(image):
    dim = max(image.shape) // 20
    if dim < 3:
        dim = 3

    return np.ones((dim, dim), np.uint8)


def remove_specials(characters):
    return characters.replace("\n", "").replace("\f", "")

def validateNumber(image, found, could_be):
    k = getKernel(image)
    eroded = cv2.erode(image,k)
    dilated = cv2.dilate(image,k)
    eroded_d = pytesseract.image_to_string(eroded, lang='eng', config='--psm 6 --oem 3')[0]
    dilated_d = pytesseract.image_to_string(dilated, lang='eng', config='--psm 6 --oem 3')[0]
    potential_numbers = [eroded_d,dilated_d,found]

    could_be_count   = potential_numbers.count(could_be)

    return could_be if could_be_count > 1 else found

def getDigit(image, iter = 0):
    if iter > 0:
        image = noise_removal(image)

    dig = remove_specials(pytesseract.image_to_string(image, lang='eng', config='--psm 6 --oem 3'))
    dig = fixCommonErrors(dig)
    digitsOnly = [d for d in dig if d.isdigit()]

    if not digitsOnly:
        if iter > 3 : return "0"
        else : return getDigit(image,iter+1)

    if digitsOnly[0] == "1":
        digitsOnly[0] = validateNumber(image,"1","7")

    if digitsOnly[0] == "2":
        digitsOnly[0] = validateNumber(image,"2","7")

    if digitsOnly[0] == "4":
        digitsOnly[0] = validateNumber(image,"4","1")

    return digitsOnly[0]


def isWhiteImage(image):
    return np.all(image == 255)


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

def noise_removal(image):
    kernel = getKernel(image)
    return cv2.erode(
        cv2.dilate(image, kernel)
        , kernel
    )

def extractDigits(cells):
    sudoku = ""
    i = 0

    border = 10

    for c in cells:
        c = draw_white_border(c)
        d = 0

        row_col = rowCol(i)
        if row_col in [(6, 1)]:
            print("Hit Problem cell")

        if not isWhiteImage(c):
            numberRect = getNumberRect(c)
            x, y, w, h = numberRect
            c = c[y:y + h, x:x + w]
            c = pad_image(c, border)
            d = getDigit(c)

        sudoku += str(d)
        i += 1

    return sudoku


def resizeImage(img, height):
    width = round(img.shape[1] * (height/img.shape[0]))
    return cv2.resize(img,(height,width))


def pad_image(img, border = 10):
    img =  cv2.copyMakeBorder(img, border, border, border, border, cv2.BORDER_CONSTANT, None, 255)
    return img


def getOneLineSudoku(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("Converting To Black and White")
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    print("Cropping Image")
    img = cropImage(pad_image(img))

    print("Splitting Cells")
    cells = split_sudoku_cells(img)

    print("Reading Cells")
    oneLineSudoku = extractDigits(cells)

    return oneLineSudoku


def main(filename):
    return getOneLineSudoku(filename)
