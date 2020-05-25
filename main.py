import readImage
import sys
import subprocess



def main():
    filename = sys.argv[1]
    oneLineSoduku = readImage.main(filename)
    args = ['./sodukuSolver', oneLineSoduku]
    p = subprocess.Popen(args)
    print(p)

if __name__ == "__main__":
    main()    