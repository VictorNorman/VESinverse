import unittest
import sys
import tkinter as tk 
import VESinverse as VI#This will change when splitting file into GUI and Computation


class VEStesting(unittest.TestCase):
    def test_1(self):
        '''test_1 follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        #VI.num_iter = IntVar(tk.Tk(), 10000)
        #VI.num_iter = 1000
        VI.iter = 1000
        VI.num_layers = 3
        VI.thick_min_layer = [1, 10]
        VI.thick_max_layer = [5, 75]
        VI.res_min_layer = [20, 2, 500]
        VI.res_max_layer = [200, 100, 3000]

        VI.computePredictions()
    


if __name__ == '__main__':
    test = VEStesting()
    test.test_1()