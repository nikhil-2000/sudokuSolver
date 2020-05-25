import readImage
import sys
import subprocess



def main():
    filename = sys.argv[1]
    oneLineSudoku = readImage.main(filename)
    args = ['./sudokuSolver', oneLineSudoku]
    p = subprocess.Popen(args)
    print(p)

if __name__ == "__main__":
    main()    