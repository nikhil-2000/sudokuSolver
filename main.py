import imageReader.readImage as readImage
import sys
import subprocess



def main():
    filename = sys.argv[1]
    oneLineSudoku = readImage.main(filename)
    #Need a fix for different os, maybe compile 3 different versions ?
    args = ['/solver/sudokuSolver.exe', oneLineSudoku]
    p = subprocess.Popen(args)
    print(p)

if __name__ == "__main__":
    main()    