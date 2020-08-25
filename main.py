import imageReader.readImage as readImage
import sys
import subprocess
import platform


def main():
    filename = sys.argv[1]
    oneLineSudoku = readImage.main(filename)
    # Need a fix for different os, maybe compile 3 different versions ?
    if platform.system() == "Windows":
        args = ['solver/sudokuSolver.exe', oneLineSudoku]
    elif platform.system() == "Linux":
        args = ['solver/sudokuSolver', oneLineSudoku]
    else:
        args = ['solver/sudokuSolver', oneLineSudoku]

    p = subprocess.Popen(args)
    print(p)


if __name__ == "__main__":
    main()
