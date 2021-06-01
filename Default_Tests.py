import unittest
import sys
import VESinverse_JClark as VI         #This will change when splitting file into GUI and Computation

''' The tests are numbered by the page
    in the excel Doc
    i.e. sheet 2 of 17 has the 3L-R2-D1 data so the test for that data is numbered 2
'''

class VEStesting(unittest.TestCase):
#Layer 3 Tests
    def test_3L_R1_D1(self):            #Test_number == 4
        '''follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        VI.LAYERS = 3   
        VI.DATASET = 1
        VI.RANGE = 1
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 1.240)
        self.assertEqual(round(VI.pkeep[3], 3), 145.898)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 20.934)
        self.assertEqual(round(VI.pkeep[4], 3), 5.977)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 850.819)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.07708)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 110)
        self.assertEqual(VI.rdat[3], 95)
        self.assertEqual(VI.rdat[4], 40)
        self.assertEqual(VI.rdat[5], 24)
        self.assertEqual(VI.rdat[6], 15)
        self.assertEqual(VI.rdat[7], 10.5)
        self.assertEqual(VI.rdat[8], 8)
        self.assertEqual(VI.rdat[9], 6)
        self.assertEqual(VI.rdat[10], 6.5)
        self.assertEqual(VI.rdat[11], 11)
        self.assertEqual(VI.rdat[12], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 139.607)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 120.653)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 86.525)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 39.519)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 26.552)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 10.712)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 7.996)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 6.571)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 6.872)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 8.659)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 11.916)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 26.783)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D3(self):            #Test_number == 1
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 3
        VI.RANGE = 2
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 3.425)
        self.assertEqual(round(VI.pkeep[3], 3), 123.969)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 31.392)
        self.assertEqual(round(VI.pkeep[4], 3), 7.610)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 358.811)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.063684)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 124)
        self.assertEqual(VI.rdat[3], 120)
        self.assertEqual(VI.rdat[4], 115)
        self.assertEqual(VI.rdat[5], 110)
        self.assertEqual(VI.rdat[6], 95)
        self.assertEqual(VI.rdat[7], 40)
        self.assertEqual(VI.rdat[8], 24)
        self.assertEqual(VI.rdat[9], 15)
        self.assertEqual(VI.rdat[10], 10)
        self.assertEqual(VI.rdat[11], 11)
        self.assertEqual(VI.rdat[12], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 129.148)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 129.604)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 132.062)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 140.443)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 145.663)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 160.541)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 167.419)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 169.344)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 155.021)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 110.427)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 79.748)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 59.383)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D1(self):            #Test_number == 2
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 1
        VI.RANGE = 2
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 1.033)
        self.assertEqual(round(VI.pkeep[3], 3), 103.591)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 38.001)
        self.assertEqual(round(VI.pkeep[4], 3), 11.226)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 93.574)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.1636)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 110)
        self.assertEqual(VI.rdat[3], 95)
        self.assertEqual(VI.rdat[4], 40)
        self.assertEqual(VI.rdat[5], 24)
        self.assertEqual(VI.rdat[6], 15)
        self.assertEqual(VI.rdat[7], 10.5)
        self.assertEqual(VI.rdat[8], 8)
        self.assertEqual(VI.rdat[9], 6)
        self.assertEqual(VI.rdat[10], 6.5)
        self.assertEqual(VI.rdat[11], 11)
        self.assertEqual(VI.rdat[12], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 97.140)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 80.420)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 54.951)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 26.804)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 20.459)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 13.477)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 12.344)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 11.606)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 11.594)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 12.157)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 13.645)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 22.966)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D2(self):            #Test_number == 3
        '''follows from the 3L-R2-D2 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 2
        VI.RANGE = 2
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 3.424)
        self.assertEqual(round(VI.pkeep[3], 3), 123.969)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 31.392)
        self.assertEqual(round(VI.pkeep[4], 3), 7.6097)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 358.811)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.07708)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 130)
        self.assertEqual(VI.rdat[3], 140)
        self.assertEqual(VI.rdat[4], 150)
        self.assertEqual(VI.rdat[5], 160)
        self.assertEqual(VI.rdat[6], 170)
        self.assertEqual(VI.rdat[7], 175)
        self.assertEqual(VI.rdat[8], 170)
        self.assertEqual(VI.rdat[9], 130)
        self.assertEqual(VI.rdat[10], 100)
        self.assertEqual(VI.rdat[11], 80)
        self.assertEqual(VI.rdat[12], 60)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 123.981)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 122.485)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 118.7)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 105.397)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 96.59)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 68.925)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 53.113)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 21.708)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 12.982)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 9.449)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 10.985)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 22.06)
        print("\"Predicted\" tests Completed")

    def test_3L_R1_D2(self):            #Test_number == 5
     '''follows from the 3L-R2-D2 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 2
        VI.RANGE = 1
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 4.969)
        self.assertEqual(round(VI.pkeep[3], 3), 157.388)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 71.670)
        self.assertEqual(round(VI.pkeep[4], 3), 83.794)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 2230.04)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 4), 0.1159)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 130)
        self.assertEqual(VI.rdat[3], 140)
        self.assertEqual(VI.rdat[4], 150)
        self.assertEqual(VI.rdat[5], 160)
        self.assertEqual(VI.rdat[6], 170)
        self.assertEqual(VI.rdat[7], 175)
        self.assertEqual(VI.rdat[8], 170)
        self.assertEqual(VI.rdat[9], 130)
        self.assertEqual(VI.rdat[10], 100)
        self.assertEqual(VI.rdat[11], 80)
        self.assertEqual(VI.rdat[12], 60)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 157.671)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 157.075)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 156.427)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 153.796)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 151.724)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 143.373)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 136.93)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 116.639)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 105.238)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 92.771)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 90.918)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 117.472)
        print("\"Predicted\" tests Completed")   

    def test_3L_R1_D3(self):            #Test_number == 6
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 3
        VI.RANGE = 1
        VI.GRAPH = False
        VI.computePredictions()

        self.assertEqual(round(VI.pkeep[1], 3), 3.110)
        self.assertEqual(round(VI.pkeep[3], 3), 144.197)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.pkeep[2], 3), 44.508)
        self.assertEqual(round(VI.pkeep[4], 3), 9.867)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.pkeep[5], 3), 1075.63)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.06624)
        print("RMS test Completed")

        self.assertEqual(VI.adat[1], 0.55)
        self.assertEqual(VI.adat[2], 0.95)
        self.assertEqual(VI.adat[3], 1.5)
        self.assertEqual(VI.adat[4], 2.5)
        self.assertEqual(VI.adat[5], 3)
        self.assertEqual(VI.adat[6], 4.5)
        self.assertEqual(VI.adat[7], 5.5)
        self.assertEqual(VI.adat[8], 9)
        self.assertEqual(VI.adat[9], 12)
        self.assertEqual(VI.adat[10], 20)
        self.assertEqual(VI.adat[11], 30)
        self.assertEqual(VI.adat[12], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.rdat[1], 125)
        self.assertEqual(VI.rdat[2], 124)
        self.assertEqual(VI.rdat[3], 120)
        self.assertEqual(VI.rdat[4], 115)
        self.assertEqual(VI.rdat[5], 110)
        self.assertEqual(VI.rdat[6], 95)
        self.assertEqual(VI.rdat[7], 40)
        self.assertEqual(VI.rdat[8], 24)
        self.assertEqual(VI.rdat[9], 15)
        self.assertEqual(VI.rdat[10], 10)
        self.assertEqual(VI.rdat[11], 11)
        self.assertEqual(VI.rdat[12], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[1], 3), 144.077)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 141.915)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 136.358)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 117.834)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 106.207)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 72.117)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 54.128)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 21.928)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 14.173)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 11.086)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 11.968)
        self.assertEqual(round(VI.pltanswerkeep[12], 3), 21.272)
        print("\"Predicted\" tests Completed")

#Layer 2 Tests

if __name__ == '__main__':
    test_number = int(sys.argv[1])
    test = VEStesting()
    if test_number == 1:
        test.test_3L_R2_D3()        #written
    elif test_number == 2:
        test.test_3L_R2_D1()        #Written
    elif test_number == 3:
        test.test_3L_R2_D2()        #Written
    elif test_number == 4:
        test.test_3L_R1_D1()        #Written
    elif test_number == 5:
        test.test_3L_R1_D2()        #written
    elif test_number == 6:
        test.test_3L_R1_D3()        #Written