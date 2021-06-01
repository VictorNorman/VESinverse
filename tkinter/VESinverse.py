# -*- coding: utf-8 -*-

#
# Created on Thu Jan 28 16:32:48 2016
# @author: jclark

# This code uses the Ghosh method to determine the apparent resistivities
# for a layered earth model. Either schlumberger or Wenner configurations
# can be used

# GUI Implementation Additions
# Created Winter 2021
# @author: Rebecca DiCosola
# @author: Victor Norman


import numpy as np
import random
import matplotlib.pyplot as plt
import sys
from tkinter import *
from tkinter import filedialog


# ------------------ CONSTANTS -----------------------------

# For rounding values when displaying them
NDIGITS = 6

# Schlumberger Filter
FLTR1 = [0., .00046256, -.0010907, .0017122, -.0020687,
         .0043048, -.0021236, .015995, .017065, .098105, .21918, .64722,
         1.1415, .47819, -3.515, 2.7743, -1.201, .4544, -.19427, .097364,
         -.054099, .031729, -.019109, .011656, -.0071544, .0044042,
         -.002715, .0016749, -.0010335, .00040124]

# Wenner Filter
FLTR2 = [0., .000238935, .00011557, .00017034, .00024935,
         .00036665, .00053753, .0007896, .0011584, .0017008, .0024959,
         .003664, .0053773, .007893, .011583, .016998, .024934, .036558,
         .053507, .078121, .11319, .16192, .22363, .28821, .30276, .15523,
         -.32026, -.53557, .51787, -.196, .054394, -.015747, .0053941,
         -.0021446, .000665125]

MAX_LAYERS = 5

# Array size
# 65 is completely arbitrary
ARRAYSIZE = 65

SCHLUMBERGER = 1
WENNER = 2


ONE_E30 = 1.e30
ONE29 = 0.99e30
DELX = np.log(10.0) / 6.

# I know there must be a better method to assign lists. And probably numpy
# arrays would be best. But my Python wasn't up to it. If the last letter
# is an 'l' that means it is a log10 of the value
p = [0] * 20
r = [0] * ARRAYSIZE
rl = [0] * ARRAYSIZE
t = [0] * 50
b = [0] * ARRAYSIZE
asav = [0] * ARRAYSIZE
asavl = [0] * ARRAYSIZE
adatl = [0] * ARRAYSIZE
rdatl = [0] * ARRAYSIZE
adat = [0] * ARRAYSIZE
rdat = [0] * ARRAYSIZE
pkeep = [0] * ARRAYSIZE
rkeep = [0] * ARRAYSIZE
rkeepl = [0] * ARRAYSIZE
pltanswer = [0] * ARRAYSIZE
pltanswerl = [0] * ARRAYSIZE
pltanswerkeep = [0] * ARRAYSIZE
pltanswerkeepl = [0] * ARRAYSIZE

x = [0] * 100
y = [0] * 100
y2 = [0] * 100
u = [0] * 5000

# this variable is never used
# new_x = [0] * 1000
# this variable is never used
# new_y = [0] * 1000

# Input
algorithm_choice = 1
num_layers = 0  # number of layers
n = 2 * num_layers - 1
iter = 10000  # number of iterations for the Monte Carlo guesses. to be input on GUI

# this is where the range in parameters should be input from a GUI
# I'm hard coding this in for now

# enter thickenss range for each layer and then resistivity range.
# for 3 layers small[1] and small[2] are low end of thickness range
# small[3], small[4] and small[5] are the low end of resistivities

# small[1] = 1.
# xlarge[1] = 5
# small[2] = 10.
# xlarge[2] = 75.
# small[3] = 20.
# xlarge[3] = 200.
# small[4] = 2.
# xlarge[4] = 100.
# small[5] = 500.
# xlarge[5] = 3000.
# 1 10 5 75 20 2 500 200 100 3000

# hard coded data input - spacing and apparent resistivities measured
# in the field
ndat = 13
# adat = [0., 0.55, 0.95, 1.5, 2.5, 3., 4.5, 5.5, 9., 12., 20., 30., 70.]
# rdat = [0., 125., 110., 95., 40., 24., 15., 10.5, 8., 6., 6.5, 11., 25.]
rms = ONE_E30
errmin = 1.e10

spac = 0.2  # smallest electrode spacing
m = 20  # number of points where resistivity is calculated

spac = np.log(spac)

# these lines apparently find the computer precision ep
ep = 1.0
ep = ep / 2.0
fctr = ep + 1.
while fctr > 1.:
    ep = ep / 2.0
    fctr = ep + 1.


# ------------------- Function definitions --------------------------

def error():
    sumerror = 0.
    # pltanswer = [0] * 64
    spline(m, ONE_E30, ONE_E30, asavl, rl, y2)
    for i in range(1, ndat):
        ans = splint(m, adatl[i], asavl, rl, y2)
        sumerror = sumerror + (rdatl[i] - ans) * (rdatl[i] - ans)
        # print(i, sum1, rdat[i], rdatl[i], ans)
        pltanswerl[i] = ans
        pltanswer[i] = np.power(10, ans)
    rms = np.sqrt(sumerror / (ndat-1))

    # check the spline routine
#    for i in range(1, m+1):
#        anstest = splint(m, asavl[i], asavl, rl, y2)
#        print( asavl[i], rl[i], anstest)
    # print(' rms  =  ', rms)
# if you erally want to get a good idea of all perdictions from Montecarlo
# perform the following plot (caution - change iter to a smaller number)
    # plt.loglog(adat[1:ndat], pltanswer[1:ndat])

    return rms


def transf(y, i):
    u = 1. / np.exp(y)
    t[1] = p[n]
    for j in range(2, num_layers+1):
        pwr = -2. * u * p[num_layers+1-j]
        if pwr < np.log(2. * ep):
            pwr = np.log(2. * ep)
        a = np.exp(pwr)
        b = (1. - a)/(1. + a)
        rs = p[n + 1 - j]
        tpr = b * rs
        t[j] = (tpr + t[j-1]) / (1. + tpr * t[j-1] / (rs * rs))
    r[i] = t[num_layers]


def filters(b, k):
    for i in range(1, m+1):
        re = 0.
        for j in range(1, k+1):
            re = re + b[j] * r[i + k - j]
        r[i] = re


def rmsfit():
    if algorithm_choice == SCHLUMBERGER:
        y = spac - 19. * DELX - 0.13069
        mum1 = m + 28
        for i in range(1, mum1 + 1):
            transf(y, i)
            y = y + DELX
        filters(FLTR1, 29)
    elif algorithm_choice == WENNER:
        s = np.log(2.)
        y = spac-10.8792495 * DELX
        mum2 = m + 33
        for i in range(1, mum2 + 1):
            transf(y, i)
            a = r[i]
            y1 = y + s
            transf(y1, i)
            r[i] = 2. * a - r[i]
            y = y + DELX
        filters(FLTR2, 34)
    else:
        print("type of survey not indicated")
        sys.exit(-1)

    x = spac
    # print("A-Spacing   App. Resistivity")
    for i in range(1, m+1):
        a = np.exp(x)
        asav[i] = a
        asavl[i] = np.log10(a)
        rl[i] = np.log10(r[i])
        x = x + DELX
        # print("%7.2f   %9.3f " % ( asav[i], r[i]))
    rms = error()
    return rms


def spline(n, yp1, ypn, x=[], y=[], y2=[]):
    '''my code to do a spline fit to predicted data at the nice spacing of Ghosh
    use splint to determine the spline interpolated prediction at the
    spacing where the measured resistivity was taken - to compare observation
    to prediction'''

    u = [0] * 1000
    # print(x, y)
    if yp1 > ONE29:
        y2[0] = 0.
        u[0] = 0.
    else:
        y2[0] = -0.5
        u[0] = (3. / (x[1] - x[0])) * ((y[1] - y[0]) /
                                       (x[1] - x[0]) - yp1)

    for i in range(1, n):
        # print(i, x[i])
        sig = (x[i] - x[i - 1]) / (x[i + 1] - x[i - 1])
        p = sig * y2[i - 1] + 2.
        y2[i] = (sig - 1.) / p
        u[i] = ((6. * ((y[i + 1] - y[i]) / (x[i + 1] - x[i]) -
                       (y[i] - y[i - 1]) / (x[i] - x[i - 1])) /
                 (x[i + 1] - x[i - 1]) - sig * u[i - 1]) / p)

    if ypn > ONE29:
        qn = 0.
        un = 0.
    else:
        qn = 0.5
        un = (3. / (x[n] - x[n - 1])) * \
            (ypn - (y[n] - y[n-1]) / (x[n] - x[n - 1]))

    y2[n] = (un - qn * u[n - 1]) / (qn * y2[n - 1] + 1.)
    for k in range(n - 1, -1, -1):
        y2[k] = y2[k] * y2[k + 1] + u[k]


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
    # print(x, xa[khi], xa[klo])
    a = (xa[khi] - x) / h
    b = (x - xa[klo]) / h
    y = (a * ya[klo] + b * ya[khi] + ((a * a * a - a) * y2a[klo] +
                                      (b * b * b - b) * y2a[khi]) * (h * h) / 6.)
    # print("x=   ", x,"y=  ", y, "  ya=  ", ya[khi],"  y2a=  ", y2a[khi], "  h=  ",h)
    return y


def openGUI():
    global algorithm_choice
    global num_layers
    global n
    global iter
    global file_explore
    global file_view
    global algorithm_index
    global thick_min_layer, thick_min_entries
    global thick_max_layer, thick_max_entries
    global res_min_layer, res_min_entries
    global res_max_layer, res_max_entries
    global layerinputframe

    global computed_results_labels

    computed_results_labels = []

    # file explore button
    preframe = Frame(mainwindow, background="gainsboro")
    preframe.pack(side=TOP, anchor=NW)
    selected_file = Label(preframe, bg="gainsboro", text="Selected File Path")
    selected_file.grid(row=1, column=2)
    file_view = Label(preframe, bg="gainsboro", text="No file",
                      width=40, wraplength=220, justify="center")
    file_view.grid(row=2, column=2)
    file_explore = Button(preframe, text="Select Resistivity Data File",
                          command=pickFile)
    file_explore.grid(row=1, column=1, rowspan=2)

    # drop down menu to pick number of layers
    dropdown_label = Label(preframe, bg="gainsboro",
                           text="Number of Layers", width=20)
    dropdown_label.grid(row=1, column=3)

    layerlist = list(range(1, MAX_LAYERS + 1))
    layersmenu = OptionMenu(preframe, num_layers_var, *layerlist)
    layersmenu.config(bg="gainsboro")
    layersmenu.grid(row=2, column=3)

    # https://www.delftstack.com/howto/python-tkinter/how-to-create-dropdown-menu-in-tkinter/
    # This is how we can detect if the menu selection has changed.
    num_layers_var.trace("w", numLayersChanged)

    # box to enter number of iterations
    iter_label = Label(preframe, bg="gainsboro",
                       text="Number of Iterations", width=20)
    iter_label.grid(row=1, column=4)
    iterentry = Entry(preframe, textvariable=num_iter, width=10)
    iterentry.grid(row=2, column=4, pady=5)

    # set number of layers
    num_layers = num_layers_var.get()

    # initialize arrays of IntVars for Entry boxes
    thick_min_layer = []  # [0] * (num_layers - 1)
    thick_max_layer = []  # [0] * (num_layers - 1)
    res_min_layer = []    # [0] * num_layers
    res_max_layer = []    # [0] * num_layers

    # ------------- Area showing layer input entry boxes and computed output -------------

    # store num_layers in a global variable so that when it is changed
    # we can see the old value.  We will create input and output boxes for
    # all MAX_LAYERS layers, but only display the ones for num_layers. When the value
    # changes we'll display or hide boxes.
    global curr_num_layers
    curr_num_layers = num_layers

    layerinputframe = Frame(mainwindow, background="gainsboro")
    layerinputframe.pack(side=TOP, anchor=SW)

    # thickness and resistivity labels
    Label(layerinputframe, bg="gainsboro", font=("TkDefaultFont", 13),
          text="Model Range in Thickness (m)").grid(row=1, column=1, columnspan=3, pady=5)
    Label(layerinputframe, bg="gainsboro", font=("TkDefaultFont", 13),
          text="Model Range in Resistivity (m)").grid(row=1, column=5, columnspan=3, pady=5)

    # thickness minimum values
    Label(layerinputframe, bg="gainsboro",
          text="Minimum\nValue", width=15).grid(row=2, column=1)

    thick_min_entries = []
    # - 1 here because bottom layer has Infinite thickness
    for i in range(MAX_LAYERS - 1):
        thick_min_layer.append(IntVar(mainwindow))
        thick_min_entries.append(Entry(
            layerinputframe, textvariable=thick_min_layer[i], width=10))

    # Add "Infinite" label to bottom of left column.
    # We store it in the thick_min_entries list so that when the number of
    # layers changes, we can remap it.  BUT IT IS NOT AN ENTRY!
    infinite_thickness_label = Label(layerinputframe, bg="gainsboro",
                                     text="Infinite Thickness")
    infinite_thickness_label.grid(row=num_layers+2, column=1, columnspan=2)
    thick_min_entries.append(infinite_thickness_label)

    # thickness maximum values
    Label(layerinputframe, bg="gainsboro",
          text="Maximum\nValue", width=15).grid(row=2, column=2)

    thick_max_entries = []
    for i in range(MAX_LAYERS - 1):
        thick_max_layer.append(IntVar(mainwindow))
        thick_max_entries.append(Entry(
            layerinputframe, textvariable=thick_max_layer[i], width=10))

    # thickness and resistivity prediction labels
    Label(layerinputframe, bg="gainsboro",
          text="Thickness\nPrediction", width=15).grid(row=2, column=3)
    Label(layerinputframe, bg="gainsboro",
          text="Resistivity\nPrediction", width=15).grid(row=2, column=4)

    # resistivity minimum values
    Label(layerinputframe, bg="gainsboro",
          text="Minimum\nValue", width=15).grid(row=2, column=6)

    res_min_entries = []
    for i in range(MAX_LAYERS):
        res_min_layer.append(IntVar(mainwindow))
        res_min_entries.append(Entry(
            layerinputframe, textvariable=res_min_layer[i], width=10))

    # resistivity maximum values
    Label(layerinputframe, bg="gainsboro",
          text="Maximum\nValue", width=15).grid(row=2, column=7)

    res_max_entries = []
    for i in range(MAX_LAYERS):
        res_max_layer.append(IntVar(mainwindow))
        res_max_entries.append(Entry(
            layerinputframe, textvariable=res_max_layer[i], width=10))

    displayChosenLayers(0, num_layers)

    # note while testing
    Label(layerinputframe, bg="gainsboro", font=("TkDefaultFont", 7),
          text="  --> For predictable results, enter 1 10 5 75 20 2 500 200 100 3000").grid(row=8, column=1, columnspan=3, pady=5)

    # ------------------ Buttons at the bottom ----------------------

    executionframe = Frame(mainwindow, background="gainsboro")
    executionframe.pack(side=BOTTOM, anchor=SW)
    execute_VES = Button(executionframe, text="Compute Predictions",
                         command=computePredictions)
    execute_VES.grid(row=1, column=1, padx=10, pady=5)

    # plot curves button
    plot_curves = Button(executionframe, text="Plot the Curves",
                         command=plotCurves)
    plot_curves.grid(row=1, column=2, padx=10, pady=5)


def displayChosenLayers(old_num_layers, curr_num_layers):
    assert old_num_layers != curr_num_layers

    if old_num_layers < curr_num_layers:

        # 0 for old_num_layers means we were not showing any layers before
        # (the initial state). But, we have to interate from 0, so we
        # change it to 1, so that in the loop, it is decremented to 0.
        if old_num_layers == 0:
            old_num_layers = 1

        # More layers to be shown now.
        # Show the entry boxes if the user has selected to see those layers
        # subtract 1 from old_num_layers because indices start at 0
        for i in range(old_num_layers - 1, curr_num_layers - 1):
            thick_min_entries[i].grid(row=i+3, column=1)
            thick_max_entries[i].grid(row=i+3, column=2)
        for i in range(old_num_layers - 1, curr_num_layers):
            res_min_entries[i].grid(row=i+3, column=6)
            res_max_entries[i].grid(row=i+3, column=7)

    else:
        # fewer layers to be shown now: use grid_forget() to un-display them
        for i in range(old_num_layers - 2, curr_num_layers - 2, -1):
            thick_min_entries[i].grid_forget()
            thick_max_entries[i].grid_forget()
        for i in range(old_num_layers - 1, curr_num_layers - 1, -1):
            res_min_entries[i].grid_forget()
            res_max_entries[i].grid_forget()

    # Move the "Infinite Thickness" label
    inf_thickness_label = thick_min_entries[MAX_LAYERS - 1]
    inf_thickness_label.grid(row=curr_num_layers+2, column=1, columnspan=2)


def numLayersChanged(*args):
    global curr_num_layers
    global computed_results_labels

    # Clear displayed results
    if computed_results_labels != []:
        for l in computed_results_labels:
            l.grid_forget()
    computed_results_labels = []

    new_num_layers = num_layers_var.get()
    if new_num_layers != curr_num_layers:
        print(f"num_layers changed from {curr_num_layers} to {new_num_layers}")
        displayChosenLayers(curr_num_layers, new_num_layers)
    # Store new value as current value
    curr_num_layers = new_num_layers


def pickFile():
    global file_view
    global algorithm_choice

    global adat
    global rdat
    global ndat

    # get file
    resistivity_file = filedialog.askopenfilename(initialdir="/",
                                                  title="Open File",
                                                  filetypes=(("Text Files", "*.txt"),
                                                             ("All Files", "*.*")))

    # set label by file button to resistivity file link
    file_view.config(text=resistivity_file)

    # open the file and read entire file into file_list.
    file_handle = open(resistivity_file, "r")
    file_list = file_handle.readlines()

    # when printing, skip first 2 lines: data starts in line 3.
    for i in range(2, len(file_list)):
        print(file_list[i])

    # algorithm to use is on line 1 (second line).
    if int(file_list[1].strip()) == SCHLUMBERGER:
        algorithm_choice = SCHLUMBERGER
    elif int(file_list[1].strip()) == WENNER:
        algorithm_choice = WENNER
    else:
        print('Algorithm choice on line 2 must be 1 or 2', file=sys.stderr)
        sys.exit(-1)

    # for each data line
    for i in range(2, len(file_list)):
        fields = file_list[i].split()
        spacing_val = float(fields[0].strip())
        # print('-->' + spacing_val + '<--')
        resis_val = float(fields[1].strip())
        # print('-->' + resis_val + '<--')
        # indexes in these array start at 0, so subtract 2

        # TODO: better name for adat or spacing_val?: what are these values?
        adat[i-2] = spacing_val
        rdat[i-2] = resis_val

    # number of data values
    ndat = len(file_list) - 2

    # TODO: do we handle files with the ending line of 0 0 ? Should we?

    # compute log10 values of adat and rdat
    # TODO: the values in adatl and rdatl are indexed starting a 1: yuck!
    # TODO: we don't convert adat[0] or rdat[0]... correct?
    for i in range(1, ndat):
        adatl[i] = np.log10(adat[i])
        rdatl[i] = np.log10(rdat[i])

# not used anymore. from the original code.
# def readData():
#     # normally this is where the data would be read from the csv file
#     # but now I'm just hard coding it in as global lists
#     for i in range(1, ndat):
#         adatl[i] = np.log10(adat[i])
#         print(adatl[i])
#         rdatl[i] = np.log10(rdat[i])
#         print(rdatl[i])
#     return


def computePredictions():
    '''compute predictions'''

    # will cut down global variables in future
    global iter
    global num_iter
    global num_layers
    global num_layers_var
    global n
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
    global m
    global asav
    global asavl
    global rkeep
    global rkeepl
    global pltanswerkeep

    # TODO: + 1 here because we are using 1-based arrays.
    small = [0] * (MAX_LAYERS + 1)
    xlarge = [0] * (MAX_LAYERS + 1)

# Turn off randomization
    random.seed(0)

    # set number of iterations
    iter = num_iter.get()

    # get number of layers
    num_layers = num_layers_var.get()
    n = 2 * num_layers - 1

    # set small[] and xlarge[]
    for i in range(num_layers - 1):
        small[i + 1] = thick_min_layer[i].get()
    for i in range(num_layers - 1):
        xlarge[i + 1] = thick_max_layer[i].get()
    for i in range(num_layers):
        small[i + num_layers] = res_min_layer[i].get()
    for i in range(num_layers):
        xlarge[i + num_layers] = res_max_layer[i].get()

    print('computePredictions: small = ', small)
    print('                    xlarge = ', xlarge)

    print('adat: ', adat)
    print('rdat: ', rdat)
    for iloop in range(1, iter + 1):
        # print( '  iloop is ', iloop)
        for i in range(1, num_layers + 1):
            randNumber = random.random()
            # print(randNumber, '  random')
            p[i] = (xlarge[i] - small[i]) * randNumber + small[i]
        for i in range(num_layers + 1, n + 1):
            randNumber = random.random()
            # print(randNumber, '  random')
            p[i] = (xlarge[i] - small[i]) * randNumber + small[i]

        rms = rmsfit()

        if rms < errmin:
            print('rms  ', rms, '   errmin ', errmin)
            for i in range(1, n+1):
                pkeep[i] = p[i]
            for i in range(1, m+1):
                rkeep[i] = r[i]
                rkeepl[i] = rl[i]
            for i in range(1, ndat + 1):
                pltanswerkeepl[i] = pltanswerl[i]
                pltanswerkeep[i] = pltanswer[i]
            errmin = rms

    # output the best fitting earth model
    print(' Layer ', '     Thickness  ', '   Res_ohm-m  ')
    for i in range(1, num_layers):
        print(i, pkeep[i], pkeep[num_layers + i - 1])
    print(num_layers, '  Infinite ', pkeep[n])

    for i in range(1, m + 1):
        asavl[i] = np.log10(asav[i])

    # output the error of fit
    print(' RMS error   ', errmin)
    print('  Spacing', '  Res_pred  ', ' Log10_spacing  ', ' Log10_Res_pred ')
    for i in range(1, m + 1):
        # print(asav[i], rkeep[i], asavl[i], rkeepl[i])
        print("%7.2f   %9.3f  %9.3f  %9.3f" % (asav[i], rkeep[i],
                                               asavl[i], rkeepl[i]))

    plt.loglog(asav[1:m], rkeep[1:m], '-')  # resistivity prediction curve
    plt.loglog(adat[1:ndat], pltanswerkeep[1:ndat],
               'ro')  # predicted data red dots
    s = 7
    plt.loglog(adat[1:ndat], rdat[1:ndat], 'bo',
               markersize=s)  # original data blue dots

    viewModel()


def viewModel():
    '''Put computed values into the gui, in the middle columns'''
    global layerinputframe
    global pkeep
    global num_layers
    global n			# 2 * num_layers - 1
    global computed_results_labels

    # we've displayed labels before, so remove them now from the display
    # if computed_results_labels != []:
    #     for l in computed_results_labels:
    #         l.grid_forget()

    for i in range(1, num_layers):
        print(i, pkeep[i], pkeep[num_layers + i - 1])
        thickness_label = Label(
            layerinputframe, bg="gainsboro", text=str(round(pkeep[i], NDIGITS)))
        thickness_label.grid(row=2+i, column=3)
        computed_results_labels.append(thickness_label)
        resistivity_label = Label(
            layerinputframe, bg="gainsboro", text=str(round(pkeep[num_layers + i - 1], NDIGITS)))
        resistivity_label.grid(row=2+i, column=4)
        computed_results_labels.append(resistivity_label)

    thickness_label = Label(
        layerinputframe, bg="gainsboro", text="Infinite")
    thickness_label.grid(row=2+num_layers, column=3)
    computed_results_labels.append(thickness_label)

    resistivity_label = Label(
        layerinputframe, bg="gainsboro", text=str(round(pkeep[n], NDIGITS)))
    resistivity_label.grid(row=2+num_layers, column=4)
    computed_results_labels.append(resistivity_label)

    errmin_label = Label(
        layerinputframe, bg="gainsboro", text=f"RMS error of Fit = {round(errmin, NDIGITS)}")
    errmin_label.grid(row=3+num_layers, column=3, columnspan=2)
    computed_results_labels.append(errmin_label)


# when plotCurves button pressed, plotCurves executes
def plotCurves():

    # show graph
    plt.show()
    plt.grid(True)


# Main
if __name__ == '__main__':
    # Seed the RNG so we don't have randomness while testing
    # GUI initialization
    mainwindow = Tk()
    mainwindow.title('VES Inverse Monte Carlo')
    mainwindow.configure(background="gainsboro")

    frame = Frame(mainwindow)
    frame.pack()

    # variables used for GUI
    algorithm_index = IntVar(mainwindow, 1)
    num_layers_var = IntVar(mainwindow, 3)
    num_iter = IntVar(mainwindow, 10000)
    openGUI()
    mainwindow.mainloop()
