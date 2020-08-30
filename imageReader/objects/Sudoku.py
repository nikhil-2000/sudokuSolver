import platform
from pytesseract import pytesseract
from imageReader.image_operations import *

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
    pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

class Sudoku:
    def __init__(self, sudoku_image):
        self.image = sudoku_image
        self.cells = []
        self.split_sudoku_cells()
        self.one_line_sudoku = self.extractDigits()

    def get_one_line_sudoku(self):
        return self.one_line_sudoku

    def split_sudoku_cells(self):
        rows = np.array_split(self.image, 9)
        for r in rows:
            splitRow = np.array_split(r, 9, axis=1)
            self.cells.extend(splitRow)

    def extractDigits(self):
        cells = self.cells
        sudoku = ""
        i = 0

        for i,c in enumerate(cells):
            c = draw_white_border(c)
            d = "0"

            row_col = rowCol(i)
            if row_col in [(6, 1)]:
                print("Hit Problem cell")

            if not isWhiteImage(c):
                c = crop_to_number(c)
                d = self.getDigit(c)

            sudoku += str(d)
            i += 1

        return sudoku

    def remove_specials(self,characters):
        return characters.replace("\n", "").replace("\f", "")

    def fixCommonErrors(self,dig):
        if dig in COMMON_ERRORS.keys():
            return COMMON_ERRORS[dig]
        return dig

    def validateNumber(self,cell, found, could_be):
        k = getKernel(cell)
        eroded = cv2.erode(cell, k)
        dilated = cv2.dilate(cell, k)
        eroded_d = pytesseract.image_to_string(eroded, lang='eng', config='--psm 6 --oem 3')[0]
        dilated_d = pytesseract.image_to_string(dilated, lang='eng', config='--psm 6 --oem 3')[0]
        potential_numbers = [eroded_d, dilated_d, found]

        could_be_count = potential_numbers.count(could_be)

        return could_be if could_be_count > 1 else found

    def getDigit(self, image,iter=0):
        if iter > 0:
            image = noise_removal(image)

        dig = self.remove_specials(pytesseract.image_to_string(image, lang='eng', config='--psm 6 --oem 3'))
        dig = self.fixCommonErrors(dig)
        digitsOnly = [d for d in dig if d.isdigit()]

        if not digitsOnly:
            if iter > 3:
                return "0"
            else:
                return self.getDigit(image, iter + 1)

        if digitsOnly[0] == "1":
            digitsOnly[0] = self.validateNumber(image, "1", "7")

        if digitsOnly[0] == "2":
            digitsOnly[0] = self.validateNumber(image, "2", "7")

        if digitsOnly[0] == "4":
            digitsOnly[0] = self.validateNumber(image, "4", "1")

        return digitsOnly[0]