from imageReader.objects.Sudoku_Image import Sudoku_Image
import sys
import subprocess
import platform


def main():
    filename = sys.argv[1]
    whole_image = Sudoku_Image(filename)
    oneLineSudoku = whole_image.get_sudoku_from_image()
    if platform.system() == "Windows":
        args = ['solver/sudokuSolver.exe', oneLineSudoku]
    elif platform.system() == "Linux":
        args = ['solver/sudokuSolver', oneLineSudoku]
    else:
        args = ['solver/sudokuSolver', oneLineSudoku]

    p = subprocess.check_output(args)
    print("-------------------")
    solved_section = p.decode("utf-8").split("Solving ...")[1]
    solved_sudoku = ""
    i = 0
    while len(solved_sudoku) < 81:
        current_char = solved_section[i]
        if current_char.isdigit():
            solved_sudoku += current_char

        i += 1

    print(solved_sudoku)
    whole_image.project_onto_sudoku(solved_sudoku)

if __name__ == "__main__":
    main()
