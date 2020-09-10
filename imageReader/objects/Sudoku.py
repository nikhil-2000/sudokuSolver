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
    def __init__(self, sudoku_image,sudoku_image_bw):
        self.image = sudoku_image
        self.image_bw = sudoku_image_bw
        self.number_to_image_dict = populate_dictionary()
        self.cells = split_sudoku_cells(self.image)
        self.cells_bw = split_sudoku_cells(self.image_bw)

        self.one_line_sudoku = self.extractDigits()

    def get_one_line_sudoku(self):
        return self.one_line_sudoku

    def get_cells(self):
        return self.cells

    def get_cell_image(self,digit):
        return self.number_to_image_dict[digit]

    def extractDigits(self):
        sudoku = ""
        i = 0

        for i,c in enumerate(self.cells_bw):
            current_cell = draw_white_border(np.copy(c))
            d = "0"

            if not isWhiteImage(current_cell):
                current_cell = crop_to_number(current_cell)
                d = self.getDigit(current_cell)

                self.update_number_image_dict(d,i)

            sudoku += str(d)
            i += 1

        return sudoku

    def getDigit(self, image,iter=0):
        if iter > 0:
            image = noise_removal(image)

        dig = remove_specials(pytesseract.image_to_string(image, lang='eng', config='--psm 6 --oem 3'))
        dig = fixCommonErrors(dig)
        digitsOnly = [d for d in dig if d.isdigit()]

        if not digitsOnly:
            if iter > 3:
                return "0"
            else:
                return self.getDigit(image, iter + 1)

        if digitsOnly[0] == "1":
            digitsOnly[0] = validateNumber(image, "1", "7")

        if digitsOnly[0] == "2":
            digitsOnly[0] = validateNumber(image, "2", "7")

        if digitsOnly[0] == "4":
            digitsOnly[0] = validateNumber(image, "4", "1")


        return digitsOnly[0]

    def update_number_image_dict(self, digit, cell_index):
        bw_cell = draw_white_border(self.cells_bw[cell_index])
        x, y, w, h = getNumberRect(bw_cell)
        #Need a better way to pick this value, seems to work for all test cases though
        p = 2
        x , y , w , h = x - p, y - p, w + 2*p, h + 2*p
        cropped_number = self.cells[cell_index][y:y + h, x:x + w]
        if digit == "0": return
        if self.number_to_image_dict[digit] == []:
            self.number_to_image_dict[digit] = cropped_number

    def fill_empty_numbers(self):
        non_empty_image = next(img for img in self.number_to_image_dict.values() if img != [])
        empty_key_value = [(k,v) for k,v in self.number_to_image_dict.items() if v == []]
        for (k,v) in empty_key_value:
            self.number_to_image_dict[k] = ResizeWithAspectRatio(getDefaultDigit(k),height=non_empty_image.shape[0])



def populate_dictionary():
    d = {}
    for i in range(1, 10):
        d[str(i)] = []  ##Will add default images

    return d

def remove_specials(characters):
    return characters.replace("\n", "").replace("\f", "")

def fixCommonErrors(dig):
    if dig in COMMON_ERRORS.keys():
        return COMMON_ERRORS[dig]
    return dig

def validateNumber(cell, found, could_be):
    k = getKernel(cell)
    eroded = cv2.erode(cell, k)
    dilated = cv2.dilate(cell, k)
    eroded_d = pytesseract.image_to_string(eroded, lang='eng', config='--psm 6 --oem 3')[0]
    dilated_d = pytesseract.image_to_string(dilated, lang='eng', config='--psm 6 --oem 3')[0]
    potential_numbers = [eroded_d, dilated_d, found]

    could_be_count = potential_numbers.count(could_be)

    return could_be if could_be_count > 1 else found

def split_sudoku_cells(image):
    image = np.copy(image)
    rows = np.array_split(image, 9)
    cells = []

    for r in rows:
        splitRow = np.array_split(r, 9, axis=1)
        cells.extend(splitRow)

    return cells


def getDefaultDigit(k):
    return cv2.imread("Images/digitImages/" + k + ".PNG")