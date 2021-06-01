import unittest
import VESinverse as VI#This will change when splitting file into GUI and Computation


class VEStesting(unittest.TestCase):
    def test_1(self):
        '''test_1 follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        VI.num_iter = 1000
        VI.num_layers = 3
        
    


if __name__ == '__main__':
    test = VEStesting()
    test.test_1()