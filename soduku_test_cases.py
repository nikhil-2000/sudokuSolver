import unittest
import readImage as rI

class TestStringMEthods(unittest.TestCase):

	# test6Actual = "170023008090000240600508001000650080050001000030074000500207006010000890400180072"
	# test7Actual = "600700200000401030008000009460030020000207000010050097300000400070102000009006008"

    def test_imageReadRight_0(self):
        test0Actual = "000000070000050801006410035607000520000209000041000609970021400105030000080000000"
        self.assertEqual(test0Actual, rI.showCroppedImage("testImages/test0.jpg"))

    def test_imageReadRight_1(self):
        test1Actual = "900000050000506100000700000070000000000090400063000000500020000000300006010000007"
        self.assertEqual(test1Actual, rI.showCroppedImage("testImages/test1.jpg"))

    def test_imageReadRight_2(self):
    	test2Actual = "006481300020000040700000009800090004600342001500060002300000005090000070005716200"
        self.assertEqual(test2Actual, rI.showCroppedImage("testImages/test2.jpg"))

    def test_imageReadRight_3(self):
    	test3Actual = "000400080190600450020080000000000097002000600810000000000070060073005019040009000"
        self.assertEqual(test3Actual, rI.showCroppedImage("testImages/test3.jpg"))

    def test_imageReadRight_4(self):
    	test4Actual = "000000000000003085001020000000507000004000100090000000500000073002010000000040009"
        self.assertEqual(test4Actual, rI.showCroppedImage("testImages/test4.jpg"))

    def test_imageReadRight_5(self):
    	test5Actual = "079804300501002090040050001200108500790030416004900003300020050010503602005706000"
        self.assertEqual(test5Actual, rI.showCroppedImage("testImages/test5.jpg"))

