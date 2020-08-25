import unittest
import imageReader.readImage as rI

class TestStringMethods(unittest.TestCase):

    def test_imageReadRight_0(self):
        test0Actual = "000000070000050801006410035607000520000209000041000609970021400105030000080000000"
        test0Found = rI.getOneLineSudoku("testImages/test0.jpg")
        self.compareSudokus(test0Actual,test0Found)
        self.assertEqual(test0Actual, test0Found)

    def test_imageReadRight_1(self):
        test1Actual = "900000050000506100000700000070000000000090400063000000500020000000300006010000007"
        test1Found = rI.getOneLineSudoku("testImages/test1.jpg")
        self.compareSudokus(test1Actual,test1Found)
        self.assertEqual(test1Actual, test1Found)

    def test_imageReadRight_2(self):
        test2Actual = "006481300020000040700000009800090004600342001500060002300000005090000070005716200"
        test2Found = rI.getOneLineSudoku("testImages/test2.png")
        self.compareSudokus(test2Actual,test2Found)
        self.assertEqual(test2Actual, test2Found)

    def test_imageReadRight_3(self):
        test3Actual = "000400080190600450020080000000000097002000600810000000000070060073005019040009000"
        test3Found = rI.getOneLineSudoku("testImages/test3.png")
        self.compareSudokus(test3Actual,test3Found)
        self.assertEqual(test3Actual, test3Found)

    def test_imageReadRight_4(self):
        test4Actual = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"
        test4Found = rI.getOneLineSudoku("testImages/test4.jpg")
        self.compareSudokus(test4Actual,test4Found)
        self.assertEqual(test4Actual, test4Found)

    def test_imageReadRight_5(self):
        test5Actual = "079804300501002090040050001200108500790030416004900003300020050010503602005706000"
        test5Found = rI.getOneLineSudoku("testImages/test5.jpg")
        self.compareSudokus(test5Actual,test5Found)
        self.assertEqual(test5Actual, test5Found)

    def test_imageReadRight_6(self):
        test6Actual = "170023008090000240600508001000650080050001000030074000500207006010000890400180072"
        test6Found = rI.getOneLineSudoku("testImages/test6.jpg")
        self.compareSudokus(test6Actual, test6Found)
        self.assertEqual(test6Actual, test6Found)

    def test_imageReadRight_7(self):
        test7Actual = "600700200000401030008000009460030020000207000010050097300000400070102000009006008"
        test7Found = rI.getOneLineSudoku("testImages/test7.jpg")
        self.compareSudokus(test7Actual, test7Found)
        self.assertEqual(test7Actual, test7Found)

    def test_imageReadRight_8(self):
        test8Actual = "003042090090060500500000010001700285008000100329008700030000001005090020080210600"
        test8Found = rI.getOneLineSudoku("testImages/test8.png")
        self.compareSudokus(test8Actual, test8Found)
        self.assertEqual(test8Actual, test8Found)

    def test_imageReadRight_9(self):
        test9Actual = "000800176000000000000520890001030005906000301500060400054071000000000000182009000"

        test9Found = rI.getOneLineSudoku("testImages/test9.jfif")
        self.compareSudokus(test9Actual, test9Found)
        self.assertEqual(test9Actual, test9Found)

    def test_imageReadRight_10(self):
        test10Actual = "006040000098300001040009000580000079400930000310087602020000908000000020000000030"
        test10Found = rI.getOneLineSudoku("testImages/test10.jpg")
        self.compareSudokus(test10Actual, test10Found)
        self.assertEqual(test10Actual, test10Found)

    def compareSudokus(self,expected, result):
        assert (len(expected) == 81)
        assert (len(expected) == len(result))
        correct = 0
        wrong = 0
        for i, dig in enumerate(expected):
            if dig == result[i]:
                correct += 1
            else:
                wrong += 1
                r, c = rowCol(i)
                print("Wrong at row %d col %d" % (r, c))
                print("Expected %s , Read: %s" % (dig, result[i]))
                print()

def rowCol(i):
    return i//9 + 1, i%9 + 1

if __name__ == '__main__':
    unittest.main()