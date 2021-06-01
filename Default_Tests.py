import unittest
import VESinverse_JClark as VI         #This will change when splitting file into GUI and Computation


class VEStesting(unittest.TestCase):
    def test_1(self):
        '''test_1 follows from the 3L-R1-D1 page in
            modelTestsForVerification'''
        VI.computePredictions()
        self.assertEqual(VI.pkeep[1], 1.2402873838963382)
        self.assertEqual(VI.pkeep[3], 145.89820038052548)
        self.assertEqual(VI.pkeep[2], 20.933615798098383)
        self.assertEqual(VI.pkeep[4], 5.976789941121553)
        self.assertEqual(VI.pkeep[5], 850.818877722824)

if __name__ == '__main__':
    test = VEStesting()
    test.test_1()