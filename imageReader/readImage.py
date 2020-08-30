from imageReader.image_operations import *
from imageReader.objects.Sudoku import Sudoku

def getOneLineSudoku(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print("Converting To Black and White")
    (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    print("Cropping Image")
    img = cropImage(pad_image(img))

    print("Splitting Cells")
    sudoku = Sudoku(img)
    return sudoku.get_one_line_sudoku()


def main(filename):
    return getOneLineSudoku(filename)
