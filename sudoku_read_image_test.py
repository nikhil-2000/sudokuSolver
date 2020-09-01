from imageReader.objects.Sudoku_Image import Sudoku_Image
import pytest

def test_imageReadRight_0():
    test0Actual = "000000070000050801006410035607000520000209000041000609970021400105030000080000000"
    path = "testImages/test0.jpg"
    load_sudokus_and_compare(test0Actual,path)

def test_imageReadRight_1():
    test1Actual = "900000050000506100000700000070000000000090400063000000500020000000300006010000007"
    path = "testImages/test1.jpg"
    load_sudokus_and_compare(test1Actual,path)


def test_imageReadRight_2():
    test2Actual = "006481300020000040700000009800090004600342001500060002300000005090000070005716200"
    path = "testImages/test2.png"
    load_sudokus_and_compare(test2Actual,path)

def test_imageReadRight_3():
    test3Actual = "000400080190600450020080000000000097002000600810000000000070060073005019040009000"
    path = "testImages/test3.png"
    load_sudokus_and_compare(test3Actual,path)


def test_imageReadRight_4():
    test4Actual = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"
    path = "testImages/test4.jpg"
    load_sudokus_and_compare(test4Actual,path)


def test_imageReadRight_5():
    test5Actual = "079804300501002090040050001200108500790030416004900003300020050010503602005706000"
    path = "testImages/test5.jpg"
    load_sudokus_and_compare(test5Actual,path)


def test_imageReadRight_6():
    test6Actual = "170023008090000240600508001000650080050001000030074000500207006010000890400180072"
    path = "testImages/test6.jpg"
    load_sudokus_and_compare(test6Actual,path)

def test_imageReadRight_7():
    test7Actual = "600700200000401030008000009460030020000207000010050097300000400070102000009006008"
    path = "testImages/test7.jpg"
    load_sudokus_and_compare(test7Actual, path)

def test_imageReadRight_8():
    test8Actual = "009070083204600050780000102040052090007106200050890041901000070060709304000580900"
    path = "testImages/test8.jpg"
    load_sudokus_and_compare(test8Actual, path)


def test_imageReadRight_9():
    test9Actual = "000800176000000000000520890001030005906000301500060400054071000000000000182009000"
    path = "testImages/test9.jfif"
    load_sudokus_and_compare(test9Actual, path)

def test_imageReadRight_10():
    test10Actual = "090080070007104500600700009400902001013000290700801004800000103001208900070010080"
    path = "testImages/test10.jpg"
    load_sudokus_and_compare(test10Actual, path)


def test_imageReadRight_11():
    test11Actual = "000830070057000008030540000603000000205000403000000601000059040500000720020068000"
    path = "testImages/test11.jpg"
    load_sudokus_and_compare(test11Actual, path)

def load_sudokus_and_compare(actual,path):
    found = Sudoku_Image(path).get_sudoku_from_image()
    compareSudokus(actual,found)

def compareSudokus(expected, result):
    assert (len(expected) == 81)
    assert (len(expected) == len(result))
    row_col_list = []
    correct = 0
    wrong = 0
    for i, dig in enumerate(expected):
        if dig == result[i]:
            correct += 1
        else:
            wrong += 1
            r, c = rowCol(i)
            row_col_list.append((r,c))
            print("Wrong at row %d col %d" % (r, c))
            print("Expected %s , Read: %s" % (dig, result[i]))

    assert expected == result

def rowCol(i):
    return i//9 + 1, i%9 + 1