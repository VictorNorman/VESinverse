# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:32:48 2016

@author: jclark

this code uses the Ghosh method to determine the apparent resistivities
for a layered earth model. Either schlumberger or Wenner configurations
can be used
"""


import math
import random
# import matplotlib.pyplot as plt
import sys




class VESinverse:
    def __init__(self):

        ARRAYSIZE = 65

        # Schlumberger filter
        self.fltr1 = [.00046256, -.0010907, .0017122, -.0020687,
                      .0043048, -.0021236, .015995, .017065, .098105,
                      .21918, .64722, 1.1415, .47819, -3.515, 2.7743,
                      -1.201, .4544, -.19427, .097364, -.054099, .031729,
                      -.019109, .011656, -.0071544, .0044042,
                      -.002715, .0016749, -.0010335, .00040124]

        # Wenner Filter
        self.fltr2 = [.000238935, .00011557, .00017034, .00024935,
                      .00036665, .00053753, .0007896, .0011584, .0017008,
                      .0024959, .003664, .0053773, .007893, .011583,
                      .016998, .024934, .036558, .053507, .078121, .11319,
                      .16192, .22363, .28821, .30276, .15523,
                      -.32026, -.53557, .51787, -.196, .054394, -.015747,
                      .0053941, -.0021446, .000665125]

        # I know there must be a better method to assign lists.
        # And probably numpy arrays would be best.
        # But my Python wasn't up to it. If the last letter
        # is an 'l' that means it is a log10 of the value

        # I can't seem to get rid of any ARRAYSIZE except on adat and rdat
        # because the first time they are referenced it is within a loop and
        # thus append would not really work

        # 65 is completely arbitrary
        self.p = []                             # Prediction?
        self.r = [0]*ARRAYSIZE                       # Resistivity?
        self.rl = [0]*ARRAYSIZE                      # Resistivity?
        self.t = [0]*50
        self.b = [0]*ARRAYSIZE
        self.asav = [0]*ARRAYSIZE
        self.asavl = [0]*ARRAYSIZE
        self.adatl = [0]*ARRAYSIZE
        self.rdatl = [0]*ARRAYSIZE
        self.adat = []                              # Spacing? out puts under the spacing tag 
        self.rdat = []                              # Original_data? outputs under the original_data tag
        self.pkeep = []                             # Final predictions? it is the array where the layer data ends up
        self.rkeep = []
        self.rkeepl = []
        self.pltanswer = []
        self.pltanswerl = []
        self.pltanswerkeep = []                     # Predictions? outputs under the Predictions tag
        self.pltanswerkeepl = []                    

        self.thickness_minimum = []
        self.resistivity_minimum = []
        self.thickness_maximum = []
        self.resistivity_maximum = []

        self.x = [0]*100
        # self.y = [0]*100
        self.y2 = [0]*100
        self.u = [0]*5000
        self.new_x = [0]*1000
        self.new_y = [0]*1000
        self.ndat = 12

        # These variables are temp names to replace matplotlib
        self.x_axis = []
        self.y_axis = []
        self.red_x = []
        self.red_y = []
        self.blue_x = []
        self.blue_y = []

        # number of iterations for the Monte Carlo guesses. to be input on GUI
        self.iter = 10000

        self.layer = 3

    def data_init(self):
        self.one30 = 1.e30
        self.rms = self.one30
        self.errmin = 1.e10

        # self.layer_index is used to offset now only pkeep for 
        self.layer_index = 2 * self.layer - 1

        # smallest electrode spacing
        self.electrode_spacing = 0.2
        # number of points where resistivity is calculated (Variable was m)
        self.resistivity_points_number = 20

        self.electrode_spacing = math.log(self.electrode_spacing)
        self.delx = math.log(10.0)/6.

        # these lines apparently find the computer precision ep
        self.ep = 1.0
        self.ep = self.ep/2.0
        self.fctr = self.ep+1.
        while self.fctr > 1.:
            self.ep = self.ep/2.0
            self.fctr = self.ep+1.

    # ----------- Getters and Setters -------------
    def get_iter(self):
        return self.iter

    def set_iter(self, new_iterations):
        self.iter = new_iterations

    def get_layers(self):
        return self.layer

    def set_layers(self, new_layer_number):
        self.layer = new_layer_number

    def get_adat(self):
        return self.adat

    def set_adat(self, gui_adat_array):
        self.adat = gui_adat_array

    def get_rdat(self):
        return self.rdat

    def set_rdat(self, gui_rdat_array):
        self.rdat = gui_rdat_array

    def set_ndat(self, new_ndat_number):
        self.ndat = new_ndat_number

    def get_ndat(self):
        return self.ndat

    # ----------- replacements for small and xlarge ----------
    def set_thickness_minimum(self, new_thick_min):
        self.thickness_minimum = new_thick_min

    def get_thickness_minimum(self):
        return self.thickness_minimum

    def set_thickness_maximum(self, new_thick_max):
        self.thickness_maximum = new_thick_max

    def get_thickness_maximum(self):
        return self.thickness_maximum

    def set_resistivity_minimum(self, new_res_min):
        self.resistivity_minimum = new_res_min

    def get_resistivity_minimum(self):
        return self.resistivity_minimum

    def set_resistivity_maximum(self, new_res_max):
        self.resistivity_maximum = new_res_max

    def get_resistivity_maximum(self):
        return self.resistivity_maximum
    # -------------------------------------------------------

    def get_pkeep(self):
        return self.pkeep

    def set_index(self, new_index):
        self.index = new_index

    def get_errmin(self):
        return self.errmin

    def get_layer_index(self):
        return self.layer_index
    
    def set_random(self, seed):
        random.seed(seed)
    
    def get_x_axis(self):
        return self.x_axis
    
    def get_y_axis(self):
        return self.y_axis

    def get_red_x(self):
        return self.red_x
    
    def get_red_y(self):
        return self.red_y
    
    def get_blue_x(self):
        return self.blue_x

    def get_blue_y(self):
        return self.blue_y
    
    def get_resistivity_point(self):
        return self.resistivity_points_number
    # ---------------------------------------------

    def readData(self):
        # normally this is where the data would be read from the csv file
        # but now I'm just hard coding it in as global lists
        for i in range(0, self.ndat, 1):
            self.adatl[i] = math.log10(self.adat[i])
            self.rdatl[i] = math.log10(self.rdat[i])

    def error(self):
        self.pltanswer.clear()
        self.pltanswerl.clear()
        sumerror = 0.
        # pltanswer = [0]*64
        self.spline(self.resistivity_points_number, self.one30, self.one30,
                    self.asavl, self.rl, self.y2)
        for i in range(0, self.ndat, 1):
            ans = self.splint(self.resistivity_points_number, self.adatl[i],
                              self.asavl, self.rl, self.y2)
            sumerror = sumerror + (self.rdatl[i] - ans) * (self.rdatl[i] - ans)
            # print(i,sum1,rdat[i],rdatl[i],ans)
            self.pltanswerl.append(ans)
            self.pltanswer.append(math.pow(10, ans))
        self.rms = math.sqrt(sumerror/(self.ndat))

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
        self.u = 1./math.exp(y)
        self.t[0] = self.p[self.layer_index-1]
        # print('\n', y, '\n', i, '\n', self.p, '\n', self.t)
        # raise Exception("Pause")
        for j in range(1, self.layer, 1):
            pwr = -2. * self.u * self.p[self.layer - 1 - j]
            if pwr < math.log(2. * self.ep):
                pwr = math.log(2. * self.ep)
            a = math.exp(pwr)
            b = (1. - a)/(1. + a)
            rs = self.p[self.layer_index - 1 - j]
            tpr = b*rs
            self.t[j] = (tpr + self.t[j - 1]) / (1. + tpr * self.t[j - 1] /
                                                 (rs * rs))
        self.r[i] = self.t[self.layer-1]

    def filters(self, b, k):
        for i in range(0, self.resistivity_points_number, 1):
            re = 0.
            for j in range(0, k, 1):
                re = re + b[j] * self.r[i + k - j - 1]
            self.r[i] = re

    def rmsfit(self):
        if self.index == 1:
            self.y = self.electrode_spacing - 19. * self.delx - 0.13069
            mum1 = self.resistivity_points_number + 28
            for i in range(0, mum1, 1):
                self.transf(self.y, i)
                self.y = self.y + self.delx
            self.filters(self.fltr1, 29)
        elif self.index == 2:
            s = math.log(2.)
            self.y = self.electrode_spacing - 10.8792495 * self.delx
            mum2 = self.resistivity_points_number + 33
            for i in range(0, mum2, 1):
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
        for i in range(0, self.resistivity_points_number, 1):
            a = math.exp(x)
            self.asav[i] = a
            self.asavl[i] = math.log10(a)
            self.rl[i] = math.log10(self.r[i])
            x = x + self.delx
            # print("%7.2f   %9.3f " % ( asav[i], r[i]))

        self.rms = self.error()

        return self.rms

    # my code to do a spline fit to predicted data at the nice spacing of Ghosh
    # use splint to determine the spline interpolated prediction at the
    # spacing where the measured resistivity was taken - to compare observation
    # to prediction

    # What does this do? It doesn't modify any self. variable
    # x, y, y2 and p are the only ones that are self. variables and the first
    # three are local and the operations done on p mean that it cannot be
    # self.p because it is an array
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

        for i in range(0, n-1):
            # print(i,x[i])
            sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
            p = sig * y2[i - 1] + 2.
            y2[i] = (sig - 1.) / p
            u[i] = ((6. * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) -
                           (y[i] - y[i - 1]) /
                           (x[i] - x[i - 1])) / (x[i + 1] - x[i - 1]) - sig *
                     u[i - 1]) / p)

        if ypn > one29:
            qn = 0.
            un = 0.
        else:
            qn = 0.5
            un = (3. / (x[n] - x[n - 1])) * (ypn - (y[n] - y[n - 1]) /
                                             (x[n] - x[n - 1]))

        y2[n] = (un - qn * u[n - 1]) / (qn * y2[n - 1] + 1.)
        for k in range(n-1, -1, -1):
            y2[k] = y2[k] * y2[k + 1] + u[k]

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
                                          (b * b * b - b) * y2a[khi]) *
             (h * h) / 6.)
        # print("x=   ", x,"y=  ", y, "  ya=  ", ya[khi],"
        #       y2a=  ", y2a[khi], "  h=  ",h)

        return y

    def computePredictions(self):
        self.data_init()
        # Turn off randomization (for now)
        # self.set_random(0)

        self.readData()

        print(self.adat[0:self.ndat], self.rdat[0:self.ndat])
        # for iloop in range(0, self.iter, 1):
        #     # print( '  iloop is ', iloop)
        #     for i in range(0, self.layer_index, 1):
        #         randNumber = random.random()
        #         # print(randNumber, '  random')
        #         self.p[i] = (self.xlarge[i] - self.small[i])*randNumber + self.small[i]
        for iloop in range(0, self.iter, 1):
            self.p.clear()
            for i in range(0, self.layer - 1):
                randNumber = random.random()
                self.p.append((self.thickness_maximum[i] - self.thickness_minimum[i])*randNumber + self.thickness_minimum[i])
                # print(f"thickness random: {randNumber}")
            for i in range(0, self.layer):
                randNumber = random.random()
                self.p.append((self.resistivity_maximum[i] - self.resistivity_minimum[i])*randNumber + self.resistivity_minimum[i])
                # print(f"resistivity random: {randNumber}")
                # raise Exception("debug")

            # print(self.p)
            self.rms = self.rmsfit()

            if self.rms < self.errmin:
                self.pkeep.clear()
                self.rkeep.clear()
                self.rkeepl.clear()
                self.pltanswerkeep.clear()
                self.pltanswerkeepl.clear()
                print('rms  ', self.rms, '   errmin ', self.errmin)
                for i in range(0, self.layer_index, 1):
                    self.pkeep.append(self.p[i])
                for i in range(0, self.resistivity_points_number, 1):
                    self.rkeep.append(self.r[i])
                    self.rkeepl.append(self.rl[i])
                for i in range(0, self.ndat, 1):
                    self.pltanswerkeepl.append(self.pltanswerl[i])
                    self.pltanswerkeep.append(self.pltanswer[i])
                self.errmin = self.rms

    # output the best fitting earth model
        print(' Layer ', '     Thickness  ', '   Res_ohm-m  ')
        for i in range(0, self.layer - 1, 1):
            print(i, self.pkeep[i], self.pkeep[self.layer+i-1])

        print(self.layer, '  Infinite ', self.pkeep[self.layer_index-1])
        for i in range(0, self.resistivity_points_number, 1):
            self.asavl[i] = math.log10(self.asav[i])

    # output the error of fit
        print(' RMS error   ', self.errmin)
        print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
        for i in range(0, self.resistivity_points_number, 1):
            # print(asav[i], rkeep[i], asavl[i], rkeepl[i])
            print("%9.3f   %9.3f  %9.3f  %9.3f" % (self.asav[i], self.rkeep[i],
                                                   self.asavl[i], self.rkeepl[i]))

        # plt.loglog(self.asav[1:self.resistivity_points_number], self.rkeep[1:self.resistivity_points_number], '-')  # resistivity prediction curve
        for i in range(self.resistivity_points_number):
            self.x_axis.append(self.asav[i])
            self.y_axis.append(self.rkeep[i])
        for i in range(self.ndat):
            self.red_x.append(self.adat[i])
            self.blue_x.append(self.adat[i])
            self.red_y.append(self.pltanswerkeep[i])
            self.blue_y.append(self.rdat[i])

        # plt.loglog(self.adat[1:self.ndat], self.pltanswerkeep[1:self.ndat],
        #            'ro')  # predicted data red dots
        # s = 7
        # plt.loglog(self.adat[1:self.ndat], self.rdat[1:self.ndat], 'bo',
                #    markersize=s)  # original data blue dots

        # output the ranges cpmstraining the model

        print('   Small', '   Large')
        # for i in range(0, self.layer_index, 1):
        #     print("%9.3f %9.3f" % (self.small[i], self.xlarge[i]))
        for i in range(0, self.layer-1, 1):
            print("%9.3f %9.3f" % (self.thickness_minimum[i], self.thickness_maximum[i]))
        for i in range(0, self.layer, 1):
            print("%9.3f %9.3f" % (self.resistivity_minimum[i], self.resistivity_maximum[i]))

    # output the final rms
        print(' RMS_=   ', "%9.6f" % self.errmin)

        # output the best fitting earth model
        print('   Layer ', '   Thickness  ', 'Res_ohm-m  ')
        for i in range(0, self.layer-1, 1):
            print("%9.1f   %9.3f  %9.3f" % (i+1, self.pkeep[i], self.pkeep[self.layer+i-1]))

        print("%9.1f" % self.layer, '  Infinite ', "%9.3f" % self.pkeep[self.layer_index-1])

        # output the original data and the predicted data
        print('  Spacing', '  Original_Data', ' Predicted')
        for i in range(0, self.ndat, 1):
            print("%9.3f  %9.3f  %9.3f" % (self.adat[i], self.rdat[i], self.pltanswerkeep[i]))

    # def graph(self):
        # plt.show()
        # plt.grid(True)


# main here
if __name__ == '__main__':
    VI = VESinverse()
    VI.data_init()
    VI.computePredictions()
