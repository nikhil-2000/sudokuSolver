from imageReader.image_operations import *
from imageReader.objects.Sudoku import Sudoku


class Sudoku_Image:

    def __init__(self, filepath):

        self.image = cv2.imread(filepath)
        self.image_bw = None
        self.sudoku = None


    def get_sudoku_from_image(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        print("Converting To Black and White")
        (thresh, self.image_bw) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        print("Cropping Image")
        img_bw = cropImage(pad_image(self.image_bw))

        _,corners = get_largest_box(pad_image(self.image_bw,border=1))
        img = cropImageToCorners(self.image,corners)

        print("Splitting Cells")
        self.sudoku = Sudoku(img,img_bw)
        return self.sudoku.get_one_line_sudoku()

    def project_onto_sudoku(self,solved):
        self.sudoku.fill_empty_numbers()
        solved_cells = self.sudoku.get_cells()
        unsolved = self.sudoku.get_one_line_sudoku()
        for i,d in enumerate(unsolved):
            if d == "0":
                solved_cell_image = self.sudoku.get_cell_image(solved[i])
                solved_cells[i] = add_image_onto(solved_cells[i],solved_cell_image)

        solved_sudoku = self.put_images_together(solved_cells)
        solved_image = self.put_sudoku_on_original(solved_sudoku)
        show(ResizeWithAspectRatio(solved_sudoku,width=600))

    def put_images_together(self,solved_cells):
        for i in range(9):
            row = solved_cells[i*9]
            for j in range(1,9):
                current_cell = solved_cells[i*9 + j]
                row = np.concatenate((row,current_cell),axis=1)

            if i == 0:
                solved_image = row
            else:
                solved_image = np.concatenate((solved_image,row))

        return solved_image

    def put_sudoku_on_original(self, solved_sudoku):
        contour, corners = get_largest_box(self.image_bw)
        cv2.drawContours(self.image, [contour],0,(255,0,0),thickness=10)
        # Got sudoku and contour, need to find way to fill contour with my solved sudoku
        return solved_sudoku

