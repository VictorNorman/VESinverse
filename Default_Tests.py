import unittest
import VESinverse_JClark as VI         #This will change when splitting file into GUI and Computation


class VEStesting(unittest.TestCase):
    def test_3L_R1_D1(self):
        '''follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        
        VI.computePredictions()

        self.assertEqual(VI.pkeep[1], 1.2402873838963382)
        self.assertEqual(VI.pkeep[3], 145.89820038052548)
        print("Layer 1 tests Completed")
        self.assertEqual(VI.pkeep[2], 20.933615798098383)
        self.assertEqual(VI.pkeep[4], 5.976789941121553)
        print("Layer 2 tests Completed")
        self.assertEqual(VI.pkeep[5], 850.818877722824)
        print("Layer 3 tests Completed")
    def test_3L_R2_D3(self):
        '''follows from the 3L-R2-D3 page in
            modelTestsForVerification'''
        VI.LAYERS = 3
        VI.DATASET = 3
        VI.RANGE = 2
if __name__ == '__main__':
    VI.LAYERS = 3   
    VI.DATASET = 1
    VI.RANGE = 2
    VI.GRAPH = False
    test = VEStesting()
    test.test_3L_R1_D1()