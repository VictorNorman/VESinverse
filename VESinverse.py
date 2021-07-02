# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:32:48 2016

@authors:  James Clark, AJ Vrieland, Rebecca DiCosola, Victor Norman

this code uses the Ghosh method to determine the apparent resistivities
for a layered earth model. Either schlumberger or Wenner configurations
can be used

Copyright 2021 James Clarck

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""


import math
import random
import matplotlib.pyplot as plt
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

        # I can't seem to get rid of any ARRAYSIZE except on location_data and field_data
        # because the first time they are referenced it is within a loop and
        # thus append would not really work

        # 65 is completely arbitrary
        self.p = []                                  # model_thicknesses_resistivities
        self.r = [0]*ARRAYSIZE                       # Resistivity?
        self.rl = [0]*ARRAYSIZE                      # Resistivity?
        self.t = [0]*50
        self.b = [0]*ARRAYSIZE
        self.a_spacing = [0]*ARRAYSIZE              # a_spacing : asav
        self.a_spacing_log = [0]*ARRAYSIZE          # a_spacing_log : asavl
        self.location_data_log = [0]*ARRAYSIZE      # location_data_log : adatl
        self.field_data_log = [0]*ARRAYSIZE         # field_data_log : rdat
        self.location_data = []                     # Location_data : adat
        self.field_data = []                        # Field_data : rdat
        self.lowest_rms_values = []                 # Lowest_rms_values : pkeep
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
        self.data_amount = 12

        # number of iterations for the Monte Carlo guesses. to be input on GUI
        self.iter = 10000

        self.layer = 3

    def data_init(self):
        self.one30 = 1.e30
        self.rms = self.one30
        self.errmin = 1.e10

        # self.layer_index is used to offset now only lowest_rms_values for 
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

    def get_location_data(self):
        return self.location_data

    def set_location_data(self, gui_adat_array):
        self.location_data = gui_adat_array

    def get_field_data(self):
        return self.field_data

    def set_field_data(self, gui_rdat_array):
        self.field_data = gui_rdat_array

    def set_data_amount(self, new_ndat_number):
        self.data_amount = new_ndat_number

    def get_data_amount(self):
        return self.data_amount

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

    def get_lowest_rms_values(self):
        return self.lowest_rms_values

    def set_index(self, new_index):
        self.index = new_index

    def get_errmin(self):
        return self.errmin

    def get_layer_index(self):
        return self.layer_index
    
    def set_random(self, seed):
        print(seed)
        random.seed(seed)
    # ---------------------------------------------

    def readData(self):
        # normally this is where the data would be read from the csv file
        # but now I'm just hard coding it in as global lists
        for i in range(0, self.data_amount, 1):
            self.location_data_log[i] = math.log10(self.location_data[i])
            self.field_data_log[i] = math.log10(self.field_data[i])

    def error(self):
        self.pltanswer.clear()
        self.pltanswerl.clear()
        sumerror = 0.
        # pltanswer = [0]*64
        self.spline(self.resistivity_points_number, self.one30, self.one30,
                    self.a_spacing_log, self.rl, self.y2)
        for i in range(0, self.data_amount, 1):
            ans = self.splint(self.resistivity_points_number, self.location_data_log[i],
                              self.a_spacing_log, self.rl, self.y2)
            sumerror = sumerror + (self.field_data_log[i] - ans) * (self.field_data_log[i] - ans)
            # print(i,sum1,field_data[i],rdatl[i],ans)
            self.pltanswerl.append(ans)
            self.pltanswer.append(math.pow(10, ans))
        self.rms = math.sqrt(sumerror/(self.data_amount))

        return self.rms

    def transf(self, y, i):
        self.u = 1./math.exp(y)
        self.t[0] = self.p[self.layer_index-1]
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
        for i in range(0, self.resistivity_points_number, 1):
            a = math.exp(x)
            self.a_spacing[i] = a
            self.a_spacing_log[i] = math.log10(a)
            self.rl[i] = math.log10(self.r[i])
            x = x + self.delx

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

        for i in range(0, n-1):
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
        a = (xa[khi] - x) / h
        b = (x - xa[klo]) / h
        y = (a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2a[klo] +
                                          (b * b * b - b) * y2a[khi]) *
             (h * h) / 6.)

        return y

    def computePredictions(self):
        self.data_init()
        # Turn off randomization (for now)
        self.set_random(0)

        self.readData()
        print(self.location_data[0:self.data_amount], self.field_data[0:self.data_amount])
        for iloop in range(0, self.iter, 1):
            self.p.clear()
            for i in range(0, self.layer - 1):
                randNumber = random.random()
                self.p.append((self.thickness_maximum[i] - self.thickness_minimum[i])*randNumber + self.thickness_minimum[i])
            for i in range(0, self.layer):
                randNumber = random.random()
                self.p.append((self.resistivity_maximum[i] - self.resistivity_minimum[i])*randNumber + self.resistivity_minimum[i])

            self.rms = self.rmsfit()

            if self.rms < self.errmin:
                self.lowest_rms_values.clear()
                self.rkeep.clear()
                self.rkeepl.clear()
                self.pltanswerkeep.clear()
                self.pltanswerkeepl.clear()
                print('rms  ', self.rms, '   errmin ', self.errmin)
                for i in range(0, self.layer_index, 1):
                    self.lowest_rms_values.append(self.p[i])
                for i in range(0, self.resistivity_points_number, 1):
                    self.rkeep.append(self.r[i])
                    self.rkeepl.append(self.rl[i])
                for i in range(0, self.data_amount, 1):
                    self.pltanswerkeepl.append(self.pltanswerl[i])
                    self.pltanswerkeep.append(self.pltanswer[i])
                self.errmin = self.rms

    # output the best fitting earth model
        print(' Layer ', '     Thickness  ', '   Res_ohm-m  ')
        for i in range(0, self.layer - 1, 1):
            print(i, self.lowest_rms_values[i], self.lowest_rms_values[self.layer+i-1])

        print(self.layer, '  Infinite ', self.lowest_rms_values[self.layer_index-1])
        for i in range(0, self.resistivity_points_number, 1):
            self.a_spacing_log[i] = math.log10(self.a_spacing[i])

    # output the error of fit
        print(' RMS error   ', self.errmin)
        print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
        for i in range(0, self.resistivity_points_number, 1):
            # print(a_spacing[i], rkeep[i], asavl[i], rkeepl[i])
            print("%9.3f   %9.3f  %9.3f  %9.3f" % (self.a_spacing[i], self.rkeep[i],
                                                   self.a_spacing_log[i], self.rkeepl[i]))

        # output the ranges cpmstraining the model

        print('   Small', '   Large')
        for i in range(0, self.layer-1, 1):
            print("%9.3f %9.3f" % (self.thickness_minimum[i], self.thickness_maximum[i]))
        for i in range(0, self.layer, 1):
            print("%9.3f %9.3f" % (self.resistivity_minimum[i], self.resistivity_maximum[i]))

    # output the final rms
        print(' RMS_=   ', "%9.6f" % self.errmin)

        # output the best fitting earth model
        print('   Layer ', '   Thickness  ', 'Res_ohm-m  ')
        for i in range(0, self.layer-1, 1):
            print("%9.1f   %9.3f  %9.3f" % (i+1, self.lowest_rms_values[i], self.lowest_rms_values[self.layer+i-1]))

        print("%9.1f" % self.layer, '  Infinite ', "%9.3f" % self.lowest_rms_values[self.layer_index-1])

        # output the original data and the predicted data
        print('  Spacing', '  Original_Data', ' Predicted')
        for i in range(0, self.data_amount, 1):
            print("%9.3f  %9.3f  %9.3f" % (self.location_data[i], self.field_data[i], self.pltanswerkeep[i]))

    def graph(self):
        plt.loglog(self.a_spacing[1:self.resistivity_points_number], self.rkeep[1:self.resistivity_points_number], '-')  # resistivity prediction curve
        plt.loglog(self.location_data[1:self.data_amount], self.pltanswerkeep[1:self.data_amount],
                   'ro')  # predicted data red dots
        s = 7
        plt.loglog(self.location_data[1:self.data_amount], self.field_data[1:self.data_amount], 'bo',
                   markersize=s)  # original data blue dots
        plt.show()
        plt.grid(True)


# main here
if __name__ == '__main__':
    VI = VESinverse()
    VI.data_init()
    VI.computePredictions()
