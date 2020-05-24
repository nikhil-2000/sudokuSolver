import readImage
import sys
import subprocess



def main():
    filename = sys.argv[1]
    oneLineSoduku = readImage.main(filename)
    print(oneLineSoduku)

    print(subprocess.check_output(['./sodukuSolver', '030007004000195000008000060820062004000800001000020000060002280000019005000000070']))


if __name__ == "__main__":
    main()    