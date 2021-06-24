import unittest
import sys
from VESinverse_ajv234 import VESinverse
import numpy as np
from VESgui import VESgui
import os
from tkinter import Tk, IntVar

''' The tests are numbered by the page
    in the excel Doc
    i.e. sheet 2 of 17 has the 3L-R2-D1 data so the test
        for that data is numbered 2
'''


class VEStesting(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.t_index = 2
        self.t_field_data = [0]*65
        self.t_location_data = [0]*65
        self.t_small = [0]*65
        self.t_xlarge = [0]*65
        self.small_array = [0]*65

        self.t_thick_min = []
        self.t_thick_max = []
        self.t_res_min = []
        self.t_res_max = []

    def run_tests(self, test_number):
        # Layer 3 tests
        if test_number == 1:
            self.test_3L_R2_D3()
        elif test_number == 2:
            self.test_3L_R2_D1()
        elif test_number == 3:
            self.test_3L_R2_D2()
        elif test_number == 4:
            self.test_3L_R1_D1()
        elif test_number == 5:
            self.test_3L_R1_D2()
        elif test_number == 6:
            self.test_3L_R1_D3()
        # Layer 2 tests
        elif test_number == 7:
            self.test_2L_R3_D4()
        elif test_number == 8:
            self.test_2L_R3_D5()
        elif test_number == 9:
            self.test_2L_R4_D5()
        elif test_number == 10:
            self.test_2L_R3_D6()
        elif test_number == 11:
            self.test_2L_R4_D6()
        # Layer 4 tests
        elif test_number == 12:
            self.test_4L_R5_D7()
        elif test_number == 13:
            self.test_4L_R6_D7()
        elif test_number == 14:
            self.test_4L_R7_D7()
        elif test_number == 15:
            self.test_4L_R7_D8()
        elif test_number == 16:
            self.test_4L_R6_D8()
        elif test_number == 17:
            self.test_4L_R5_D8()
        
        # elif test_number == 18:
        #     self.gui_test_1()
        # elif test_number == 19:
        #     self.gui_test_2()
# Layer 3 Tests

    def test_3L_R1_D1(self):            # test_number == 4
        '''follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 1
        self.RANGE = 1
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()
        self.test_3L_R1_D1_asserts()

    def test_3L_R1_D1_asserts(self):
        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.240)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 145.898)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 20.934)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 5.977)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 850.819)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.07708)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 110)
        self.assertEqual(VI.field_data[2], 95)
        self.assertEqual(VI.field_data[3], 40)
        self.assertEqual(VI.field_data[4], 24)
        self.assertEqual(VI.field_data[5], 15)
        self.assertEqual(VI.field_data[6], 10.5)
        self.assertEqual(VI.field_data[7], 8)
        self.assertEqual(VI.field_data[8], 6)
        self.assertEqual(VI.field_data[9], 6.5)
        self.assertEqual(VI.field_data[10], 11)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 139.607)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 120.653)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 86.525)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 39.519)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 26.552)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 10.712)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 7.996)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 6.571)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 6.872)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 8.659)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 11.916)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 26.783)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D3(self):            # test_number == 1
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 3
        self.RANGE = 2
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 3.425)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 123.969)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 31.392)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 7.610)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 358.811)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.06368)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 120)
        self.assertEqual(VI.field_data[3], 115)
        self.assertEqual(VI.field_data[4], 110)
        self.assertEqual(VI.field_data[5], 95)
        self.assertEqual(VI.field_data[6], 40)
        self.assertEqual(VI.field_data[7], 24)
        self.assertEqual(VI.field_data[8], 15)
        self.assertEqual(VI.field_data[9], 10)
        self.assertEqual(VI.field_data[10], 11)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 123.981)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 122.485)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 118.7)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 105.397)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 96.59)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 68.925)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 53.113)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 21.708)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 12.982)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 9.449)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 10.985)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 22.06)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D1(self):            # test_number == 2
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 1
        self.RANGE = 2
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.033)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 103.591)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 38.001)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 11.226)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 93.574)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.1636)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 110)
        self.assertEqual(VI.field_data[2], 95)
        self.assertEqual(VI.field_data[3], 40)
        self.assertEqual(VI.field_data[4], 24)
        self.assertEqual(VI.field_data[5], 15)
        self.assertEqual(VI.field_data[6], 10.5)
        self.assertEqual(VI.field_data[7], 8)
        self.assertEqual(VI.field_data[8], 6)
        self.assertEqual(VI.field_data[9], 6.5)
        self.assertEqual(VI.field_data[10], 11)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 97.140)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 80.420)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 54.951)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 26.804)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 20.459)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 13.477)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 12.344)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 11.606)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 11.594)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 12.157)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 13.645)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 22.966)
        print("\"Predicted\" tests Completed")

    def test_3L_R2_D2(self):            # test_number == 3
        '''follows from the 3L-R2-D2 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 2
        self.RANGE = 2
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 3.194)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 128.599)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 4.109)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 350.702)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 57.086)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.03167)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 130)
        self.assertEqual(VI.field_data[2], 140)
        self.assertEqual(VI.field_data[3], 150)
        self.assertEqual(VI.field_data[4], 160)
        self.assertEqual(VI.field_data[5], 170)
        self.assertEqual(VI.field_data[6], 175)
        self.assertEqual(VI.field_data[7], 170)
        self.assertEqual(VI.field_data[8], 130)
        self.assertEqual(VI.field_data[9], 100)
        self.assertEqual(VI.field_data[10], 80)
        self.assertEqual(VI.field_data[11], 60)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 129.148)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 129.604)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 132.062)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 140.443)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 145.663)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 160.541)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 167.419)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 169.344)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 155.021)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 110.427)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 79.748)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 59.383)
        print("\"Predicted\" tests Completed")

    def test_3L_R1_D2(self):            # test_number == 5
        '''follows from the 3L-R2-D2 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 2
        self.RANGE = 1
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 4.969)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 157.388)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 71.670)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 83.794)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 2), 2230.04)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 4), 0.1159)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 130)
        self.assertEqual(VI.field_data[2], 140)
        self.assertEqual(VI.field_data[3], 150)
        self.assertEqual(VI.field_data[4], 160)
        self.assertEqual(VI.field_data[5], 170)
        self.assertEqual(VI.field_data[6], 175)
        self.assertEqual(VI.field_data[7], 170)
        self.assertEqual(VI.field_data[8], 130)
        self.assertEqual(VI.field_data[9], 100)
        self.assertEqual(VI.field_data[10], 80)
        self.assertEqual(VI.field_data[11], 60)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 157.671)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 157.075)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 156.427)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 153.796)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 151.724)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 143.373)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 136.93)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 116.639)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 105.238)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 92.771)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 90.918)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 117.472)
        print("\"Predicted\" tests Completed")

    def test_3L_R1_D3(self):            # test_number == 6
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(3)
        self.DATASET = 3
        self.RANGE = 1
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 3.110)
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 144.197)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 44.508)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 9.867)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[4], 2), 1075.63)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.06624)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 120)
        self.assertEqual(VI.field_data[3], 115)
        self.assertEqual(VI.field_data[4], 110)
        self.assertEqual(VI.field_data[5], 95)
        self.assertEqual(VI.field_data[6], 40)
        self.assertEqual(VI.field_data[7], 24)
        self.assertEqual(VI.field_data[8], 15)
        self.assertEqual(VI.field_data[9], 10)
        self.assertEqual(VI.field_data[10], 11)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 144.077)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 141.915)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 136.358)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 117.834)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 106.207)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 72.117)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 54.128)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 21.928)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 14.173)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 11.086)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 11.968)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 21.272)
        print("\"Predicted\" tests Completed")

# Layer 2 Tests
    def test_2L_R3_D4(self):            # test_number == 7
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(2)
        self.DATASET = 4
        self.RANGE = 3
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 3.919)
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 123.045)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 202.736)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.01534)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 126)
        self.assertEqual(VI.field_data[3], 129)
        self.assertEqual(VI.field_data[4], 135)
        self.assertEqual(VI.field_data[5], 140)
        self.assertEqual(VI.field_data[6], 150)
        self.assertEqual(VI.field_data[7], 170)
        self.assertEqual(VI.field_data[8], 175)
        self.assertEqual(VI.field_data[9], 180)
        self.assertEqual(VI.field_data[10], 185)
        self.assertEqual(VI.field_data[11], 187)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 123.435)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 123.37)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 124.187)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 127.433)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 129.787)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 138.463)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 144.603)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 162.641)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 172.997)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 187.399)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 194.546)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 200.935)
        print("\"Predicted\" tests Completed")

    def test_2L_R3_D5(self):            # test_number == 8
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(2)
        self.DATASET = 5
        self.RANGE = 3
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 4.660)
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 125.694)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 26.060)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.02455)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 126)
        self.assertEqual(VI.field_data[3], 122)
        self.assertEqual(VI.field_data[4], 120)
        self.assertEqual(VI.field_data[5], 110)
        self.assertEqual(VI.field_data[6], 85)
        self.assertEqual(VI.field_data[7], 65)
        self.assertEqual(VI.field_data[8], 40)
        self.assertEqual(VI.field_data[9], 30)
        self.assertEqual(VI.field_data[10], 26)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 125.937)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 125.237)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 123.949)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 118.826)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 114.926)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 99.920)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 89.002)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 58.017)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 43.231)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 30.136)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 27.366)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 26.260)
        print("\"Predicted\" tests Completed")

    def test_2L_R4_D5(self):            # test_number == 9
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(2)
        self.DATASET = 5
        self.RANGE = 4
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 4.705)
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 130.232)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 25.557)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.02260)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 126)
        self.assertEqual(VI.field_data[3], 122)
        self.assertEqual(VI.field_data[4], 120)
        self.assertEqual(VI.field_data[5], 110)
        self.assertEqual(VI.field_data[6], 85)
        self.assertEqual(VI.field_data[7], 65)
        self.assertEqual(VI.field_data[8], 40)
        self.assertEqual(VI.field_data[9], 30)
        self.assertEqual(VI.field_data[10], 26)
        self.assertEqual(VI.field_data[11], 25)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 130.487)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 129.761)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 128.434)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 123.138)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 119.094)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 103.463)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 92.033)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 59.374)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 43.681)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 29.782)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 26.883)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 25.759)
        print("\"Predicted\" tests Completed")

    def test_2L_R3_D6(self):            # test_number == 10
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(2)
        self.DATASET = 6
        self.RANGE = 3
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 2.682)
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 119.676)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 367.937)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.03132)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 126)
        self.assertEqual(VI.field_data[3], 129)
        self.assertEqual(VI.field_data[4], 135)
        self.assertEqual(VI.field_data[5], 180)
        self.assertEqual(VI.field_data[6], 220)
        self.assertEqual(VI.field_data[7], 250)
        self.assertEqual(VI.field_data[8], 280)
        self.assertEqual(VI.field_data[9], 300)
        self.assertEqual(VI.field_data[10], 310)
        self.assertEqual(VI.field_data[11], 315)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 120.400)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 121.651)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 126.395)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 141.953)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 151.648)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 181.898)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 200.340)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 249.083)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 276.259)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 316.292)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 338.391)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 360.752)
        print("\"Predicted\" tests Completed")

    def test_2L_R4_D6(self):            # test_number == 11
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(2)
        self.DATASET = 6
        self.RANGE = 4
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 9.818)
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 176.162)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 49.803)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.36755)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 125)
        self.assertEqual(VI.field_data[1], 124)
        self.assertEqual(VI.field_data[2], 126)
        self.assertEqual(VI.field_data[3], 129)
        self.assertEqual(VI.field_data[4], 135)
        self.assertEqual(VI.field_data[5], 180)
        self.assertEqual(VI.field_data[6], 220)
        self.assertEqual(VI.field_data[7], 250)
        self.assertEqual(VI.field_data[8], 280)
        self.assertEqual(VI.field_data[9], 300)
        self.assertEqual(VI.field_data[10], 310)
        self.assertEqual(VI.field_data[11], 315)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 176.654)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 176.117)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 175.910)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 175.091)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 174.351)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 170.643)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 166.910)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 147.944)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 129.016)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 89.275)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 66.115)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 51.627)
        print("\"Predicted\" tests Completed")

# Layer 4 Tests

    def test_4L_R5_D7(self):            # test_number == 12
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 7
        self.RANGE = 5
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.801)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 296.297)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 2.375)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 460.889)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 40.382)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 167.079)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 298.098)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.02132)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 303)
        self.assertEqual(VI.field_data[2], 330)
        self.assertEqual(VI.field_data[3], 330)
        self.assertEqual(VI.field_data[4], 310)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 285)
        self.assertEqual(VI.field_data[7], 240)
        self.assertEqual(VI.field_data[8], 205)
        self.assertEqual(VI.field_data[9], 180)
        self.assertEqual(VI.field_data[10], 180)
        self.assertEqual(VI.field_data[11], 210)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 298.282)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 300.867)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 308.955)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 323.200)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 326.504)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 319.994)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 306.873)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 253.749)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 221.967)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 188.291)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 182.863)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 211.336)
        print("\"Predicted\" tests Completed")

    def test_4L_R6_D7(self):            # test_number == 13
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 7
        self.RANGE = 6
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.772)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 297.627)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 1.882)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 487.500)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 45.598)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 173.399)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 399.572)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.02143)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 303)
        self.assertEqual(VI.field_data[2], 330)
        self.assertEqual(VI.field_data[3], 330)
        self.assertEqual(VI.field_data[4], 310)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 285)
        self.assertEqual(VI.field_data[7], 240)
        self.assertEqual(VI.field_data[8], 205)
        self.assertEqual(VI.field_data[9], 180)
        self.assertEqual(VI.field_data[10], 180)
        self.assertEqual(VI.field_data[11], 210)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 299.714)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 302.554)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 310.923)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 324.007)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 325.935)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 314.634)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 299.245)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 245.849)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 217.651)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 190.927)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 188.955)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 229.887)
        print("\"Predicted\" tests Completed")

    def test_4L_R7_D7(self):            # test_number == 14
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 7
        self.RANGE = 7
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 5.203)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 326.917)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 41.975)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 159.527)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 38.790)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 310.892)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 346.099)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.01619)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 303)
        self.assertEqual(VI.field_data[2], 330)
        self.assertEqual(VI.field_data[3], 330)
        self.assertEqual(VI.field_data[4], 310)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 285)
        self.assertEqual(VI.field_data[7], 240)
        self.assertEqual(VI.field_data[8], 205)
        self.assertEqual(VI.field_data[9], 180)
        self.assertEqual(VI.field_data[10], 180)
        self.assertEqual(VI.field_data[11], 210)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 327.865)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 326.471)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 325.099)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 319.611)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 315.244)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 297.320)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 283.185)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 237.207)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 210.511)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 180.763)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 175.656)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 207.723)
        print("\"Predicted\" tests Completed")

    def test_4L_R7_D8(self):            # test_number == 15
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 8
        self.RANGE = 7
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 4.858)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 279.980)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 2.219)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 441.355)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 16.897)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 494.218)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 326.87)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.04340)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 298)
        self.assertEqual(VI.field_data[2], 290)
        self.assertEqual(VI.field_data[3], 270)
        self.assertEqual(VI.field_data[4], 280)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 330)
        self.assertEqual(VI.field_data[7], 370)
        self.assertEqual(VI.field_data[8], 420)
        self.assertEqual(VI.field_data[9], 510)
        self.assertEqual(VI.field_data[10], 507)
        self.assertEqual(VI.field_data[11], 370)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 280.926)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 280.383)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 281.367)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 285.705)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 289.097)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 303.103)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 314.304)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 352.717)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 377.672)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 409.668)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 412.463)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 366.955)
        print("\"Predicted\" tests Completed")

    def test_4L_R6_D8(self):            # test_number == 16
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 8
        self.RANGE = 6
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.183)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 281.464)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 1.099)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 173.206)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 46.318)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 497.618)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 255.004)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.03025)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 298)
        self.assertEqual(VI.field_data[2], 290)
        self.assertEqual(VI.field_data[3], 270)
        self.assertEqual(VI.field_data[4], 280)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 330)
        self.assertEqual(VI.field_data[7], 370)
        self.assertEqual(VI.field_data[8], 420)
        self.assertEqual(VI.field_data[9], 510)
        self.assertEqual(VI.field_data[10], 507)
        self.assertEqual(VI.field_data[11], 370)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 279.515)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 271.915)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 263.794)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 269.129)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 279.065)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 316.906)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 340.329)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 397.152)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 424.521)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 456.117)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 461.746)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 398.611)
        print("\"Predicted\" tests Completed")

    def test_4L_R5_D8(self):            # test_number == 17
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.set_layers(4)
        self.DATASET = 8
        self.RANGE = 5
        VI.GRAPH = False
        self.test_data()
        VI.computePredictions()

        self.assertEqual(round(VI.lowest_rms_values[0], 3), 1.911)
        self.assertEqual(round(VI.lowest_rms_values[3], 3), 268.001)
        print("Layer 1 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[1], 3), 11.240)
        self.assertEqual(round(VI.lowest_rms_values[4], 3), 404.555)
        print("Layer 2 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[2], 3), 46.858)
        self.assertEqual(round(VI.lowest_rms_values[5], 3), 454.764)
        print("Layer 3 tests Completed")
        self.assertEqual(round(VI.lowest_rms_values[6], 3), 293.497)
        print("Layer 4 tests Completed")
        self.assertEqual(round(VI.errmin, 5), 0.05013)
        print("RMS test Completed")

        self.assertEqual(VI.location_data[0], 0.55)
        self.assertEqual(VI.location_data[1], 0.95)
        self.assertEqual(VI.location_data[2], 1.5)
        self.assertEqual(VI.location_data[3], 2.5)
        self.assertEqual(VI.location_data[4], 3)
        self.assertEqual(VI.location_data[5], 4.5)
        self.assertEqual(VI.location_data[6], 5.5)
        self.assertEqual(VI.location_data[7], 9)
        self.assertEqual(VI.location_data[8], 12)
        self.assertEqual(VI.location_data[9], 20)
        self.assertEqual(VI.location_data[10], 30)
        self.assertEqual(VI.location_data[11], 70)
        print("\"Spacing\" tests Completed")

        self.assertEqual(VI.field_data[0], 300)
        self.assertEqual(VI.field_data[1], 298)
        self.assertEqual(VI.field_data[2], 290)
        self.assertEqual(VI.field_data[3], 270)
        self.assertEqual(VI.field_data[4], 280)
        self.assertEqual(VI.field_data[5], 300)
        self.assertEqual(VI.field_data[6], 330)
        self.assertEqual(VI.field_data[7], 370)
        self.assertEqual(VI.field_data[8], 420)
        self.assertEqual(VI.field_data[9], 510)
        self.assertEqual(VI.field_data[10], 507)
        self.assertEqual(VI.field_data[11], 370)
        print("\"Origianl_Data\" tests Completed")

        self.assertEqual(round(VI.pltanswerkeep[0], 3), 269.760)
        self.assertEqual(round(VI.pltanswerkeep[1], 3), 272.221)
        self.assertEqual(round(VI.pltanswerkeep[2], 3), 280.806)
        self.assertEqual(round(VI.pltanswerkeep[3], 3), 302.582)
        self.assertEqual(round(VI.pltanswerkeep[4], 3), 313.482)
        self.assertEqual(round(VI.pltanswerkeep[5], 3), 340.399)
        self.assertEqual(round(VI.pltanswerkeep[6], 3), 353.380)
        self.assertEqual(round(VI.pltanswerkeep[7], 3), 380.486)
        self.assertEqual(round(VI.pltanswerkeep[8], 3), 393.100)
        self.assertEqual(round(VI.pltanswerkeep[9], 3), 411.510)
        self.assertEqual(round(VI.pltanswerkeep[10], 3), 421.277)
        self.assertEqual(round(VI.pltanswerkeep[11], 3), 403.415)
        print("\"Predicted\" tests Completed")

# GUI Tests

    def gui_test_1(self):
        window = Tk()
        gui = VESgui(window)
        gui.argument_init()
        gui.args = gui.parser.parse_args(["-l", "4", "-i", "10000", "-f", "/home/zer0relm/Documents/VESinverse/dataSets/DataSet8.txt", 
                                          "-ti", "1,1,1", "-ta", "2,2,50", "-ri", "1,1,1,1", "-ra", "500,500,500,500"])
        gui.check_arguments()
        self.assertEqual(gui.num_layers, 4)
        print("--layer test Completed")
        self.assertEqual(gui.iterator.get(), 10000)
        print("--iter test Completed")
        self.assertEqual(gui.input_file, "/home/zer0relm/Documents/VESinverse/dataSets/DataSet8.txt")
        print("--file test Completed")
        self.assertEqual(gui.thick_min_layer[0].get(), 1)
        self.assertEqual(gui.thick_min_layer[1].get(), 1)
        self.assertEqual(gui.thick_min_layer[2].get(), 1)
        print("--thickmin test Completed")
        self.assertEqual(gui.thick_max_layer[0].get(), 2)
        self.assertEqual(gui.thick_max_layer[1].get(), 2)
        self.assertEqual(gui.thick_max_layer[2].get(), 50)
        print("--thickmax test Completed")
        self.assertEqual(gui.res_min_layer[0].get(), 1)
        self.assertEqual(gui.res_min_layer[1].get(), 1)
        self.assertEqual(gui.res_min_layer[2].get(), 1)
        self.assertEqual(gui.res_min_layer[3].get(), 1)
        print("--resmin test Completed")
        self.assertEqual(gui.res_max_layer[0].get(), 500)
        self.assertEqual(gui.res_max_layer[1].get(), 500)
        self.assertEqual(gui.res_max_layer[2].get(), 500)
        self.assertEqual(gui.res_max_layer[3].get(), 500)
    
    def gui_test_2(self):
        window = Tk()
        gui = VESgui(window)
        gui.argument_init()
        gui.args = gui.parser.parse_args(["-l", "3", "-i", "10000", "-f", "/home/zer0relm/Documents/VESinverse/dataSets/DataSet1.txt", 
                                          "-ti", "1,10", "-ta", "5,75", "-ri", "20,2,500", "-ra", "200,100,3000"])
        gui.check_arguments()
        self.assertEqual(gui.num_layers, 3)
        print("--layer test Completed")
        self.assertEqual(gui.iterator.get(), 10000)
        print("--iter test Completed")
        self.assertEqual(gui.input_file, "/home/zer0relm/Documents/VESinverse/dataSets/DataSet1.txt")
        print("--file test Completed")
        self.assertEqual(gui.thick_min_layer[0].get(), 1)
        self.assertEqual(gui.thick_min_layer[1].get(), 10)
        print("--thickmin test Completed")
        self.assertEqual(gui.thick_max_layer[0].get(), 5)
        self.assertEqual(gui.thick_max_layer[1].get(), 75)
        print("--thickmax test Completed")
        self.assertEqual(gui.res_min_layer[0].get(), 20)
        self.assertEqual(gui.res_min_layer[1].get(), 2)
        self.assertEqual(gui.res_min_layer[2].get(), 500)
        print("--resmin test Completed")
        self.assertEqual(gui.res_max_layer[0].get(), 200)
        self.assertEqual(gui.res_max_layer[1].get(), 100)
        self.assertEqual(gui.res_max_layer[2].get(), 3000)

        gui.pickFile("/home/zer0relm/Documents/VESinverse/dataSets/DataSet1.txt", 1)
        gui.computation(1)

# test_data
    def test_data(self):
        # hard coded data input - spacing and
        # apparent resistivities measured in the field
        self.t_location_data = [0.55, 0.95, 1.5, 2.5, 3., 4.5,
                       5.5, 9., 12., 20., 30., 70.]

        if self.DATASET == 1:
            self.t_field_data = [125., 110., 95., 40., 24., 15.,
                           10.5, 8., 6., 6.5, 11., 25.]  # DATA 1
        elif self.DATASET == 2:
            self.t_field_data = [125., 130., 140., 150., 160.,
                           170., 175., 170., 130., 100., 80., 60.]  # DATA 2
        elif self.DATASET == 3:
            self.t_field_data = [125., 124., 120., 115., 110.,
                           95., 40., 24., 15., 10., 11., 25.]  # DATA 3
        elif self.DATASET == 4:
            self.t_field_data = [125., 124., 126., 129., 135.,
                           140., 150., 170., 175., 180., 185., 187.]  # DATA 4
        elif self.DATASET == 5:
            self.t_field_data = [125., 124., 126., 122., 120.,
                           110., 85., 65., 40., 30., 26., 25.]  # DATA 5
        elif self.DATASET == 6:
            self.t_field_data = [125., 124., 126., 129., 135.,
                           180., 220., 250., 280., 300., 310., 315.]  # DATA 6
        elif self.DATASET == 7:
            self.t_field_data = [300., 303., 330., 330., 310.,
                           300., 285., 240., 205., 180., 180., 210.]  # DATA 7
        elif self.DATASET == 8:
            self.t_field_data = [300., 298., 290., 270., 280.,
                           300., 330., 370., 420., 510., 507., 370.]  # DATA 8

        # this is where the range in parameters should be input from a GUI
        # I'm hard coding this in for now

        # enter thickenss range for each layer and then resistivity range.
        # for 3 layers small[1] and small[2] are low end of thickness range
        # small[3], small[4] and small[5] are the low end of resistivities
        if self.RANGE == 1:
            # range 1  3-layer case (narrow range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(5)
            self.t_thick_min.append(10.)
            self.t_thick_max.append(75.)

            self.t_res_min.append(20.)
            self.t_res_max.append(200)
            self.t_res_min.append(2.)
            self.t_res_max.append(100.)
            self.t_res_min.append(500.)
            self.t_res_max.append(3000.)
        elif self.RANGE == 2:
            # range 2 3-layer case (broad range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(10)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)

            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
        elif self.RANGE == 3:
            # range 3  2-layer case (broad range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(20)

            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500)
        elif self.RANGE == 4:
            # range 4  2-layer case (small range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(10)

            self.t_res_min.append(50.)
            self.t_res_max.append(200.)
            self.t_res_min.append(1.)
            self.t_res_max.append(50.)
        elif self.RANGE == 5:
            # range 5 4-layer case (small range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(2)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)

            self.t_res_min.append(200.)
            self.t_res_max.append(400.)
            self.t_res_min.append(400.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
        elif self.RANGE == 6:
            # range 6 4-layer case (broad range)
            self.t_thick_min.append(1)
            self.t_thick_max.append(2.)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(2.)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)

            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
        elif self.RANGE == 7:
            # range 7 4-layer case (broadest range)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)
            self.t_thick_min.append(1.)
            self.t_thick_max.append(50.)

            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)
            self.t_res_min.append(1.)
            self.t_res_max.append(500.)

        # INPUT
        self.t_index = 2   # 1 is for shchlumberger and 2 is for Wenner

        VI.set_location_data(self.t_location_data)
        VI.set_field_data(self.t_field_data)
        VI.set_thickness_minimum(self.t_thick_min)
        VI.set_thickness_maximum(self.t_thick_max)
        VI.set_resistivity_minimum(self.t_res_min)
        VI.set_resistivity_maximum(self.t_res_max)
        VI.set_index(self.t_index)
        self.t_thick_min = []
        self.t_thick_max = []
        self.t_res_min = []
        self.t_res_max = []


if __name__ == '__main__':
    test = VEStesting()
    VI = VESinverse()
    VI.set_random(0)
    if len(sys.argv) >= 2:
        input_number = int(sys.argv[1])
        print('\n\nRunning test', input_number)
        test.run_tests(input_number)
        print('\n\nFinished test,', input_number)
    else:
        for i in range(1, 20):
            print("Runing test", i)
            test.run_tests(i)
            print("Finished test", i, "\n\n")

