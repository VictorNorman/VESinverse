import unittest
import sys
from tkinter import Tk, IntVar 
import VESinverse as VI         #This will change when splitting file into GUI and Computation


class VEStesting(unittest.TestCase):
    def test_1(self):
        '''test_1 follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        formating = Tk() # this is needed for the IntVar to work
        VI.num_iter = IntVar(Tk(), 10000)
        #VI.num_iter = 1000
        VI.pickFile(1)
        VI.num_layers_var = IntVar(formating, 3)
        VI.thick_min_layer = [IntVar(formating, 1), IntVar(formating, 10)]
        VI.thick_max_layer = [IntVar(formating, 5), IntVar(formating, 75)]
        VI.res_min_layer = [IntVar(formating, 20), IntVar(formating, 2), IntVar(formating, 500)]
        VI.res_max_layer = [IntVar(formating, 200), IntVar(formating, 100), IntVar(formating, 3000)]

        VI.computePredictions(1)
    
        self.assertEqual(VI.pkeep[1], 1.2402873838963382)
        self.assertEqual(VI.pkeep[3], 145.89820038052548)
        self.assertEqual(VI.pkeep[2], 20.933615798098383)
        self.assertEqual(VI.pkeep[4], 5.976789941121553)
        self.assertEqual(VI.pkeep[5], 850.818877722824)

if __name__ == '__main__':
    test = VEStesting()
    test.test_1()