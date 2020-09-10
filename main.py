from imageReader.objects.Sudoku_Image import Sudoku_Image
import sys
import subprocess
import platform


def main(filename):
    whole_image = Sudoku_Image(filename)
    oneLineSudoku = whole_image.get_sudoku_from_image()
    if platform.system() == "Windows":
        args = ['solver/sudokuSolver.exe', oneLineSudoku]
    elif platform.system() == "Linux":
        args = ['solver/sudokuSolver', oneLineSudoku]
    else:
        args = ['solver/sudokuSolver', oneLineSudoku]

    p = subprocess.check_output(args)
    solved_section = p.decode("utf-8").split("Solving ...")[1]

    if "Unsolvable Grid" in solved_section:
        print("Cannot solve sudoku")
        return

    solved_sudoku = ""
    i = 0
    while len(solved_sudoku) < 81:
        current_char = solved_section[i]
        if current_char.isdigit():
            solved_sudoku += current_char

        i += 1

    whole_image.project_onto_sudoku(solved_sudoku)
    print("-------------------")

if __name__ == "__main__":
    file = sys.argv[1]
    main(file)
