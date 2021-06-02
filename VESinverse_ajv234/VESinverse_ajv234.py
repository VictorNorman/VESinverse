# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:32:48 2016

@author: jclark

this code uses the Ghosh method to determine the apparent resistivities
for a layered earth model. Either schlumberger or Wenner configurations
can be used
"""


import numpy as np
import random
import matplotlib.pyplot as plt
import sys


class VESinverse:
    def __init__(self): 
        # For Testing Purposes
        # Only the Test suit should edit these Constants
        self.LAYERS = 4
        self.DATASET = 7
        self.RANGE = 5
        self.GRAPH = True

        ARRAYSIZE = 65

        # Schlumberger filter
        self.fltr1 = [0., .00046256, -.0010907, .0017122, -.0020687,
                .0043048, -.0021236, .015995, .017065, .098105, .21918, .64722,
                1.1415, .47819, -3.515, 2.7743, -1.201, .4544, -.19427, .097364,
                -.054099, .031729, -.019109, .011656, -.0071544, .0044042,
                -.002715, .0016749, -.0010335, .00040124]

        # Wenner Filter
        self.fltr2 = [0., .000238935, .00011557, .00017034, .00024935,
                .00036665, .00053753, .0007896, .0011584, .0017008, .0024959,
                .003664, .0053773, .007893, .011583, .016998, .024934, .036558,
                .053507, .078121, .11319, .16192, .22363, .28821, .30276, .15523,
                -.32026, -.53557, .51787, -.196, .054394, -.015747, .0053941,
                -.0021446, .000665125]

        # I know there must be a better method to assign lists. And probably numpy
        # arrays would be best. But my Python wasn't up to it. If the last letter
        # is an 'l' that means it is a log10 of the value

        # 65 is completely arbitrary
        self.p = [0]*20                              #Prediction?
        self.r = [0]*ARRAYSIZE                       #Resistivity?
        self.rl = [0]*ARRAYSIZE                      #Resistivity? log10
        self.t = [0]*50
        self.b = [0]*ARRAYSIZE
        self.asav = [0]*ARRAYSIZE
        self.asavl = [0]*ARRAYSIZE
        self.adatl = [0]*ARRAYSIZE
        self.rdatl = [0]*ARRAYSIZE
        self.adat = [0]*ARRAYSIZE
        self.rdat = [0]*ARRAYSIZE
        self.pkeep = [0]*ARRAYSIZE
        self.rkeep = [0]*ARRAYSIZE
        self.rkeepl = [0]*ARRAYSIZE
        self.pltanswer = [0]*ARRAYSIZE
        self.pltanswerl = [0]*ARRAYSIZE
        self.pltanswerkeep = [0]*ARRAYSIZE
        self.pltanswerkeepl = [0]*ARRAYSIZE

        self.small = [0]*ARRAYSIZE
        self.xlarge = [0]*ARRAYSIZE

        self.x = [0]*100
        self.y = [0]*100
        self.y2 = [0]*100
        self.u = [0]*5000
        self.new_x = [0]*1000
        self.new_y = [0]*1000
        self.ndat = 13

    def data_init(self):
        # hard coded data input - spacing and apparent resistivities measured
        # in teh field
        self.adat = [0., 0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30., 70.]

        if self.DATASET == 1:
            self.rdat = [0., 125., 110., 95., 40., 24., 15.,
                    10.5, 8., 6., 6.5, 11., 25.]  # DATA 1
        elif self.DATASET == 2:
            self.rdat = [0., 125., 130., 140., 150., 160.,
                    170., 175., 170., 130., 100., 80., 60.]  # DATA 2
        elif self.DATASET == 3:
            self.rdat = [0., 125., 124., 120., 115., 110.,
                    95., 40., 24., 15., 10., 11., 25.]  # DATA 3
        elif self.DATASET == 4:
            self.rdat = [0.,  125., 124., 126., 129., 135.,
                    140., 150., 170., 175., 180., 185., 187.]  # DATA 4
        elif self.DATASET == 5:
            self.rdat = [0.,  125., 124., 126., 122., 120.,
                    110., 85., 65., 40., 30., 26., 25.]  # DATA 5
        elif self.DATASET == 6:
            self.rdat = [0.,  125., 124., 126., 129., 135.,
                    180., 220., 250., 280., 300., 310., 315.]  # DATA 6
        elif self.DATASET == 7:
            self.rdat = [0., 300., 303., 330., 330., 310.,
                    300., 285., 240., 205., 180., 180., 210.]  # DATA 7
        elif self.DATASET == 8:
            self.rdat = [0., 300., 298., 290., 270., 280.,
                    300., 330., 370., 420., 510., 507., 370.]  # DATA 8
        self.one30 = 1.e30
        self.rms = self.one30
        self.errmin = 1.e10

        # INPUT
        self.index = 2   # 1 is for shchlumberger and 2 is for Wenner

        if self.LAYERS == 3:
            self.layer = 3
        elif self.LAYERS == 2:
            self.layer = 2
        elif self.LAYERS == 4:
            self.layer = 4

        self.layer_index = 2 * self.layer - 1     # layer (e) and layer_index (n) variables have been updated

        self.electrode_spacing = 0.2  # smallest electrode spacing
        self.resistivity_points_number = 20  # number of points where resistivity is calculated (Variable was m)

        self.electrode_spacing = np.log(self.electrode_spacing)
        self.delx = np.log(10.0)/6.

        # these lines apparently find the computer precision ep
        self.ep = 1.0
        self.ep = self.ep/2.0
        self.fctr = self.ep+1.
        while self.fctr > 1.:
            self.ep = self.ep/2.0
            self.fctr = self.ep+1.

        # this is where the range in parameters should be input from a GUI
        # I'm hard coding this in for now

        # enter thickenss range for each layer and then resistivity range.
        # for 3 layers small[1] and small[2] are low end of thickness range
        # small[3], small[4] and small[5] are the low end of resistivities
        if self.RANGE == 1:
            # range 1  3-layer case (narrow range)
            self.small[1] = 1.
            self.xlarge[1] = 5
            self.small[2] = 10.
            self.xlarge[2] = 75.
            self.small[3] = 20.
            self.xlarge[3] = 200.
            self.small[4] = 2.
            self.xlarge[4] = 100
            self.small[5] = 500.
            self.xlarge[5] = 3000.
        elif self.RANGE == 2:
            # range 2 3-layer case (broad range)
            self.small[1] = 1.
            self.xlarge[1] = 10
            self.small[2] = 1.
            self.xlarge[2] = 50.
            self.small[3] = 1.
            self.xlarge[3] = 500.
            self.small[4] = 1.
            self.xlarge[4] = 500.
            self.small[5] = 1.
            self.xlarge[5] = 500.
        elif self.RANGE == 3:
            # range 3  2-layer case (broad range)
            self.small[1] = 1.
            self.xlarge[1] = 20
            self.small[2] = 1.
            self.xlarge[2] = 500.
            self.small[3] = 1.
            self.xlarge[3] = 500
        elif self.RANGE == 4:
            # range 4  2-layer case (small range)
            self.small[1] = 1.
            self.xlarge[1] = 10
            self.small[2] = 50.
            self.xlarge[2] = 200.
            self.small[3] = 1.
            self.xlarge[3] = 50.
        elif self.RANGE == 5:
            # range 5 4-layer case (small range)
            self.small[1] = 1.
            self.xlarge[1] = 2
            self.small[2] = 1.
            self.xlarge[2] = 50.
            self.small[3] = 1.
            self.xlarge[3] = 50.
            self.small[4] = 200.
            self.xlarge[4] = 400.
            self.small[5] = 400.
            self.xlarge[5] = 500.
            self.small[6] = 1.
            self.xlarge[6] = 500.
            self.small[7] = 1.
            self.xlarge[7] = 500.
        elif self.RANGE == 6:
            # range 6 4-layer case (broad range)
            self.small[1] = 1
            self.xlarge[1] = 2
            self.small[2] = 1.
            self.xlarge[2] = 2.
            self.small[3] = 1.
            self.xlarge[3] = 50.
            self.small[4] = 1.
            self.xlarge[4] = 500.
            self.small[5] = 1.
            self.xlarge[5] = 500.
            self.small[6] = 1.
            self.xlarge[6] = 500.
            self.small[7] = 1.
            self.xlarge[7] = 500.
        elif self.RANGE == 7:
            # range 7 4-layer case (broadest range)
            self.small[1] = 1
            self.xlarge[1] = 50
            self.small[2] = 1.
            self.xlarge[2] = 50.
            self.small[3] = 1.
            self.xlarge[3] = 50.
            self.small[4] = 1.
            self.xlarge[4] = 500.
            self.small[5] = 1.
            self.xlarge[5] = 500.
            self.small[6] = 1.
            self.xlarge[6] = 500.
            self.small[7] = 1.
            self.xlarge[7] = 500.

        self.iter = 10000  # number of iterations for the Monte Carlo guesses. to be input on GUI


    def readData(self):
        # normally this is where the data would be read from the csv file
        # but now I'm just hard coding it in as global lists

        for i in range(1, self.ndat, 1):
            self.adatl[i] = np.log10(self.adat[i])
            self.rdatl[i] = np.log10(self.rdat[i])

        return


    def error(self):
        sumerror = 0.
        # pltanswer = [0]*64
        self.spline(self.resistivity_points_number, self.one30, self.one30, self.asavl, self.rl, self.y2)
        for i in range(1, self.ndat, 1):
            ans = self.splint(self.resistivity_points_number, self.adatl[i], self.asavl, self.rl, self.y2)
            sumerror = sumerror + (self.rdatl[i] - ans) * (self.rdatl[i] - ans)
            # print(i,sum1,rdat[i],rdatl[i],ans)
            self.pltanswerl[i] = ans
            self.pltanswer[i] = np.power(10, ans)
        self.rms = np.sqrt(sumerror/(self.ndat-1))

        # check the spline routine
        # for i in range(1,m+1,1):
        #     anstest = splint(m, asavl[i],asavl,rl,y2)
        #     print( asavl[i], rl[i], anstest)
        # print(' rms  =  ', rms)
    # if you erally want to get a good idea of all perdictions from Montecarlo
    # perform the following plot (caution - change iter to a smaller number)
        # plt.loglog(adat[1:ndat],pltanswer[1:ndat])
        return self.rms


    def transf(self, y, i):
        self.u = 1./np.exp(y)
        self.t[1] = self.p[self.layer_index]
        for j in range(2, self.layer+1, 1):
            pwr = -2. * self.u * self.p[self.layer + 1 - j]
            if pwr < np.log(2. * self.ep):
                pwr = np.log(2. * self.ep)
            a = np.exp(pwr)
            b = (1. - a)/(1. + a)
            rs = self.p[self.layer_index + 1 - j]
            tpr = b*rs
            self.t[j] = (tpr + self.t[j - 1]) / (1. + tpr * self.t[j - 1] / (rs * rs))
        self.r[i] = self.t[self.layer]
        return


    def filters(self, b, k):
        for i in range(1, self.resistivity_points_number + 1, 1):
            re = 0.
            for j in range(1, k + 1, 1):
                re = re + b[j] * self.r[i + k - j]
            self.r[i] = re
        return


    def rmsfit(self):
        if self.index == 1:
            self.y = self.electrode_spacing -19. * self.delx - 0.13069
            mum1 = self.resistivity_points_number + 28
            for i in range(1, mum1 + 1, 1):
                self.transf(self.y, i)
                self.y = self.y + self.delx
            self.filters(self.fltr1, 29)
        elif self.index == 2:
            s = np.log(2.)
            self.y = self.electrode_spacing -10.8792495 * self.delx
            mum2 = self.resistivity_points_number + 33
            for i in range(1, mum2 + 1, 1):
                self.transf(self.y, i)
                a = self.r[i]
                self.y1 = self.y + s
                self.transf(self.y1, i)
                self.r[i] = 2. * a - self.r[i]
                self.y = self.y + self.delx
            self.filters(self.fltr2, 34)
        else:
            print(" type of survey not indicated")
            sys.exit()

        x = self.electrode_spacing
        # print("A-Spacing   App. Resistivity")
        for i in range(1, self.resistivity_points_number+1, 1):
            a = np.exp(x)
            self.asav[i] = a
            self.asavl[i] = np.log10(a)
            self.rl[i] = np.log10(self.r[i])
            x = x + self.delx
            # print("%7.2f   %9.3f " % ( asav[i], r[i]))

        self.rms = self.error()

        return self.rms

    # my code to do a spline fit to predicted data at the nice spacing of Ghosh
    # use splint to determine the spline interpolated prediction at the
    # spacing where the measured resistivity was taken - to compare observation
    # to prediction


    def spline(self, n, yp1, ypn, x=[], y=[], y2=[]):
        u = [0] * 1000
        one29 = 0.99e30
        # print(x,y)
        if yp1 > one29:
            y2[0] = 0.
            u[0] = 0.
        else:
            y2[0] = -0.5
            u[0] = (3. / (x[1] - x[0])) * ((y[1] - y[0]) / (x[1] - x[0]) - yp1)

        for i in range(1, n):
            # print(i,x[i])
            sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
            p = sig * y2[i - 1] + 2.
            y2[i] = (sig - 1.) / p
            u[i] = ((6. * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) - (y[i] - y[i - 1]) /
                        (x[i] - x[i - 1])) / (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p)

        if ypn > one29:
            qn = 0.
            un = 0.
        else:
            qn = 0.5
            un = (3. / (x[n] - x[n - 1])) * (ypn - (y[n] - y[n - 1]) / (x[n] - x[n - 1]))

        y2[n] = (un - qn * u[n - 1]) / (qn * y2[n - 1] + 1.)
        for k in range(n-1, -1, -1):
            y2[k] = y2[k] * y2[k + 1] + u[k]

        return


    def splint(self, n, x, xa=[], ya=[], y2a=[]):
        klo = 0
        khi = n
        while khi - klo > 1:
            k = int((khi + klo) // 2)
            if xa[k] > x:
                khi = k
            else:
                klo = k
        h = xa[khi] - xa[klo]
        if abs(h) < 1e-20:
            print(" bad xa input")
        # print(x,xa[khi],xa[klo])
        a = (xa[khi] - x) / h
        b = (x - xa[klo]) / h
        y = (a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2a[klo] +
                                (b * b * b - b) * y2a[khi]) * (h * h) / 6.)
        # print("x=   ", x,"y=  ", y, "  ya=  ", ya[khi],"  y2a=  ", y2a[khi], "  h=  ",h)

        return y


    def computePredictions(self):

        # # TODO: This should be GONE by the end of Summer
        # global iter
        # global num_iter
        # global num_layers
        # global num_layers_var
        # global layer_index
        # global thick_min_layer
        # global thick_max_layer
        # global res_min_layer
        # global res_max_layer
        # global adat
        # global rdat
        # global ndat
        # global rms
        # global errmin
        # global pkeep
        # global asav
        # global asavl
        # global rkeep
        # global rkeepl
        # global pltanswerkeep

        # Turn off randomization (for now)
        random.seed(0)

        self.readData()
        print(self.adat[1:self.ndat], self.rdat[1:self.ndat])
        for iloop in range(1, self.iter+1, 1):
            # print( '  iloop is ', iloop)
            for i in range(1, self.layer_index + 1, 1):
                randNumber = random.random()
                # print(randNumber, '  random')
                self.p[i] = (self.xlarge[i] - self.small[i])*randNumber + self.small[i]

            self.rms = self.rmsfit()

            if self.rms < self.errmin:
                print('rms  ', self.rms, '   errmin ', self.errmin)
                for i in range(1, self.layer_index + 1, 1):
                    self.pkeep[i] = self.p[i]
                for i in range(1, self.resistivity_points_number+1, 1):
                    self.rkeep[i] = self.r[i]
                    self.rkeepl[i] = self.rl[i]
                for i in range(1, self.ndat+1, 1):
                    self.pltanswerkeepl[i] = self.pltanswerl[i]
                    self.pltanswerkeep[i] = self.pltanswer[i]
                self.errmin = self.rms

    # output the best fitting earth model
        print(' Layer ', '     Thickness  ', '   Res_ohm-m  ')
        for i in range(1, self.layer, 1):
            print(i, self.pkeep[i], self.pkeep[self.layer+i-1])

        print(self.layer, '  Infinite ', self.pkeep[self.layer_index])
        for i in range(1, self.resistivity_points_number+1, 1):
            self.asavl[i] = np.log10(self.asav[i])

    # output the error of fit
        print(' RMS error   ', self.errmin)
        print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
        for i in range(1, self.resistivity_points_number+1, 1):
            # print(asav[i], rkeep[i], asavl[i], rkeepl[i])
            print("%9.3f   %9.3f  %9.3f  %9.3f" % (self.asav[i], self.rkeep[i],
                                                self.asavl[i], self.rkeepl[i]))

        plt.loglog(self.asav[1:self.resistivity_points_number], self.rkeep[1:self.resistivity_points_number], '-')  # resistivity prediction curve
        plt.loglog(self.adat[1:self.ndat], self.pltanswerkeep[1:self.ndat],
                'ro')  # predicted data red dots
        s = 7
        plt.loglog(self.adat[1:self.ndat], self.rdat[1:self.ndat], 'bo',
                markersize=s)  # original data blue dots

        # output the ranges cpmstraining the model

        print('   Small', '   Large')
        for i in range(1, self.layer_index+1, 1):
            print("%9.3f %9.3f" % (self.small[i], self.xlarge[i]))

    # output the final rms
        print(' RMS_=   ', "%9.6f" % self.errmin)

        # output the best fitting earth model
        print('   Layer ', '   Thickness  ', 'Res_ohm-m  ')
        for i in range(1, self.layer, 1):
            print("%9.1f   %9.3f  %9.3f" % (i, self.pkeep[i], self.pkeep[self.layer+i-1]))

        print("%9.1f" % self.layer, '  Infinite ', "%9.3f" % self.pkeep[self.layer_index])

        # output the original data and the predicted data
        print('  Spacing', '  Original_Data', ' Predicted')
        for i in range(1, self.ndat, 1):
            print("%9.3f  %9.3f  %9.3f" % (self.adat[i], self.rdat[i], self.pltanswerkeep[i]))
        if self.GRAPH is True:
            plt.show()
            plt.grid(True)
            sys.exit(0)


# main here
if __name__ == '__main__':
    VI = VESinverse()
    VI.data_init()
    VI.computePredictions()
