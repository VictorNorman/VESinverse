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

# For Testing Purposes
# Only the Test suit should edit these Constants
LAYERS = 4
DATASET = 7
RANGE = 5
GRAPH = True

ARRAYSIZE = 65

# Schlumberger filter
fltr1 = [.00046256, -.0010907, .0017122, -.0020687,
         .0043048, -.0021236, .015995, .017065, .098105, .21918, .64722,
         1.1415, .47819, -3.515, 2.7743, -1.201, .4544, -.19427, .097364,
         -.054099, .031729, -.019109, .011656, -.0071544, .0044042,
         -.002715, .0016749, -.0010335, .00040124]

# Wenner Filter
fltr2 = [.000238935, .00011557, .00017034, .00024935,
         .00036665, .00053753, .0007896, .0011584, .0017008, .0024959,
         .003664, .0053773, .007893, .011583, .016998, .024934, .036558,
         .053507, .078121, .11319, .16192, .22363, .28821, .30276, .15523,
         -.32026, -.53557, .51787, -.196, .054394, -.015747, .0053941,
         -.0021446, .000665125]

# I know there must be a better method to assign lists. And probably numpy
# arrays would be best. But my Python wasn't up to it. If the last letter
# is an 'l' that means it is a log10 of the value

# 65 is completely arbitrary
p = [0]*20              
r = [0]*ARRAYSIZE
rl = [0]*ARRAYSIZE
t = [0]*50
b = [0]*ARRAYSIZE
asav = [0]*ARRAYSIZE
asavl = [0]*ARRAYSIZE
adatl = [0]*ARRAYSIZE
rdatl = [0]*ARRAYSIZE
adat = [0]*ARRAYSIZE
rdat = [0]*ARRAYSIZE
pkeep = [0]*ARRAYSIZE
rkeep = [0]*ARRAYSIZE
rkeepl = [0]*ARRAYSIZE
pltanswer = [0]*ARRAYSIZE
pltanswerl = [0]*ARRAYSIZE
pltanswerkeep = [0]*ARRAYSIZE
pltanswerkeepl = [0]*ARRAYSIZE

rl = [0]*ARRAYSIZE
small = [0]*ARRAYSIZE
xlarge = [0]*ARRAYSIZE

x = [0]*100
y = [0]*100
y2 = [0]*100
u = [0]*5000
new_x = [0]*1000
new_y = [0]*1000
ndat = 12
# hard coded data input - spacing and apparent resistivities measured
# in teh field


def data_init():

    global adat
    global rdat
    global one30
    global rms
    global errmin
    global index
    global layer
    global layer_index
    global electrode_spacing
    global resistivity_points_number
    global delx
    global ep
    global fctr
    global small
    global xlarge
    global iter

    adat = [0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30., 70.]

    if DATASET == 1:
        rdat = [125., 110., 95., 40., 24., 15.,
                10.5, 8., 6., 6.5, 11., 25.]  # DATA 1
    elif DATASET == 2:
        rdat = [125., 130., 140., 150., 160.,
                170., 175., 170., 130., 100., 80., 60.]  # DATA 2
    elif DATASET == 3:
        rdat = [125., 124., 120., 115., 110.,
                95., 40., 24., 15., 10., 11., 25.]  # DATA 3
    elif DATASET == 4:
        rdat = [ 125., 124., 126., 129., 135.,
                140., 150., 170., 175., 180., 185., 187.]  # DATA 4
    elif DATASET == 5:
        rdat = [ 125., 124., 126., 122., 120.,
                110., 85., 65., 40., 30., 26., 25.]  # DATA 5
    elif DATASET == 6:
        rdat = [ 125., 124., 126., 129., 135.,
                180., 220., 250., 280., 300., 310., 315.]  # DATA 6
    elif DATASET == 7:
        rdat = [300., 303., 330., 330., 310.,
                300., 285., 240., 205., 180., 180., 210.]  # DATA 7
    elif DATASET == 8:
        rdat = [300., 298., 290., 270., 280.,
                300., 330., 370., 420., 510., 507., 370.]  # DATA 8
    one30 = 1.e30
    rms = one30
    errmin = 1.e10

    # INPUT
    index = 2   # 1 is for shchlumberger and 2 is for Wenner

    if LAYERS == 3:
        layer = 3
    elif LAYERS == 2:
        layer = 2
    elif LAYERS == 4:
        layer = 4

    layer_index = 2 * layer - 1    # layer (e) and layer_index (n) variables have been updated


    electrode_spacing = 0.2  # smallest electrode spacing
    resistivity_points_number = 20  # number of points where resistivity is calculated (Variable was m)

    electrode_spacing = np.log(electrode_spacing)
    delx = np.log(10.0)/6.

    # these lines apparently find the computer precision ep
    ep = 1.0
    ep = ep/2.0
    fctr = ep+1.
    while fctr > 1.:
        ep = ep/2.0
        fctr = ep+1.

    # this is where the range in parameters should be input from a GUI
    # I'm hard coding this in for now

    # enter thickenss range for each layer and then resistivity range.
    # for 3 layers small[0] and small[1] are low end of thickness range
    # small[2], small[3] and small[4] are the low end of resistivities
    if RANGE == 1:
        # range 1  3-layer case (narrow range)
        small[0] = 1.
        xlarge[0] = 5
        small[1] = 10.
        xlarge[1] = 75.
        small[2] = 20.
        xlarge[2] = 200.
        small[3] = 2.
        xlarge[3] = 100
        small[4] = 500.
        xlarge[4] = 3000.
    elif RANGE == 2:
        # range 2 3-layer case (broad range)
        small[0] = 1.
        xlarge[0] = 10
        small[1] = 1.
        xlarge[1] = 50.
        small[2] = 1.
        xlarge[2] = 500.
        small[3] = 1.
        xlarge[3] = 500.
        small[4] = 1.
        xlarge[4] = 500.
    elif RANGE == 3:
        # range 3  2-layer case (broad range)
        small[0] = 1.
        xlarge[0] = 20
        small[1] = 1.
        xlarge[1] = 500.
        small[2] = 1.
        xlarge[2] = 500
    elif RANGE == 4:
        # range 4  2-layer case (small range)
        small[0] = 1.
        xlarge[0] = 10
        small[1] = 50.
        xlarge[1] = 200.
        small[2] = 1.
        xlarge[2] = 50.
    elif RANGE == 5:
        # range 5 4-layer case (small range)
        small[0] = 1.
        xlarge[0] = 2
        small[1] = 1.
        xlarge[1] = 50.
        small[2] = 1.
        xlarge[2] = 50.
        small[3] = 200.
        xlarge[3] = 400.
        small[4] = 400.
        xlarge[4] = 500.
        small[5] = 1.
        xlarge[5] = 500.
        small[6] = 1.
        xlarge[6] = 500.
    elif RANGE == 6:
        # range 6 4-layer case (broad range)
        small[0] = 1
        xlarge[0] = 2
        small[1] = 1.
        xlarge[1] = 2.
        small[2] = 1.
        xlarge[2] = 50.
        small[3] = 1.
        xlarge[3] = 500.
        small[4] = 1.
        xlarge[4] = 500.
        small[5] = 1.
        xlarge[5] = 500.
        small[6] = 1.
        xlarge[6] = 500.
    elif RANGE == 7:
        # range 7 4-layer case (broadest range)
        small[0] = 1
        xlarge[0] = 50
        small[1] = 1.
        xlarge[1] = 50.
        small[2] = 1.
        xlarge[2] = 50.
        small[3] = 1.
        xlarge[3] = 500.
        small[4] = 1.
        xlarge[4] = 500.
        small[5] = 1.
        xlarge[5] = 500.
        small[6] = 1.
        xlarge[6] = 500.

    iter = 10000  # number of iterations for the Monte Carlo guesses. to be input on GUI


def readData():
    # normally this is where the data would be read from the csv file
    # but now I'm just hard coding it in as global lists

    for i in range(0, ndat, 1):
        adatl[i] = np.log10(adat[i])
        rdatl[i] = np.log10(rdat[i])
    return


def error():
    sumerror = 0.
    # pltanswer = [0]*64
    spline(resistivity_points_number, one30, one30, asavl, rl, y2)
    for i in range(0, ndat, 1):
        ans = splint(resistivity_points_number, adatl[i], asavl, rl, y2)
        sumerror = sumerror + (rdatl[i] - ans) * (rdatl[i] - ans)
        # print(i,sum1,rdat[i],rdatl[i],ans)
        pltanswerl[i] = ans
        pltanswer[i] = np.power(10, ans)
    rms = np.sqrt(sumerror/(ndat-1))

    # check the spline routine
    # for i in range(0,m+1,1):
    #     anstest = splint(m, asavl[i],asavl,rl,y2)
    #     print( asavl[i], rl[i], anstest)
    # print(' rms  =  ', rms)
# if you erally want to get a good idea of all perdictions from Montecarlo
# perform the following plot (caution - change iter to a smaller number)
    # plt.loglog(adat[0:ndat],pltanswer[0:ndat])
    return rms


def transf(y, i): 
    u = 1./np.exp(y)
    t[0] = p[layer_index-1]
    for j in range(0, layer, 1):
        pwr = -2. * u * p[layer - j -1]
        if pwr < np.log(2. * ep):
            pwr = np.log(2. * ep)
        a = np.exp(pwr)
        b = (1. - a)/(1. + a)
        rs = p[layer_index - j -1]
        tpr = b*rs
        t[j] = (tpr + t[j - 1]) / (1. + tpr * t[j - 1] / (rs * rs))
    r[i] = t[layer-1]
    return


def filters(fltr, k):                                  # This b is a local Variable not the same as the other b's
    for i in range(0, resistivity_points_number, 1):
        re = 0.
        for j in range(0, k, 1):
            re = re + fltr[j] * r[i + k - j]
        r[i] = re
    return


def rmsfit():
    if index == 1:
        y = electrode_spacing -19. * delx - 0.13069
        mum1 = resistivity_points_number + 28
        for i in range(0, mum1, 1):
            transf(y, i)
            y = y + delx
        filters(fltr1, 29)
    elif index == 2:
        s = np.log(2.)
        y = electrode_spacing -10.8792495 * delx
        mum2 = resistivity_points_number + 33
        for i in range(0, mum2, 1):
            transf(y, i)
            a = r[i]
            y1 = y + s
            transf(y1, i)
            r[i] = 2. * a - r[i]
            y = y + delx
        filters(fltr2, 34)

    else:
        print(" type of survey not indicated")
        sys.exit()

    x = electrode_spacing
    # print("A-Spacing   App. Resistivity")
    for i in range(0, resistivity_points_number, 1):
        a = np.exp(x)
        asav[i] = a
        asavl[i] = np.log10(a)
        if r[i] <= 0:
            print(r[i], '\n', i, '\n', p, '\n', t)
            raise Exception("only positive number above 0")
        rl[i] = np.log10(r[i])                              # Line in question, encountered invalid value --- why? --- there are negitave numbers somewhere in r
        x = x + delx
        # print("%7.2f   %9.3f " % ( asav[i], r[i]))

    rms = error()

    return rms

# my code to do a spline fit to predicted data at the nice spacing of Ghosh
# use splint to determine the spline interpolated prediction at the
# spacing where the measured resistivity was taken - to compare observation
# to prediction


def spline(n, yp1, ypn, x=[], y=[], y2=[]):
    u = [0] * 1000
    one29 = 0.99e30
    # print(x,y)
    if yp1 > one29:
        y2[0] = 0.
        u[0] = 0.
    else:
        y2[0] = -0.5
        u[0] = (3. / (x[0] - x[0])) * ((y[0] - y[0]) / (x[0] - x[0]) - yp1)

    for i in range(0, n):
        # print(i,x[i])
        sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
        notp = sig * y2[i - 1] + 2.
        y2[i] = (sig - 1.) / notp
        u[i] = ((6. * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) - (y[i] - y[i - 1]) /
                     (x[i] - x[i - 1])) / (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / notp)

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


def splint(n, x, xa=[], ya=[], y2a=[]):
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


def computePredictions():

    # TODO: This should be GONE by the end of Summer
    global iter
    global num_iter
    global num_layers
    global num_layers_var
    global layer_index
    global thick_min_layer
    global thick_max_layer
    global res_min_layer
    global res_max_layer
    global adat
    global rdat
    global ndat
    global rms
    global errmin
    global pkeep
    global resistivity_points_number
    global asav
    global asavl
    global rkeep
    global rkeepl
    global pltanswerkeep

    # Turn off randomization (for now)
    random.seed(0)

    readData()
    print(adat[0:ndat], rdat[0:ndat])
    for iloop in range(0, iter, 1):
        # print( '  iloop is ', iloop)
        for i in range(0, layer_index, 1):
            randNumber = random.random()
            # print(randNumber, '  random')
            p[i] = (xlarge[i] - small[i])*randNumber + small[i]

        rms = rmsfit()

        if rms < errmin:
            print('rms  ', rms, '   errmin ', errmin)
            for i in range(0, layer_index, 1):
                pkeep[i] = p[i]
            for i in range(0, resistivity_points_number, 1):
                rkeep[i] = r[i]
                rkeepl[i] = rl[i]
            for i in range(0, ndat+1, 1):
                pltanswerkeepl[i] = pltanswerl[i]
                pltanswerkeep[i] = pltanswer[i]
            errmin = rms

# output the best fitting earth model
    print(' Layer ', '     Thickness  ', '   Res_ohm-m  ')
    for i in range(0, layer, 1):
        print(i, pkeep[i], pkeep[layer+i-1])

    print(layer, '  Infinite ', pkeep[layer_index])
    for i in range(0, resistivity_points_number, 1):
        asavl[i] = np.log10(asav[i])

# output the error of fit
    print(' RMS error   ', errmin)
    print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
    for i in range(0, resistivity_points_number, 1):
        # print(asav[i], rkeep[i], asavl[i], rkeepl[i])
        print("%9.3f   %9.3f  %9.3f  %9.3f" % (asav[i], rkeep[i],
                                               asavl[i], rkeepl[i]))

    plt.loglog(asav[0:resistivity_points_number], rkeep[0:resistivity_points_number], '-')  # resistivity prediction curve
    plt.loglog(adat[0:ndat], pltanswerkeep[0:ndat],
               'ro')  # predicted data red dots
    s = 7
    plt.loglog(adat[0:ndat], rdat[0:ndat], 'bo',
               markersize=s)  # original data blue dots

    # output the ranges cpmstraining the model

    print('   Small', '   Large')
    for i in range(0, layer_index, 1):
        print("%9.3f %9.3f" % (small[i], xlarge[i]))

# output the final rms
    print(' RMS_=   ', "%9.6f" % errmin)

    # output the best fitting earth model
    print('   Layer ', '   Thickness  ', 'Res_ohm-m  ')
    for i in range(0, layer, 1):
        print("%9.1f   %9.3f  %9.3f" % (i, pkeep[i], pkeep[layer+i-1]))

    print("%9.1f" % layer, '  Infinite ', "%9.3f" % pkeep[layer_index])

    # output the original data and the predicted data
    print('  Spacing', '  Original_Data', ' Predicted')
    for i in range(0, ndat, 1):
        print("%9.3f  %9.3f  %9.3f" % (adat[i], rdat[i], pltanswerkeep[i]))
    if GRAPH is True:
        plt.show()
        plt.grid(True)
        sys.exit(0)


# main here
if __name__ == '__main__':
    data_init()
    computePredictions()
