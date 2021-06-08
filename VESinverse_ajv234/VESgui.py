from tkinter import *
from tkinter import filedialog
import sys
from VESinverse_ajv234 import VESinverse
import argparse


class VESgui:
    def __init__(self, window):
        self.window = window
        self.window.title("VES Inverse Monte Carlo")

        self.VI = VESinverse()

        self.MAX_LAYERS = 5
        self.num_layers = self.VI.get_layers()
        self.num_layers_var = IntVar(self.window, 3)
        self.iterator = IntVar(self.window, self.VI.get_iter())
        self.thickness_label = Label()
        self.resistivity_label = Label()
        self.errmin_label = Label()

        self.thick_min_layer = []
        self.thick_max_layer = []
        self.res_min_layer = []
        self.res_max_layer = []
        self.thick_min_entries = []
        self.thick_max_entries = []
        self.res_min_entries = []
        self.res_max_entries = []

        self.curr_num_layers = 3
        self.computed_results_labels = []
        self.is_input_file = False
        self.input_file = ""

    def display(self):
        self.preframe = Frame(self.window)
        self.preframe.pack(side=TOP, anchor=NW)
        # self.displayChosenLayers(0, 3)
        self.display_text()
        self.display_buttons()

    def display_text(self):
        # File Path Label
        selected_file = Label(self.preframe, text="Selected File Path")
        selected_file.grid(row=1, column=2)

        # Layer menu label
        dropdown_label = Label(self.preframe,
                               text="Number of Layers", width=20)
        dropdown_label.grid(row=1, column=3)

        # Iteration box label
        iter_label = Label(self.preframe,
                           text="Number of Iterations", width=20)
        iter_label.grid(row=1, column=4)

        self.layerinputframe = Frame(self.window)
        self.layerinputframe.pack(side=TOP, anchor=SW)

        # thickness and resistivity labels
        Label(self.layerinputframe, font=("TkDefaultFont", 13),
              text="Model Range in Thickness (m)").grid(row=1, column=1, columnspan=3, pady=5)
        Label(self.layerinputframe, font=("TkDefaultFont", 13),
              text="Model Range in Resistivity (m)").grid(row=1, column=5, columnspan=3, pady=5)

        # thickness minimum values
        Label(self.layerinputframe,
              text="Minimum\nValue", width=15).grid(row=2, column=1)
        # thickness maximum values
        Label(self.layerinputframe,
              text="Maximum\nValue", width=15).grid(row=2, column=2)

        # thickness and resistivity prediction labels
        Label(self.layerinputframe,
              text="Thickness\nPrediction", width=15).grid(row=2, column=3)
        Label(self.layerinputframe,
              text="Resistivity\nPrediction", width=15).grid(row=2, column=4)

        # resistivity minimum values
        Label(self.layerinputframe,
              text="Minimum\nValue", width=15).grid(row=2, column=6)
        # resistivity maximum values
        Label(self.layerinputframe,
              text="Maximum\nValue", width=15).grid(row=2, column=7)

        # note while testing
        Label(self.layerinputframe, font=("TkDefaultFont", 7),
              text="  --> For predictable results, enter 1 10 5 75 20 2 500 200 100 3000").grid(row=8, column=1, columnspan=3, pady=5)

    def display_buttons(self):

        # ------------  below code originally by Rebeca DiCosola ------------
        # ------------  edited by AJ Vrieland

        # file explore button
        self.file_view = Label(self.preframe, text="No file",
                               width=40, wraplength=220, justify="center")
        self.file_view.grid(row=2, column=2)
        if not self.is_input_file:
            file_explore = Button(self.preframe, text="Select Resistivity Data File",
                                  command=self.pickFile)
        else:
            file_explore = Button(self.preframe, text="Select Resistivity Data File",
                                  command=self.pickFile(self.input_file))
        file_explore.grid(row=1, column=1, rowspan=2)

        # drop down menu to pic number of layers
        layerlist = list(range(1, self.MAX_LAYERS+1))
        layersmenu = OptionMenu(self.preframe, self.num_layers_var, *layerlist)
        layersmenu.grid(row=2, column=3)
        self.num_layers_var.trace("w", self.numLayersChanged)
        self.curr_num_layers = self.num_layers

        # box to enter number of iterations
        iterentry = Entry(self.preframe, textvariable=self.iterator, width=10)
        iterentry.grid(row=2, column=4, pady=5)

        # - 1 here because bottom layer has Infinite thickness
        for i in range(self.MAX_LAYERS - 1):
            print(self.thick_min_layer)
            self.thick_min_layer.append(IntVar(self.window))
            self.thick_min_entries.append(Entry(
                                          self.layerinputframe, textvariable=self.thick_min_layer[i], width=10))

        # Add "Infinite" label to bottom of left column.
        # We store it in the thick_min_entries list so that when the number of
        # layers changes, we can remap it.  BUT IT IS NOT AN ENTRY!
        infinite_thickness_label = Label(self.layerinputframe,
                                         text="Infinite Thickness")
        infinite_thickness_label.grid(row=self.num_layers+2, column=1, columnspan=2)
        self.thick_min_entries.append(infinite_thickness_label)

        # thick_max
        for i in range(self.MAX_LAYERS - 1):
            self.thick_max_layer.append(IntVar(self.window))
            self.thick_max_entries.append(Entry(
                                          self.layerinputframe, textvariable=self.thick_max_layer[i], width=10))

        # res_min
        for i in range(self.MAX_LAYERS):
            self.res_min_layer.append(IntVar(self.window))
            self.res_min_entries.append(Entry(
                self.layerinputframe, textvariable=self.res_min_layer[i], width=10))

        # res_max
        for i in range(self.MAX_LAYERS):
            self.res_max_layer.append(IntVar(self.window))
            self.res_max_entries.append(Entry(
                self.layerinputframe, textvariable=self.res_max_layer[i], width=10))

        # self.displayChosenLayers(0, self.num_layers)

        # ------------------ Buttons at the bottom ----------------------

        executionframe = Frame(self.window)
        executionframe.pack(side=BOTTOM, anchor=SW)
        execute_VES = Button(executionframe, text="Compute Predictions",     # "Compute Predictions" button
                             command=self.computation)                      # Calls the computePredictions() function
        execute_VES.grid(row=1, column=1, padx=10, pady=5)

        # plot curves button
        plot_curves = Button(executionframe, text="Plot the Curves",
                             command=self.VI.graph)                      # if you close the graph and click the button again the graph is empty
        plot_curves.grid(row=1, column=2, padx=10, pady=5)

        self.displayChosenLayers(0, self.num_layers)

    def displayChosenLayers(self, old_num_layers, curr_num_layers):
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
                self.thick_min_entries[i].grid(row=i+3, column=1)
                self.thick_max_entries[i].grid(row=i+3, column=2)
            for i in range(old_num_layers - 1, curr_num_layers):
                self.res_min_entries[i].grid(row=i+3, column=6)
                self.res_max_entries[i].grid(row=i+3, column=7)

        else:
            # fewer layers to be shown now: use grid_forget() to un-display them
            for i in range(old_num_layers - 2, curr_num_layers - 2, -1):
                self.thick_min_entries[i].grid_forget()
                self.thick_max_entries[i].grid_forget()
            for i in range(old_num_layers - 1, curr_num_layers - 1, -1):
                self.res_min_entries[i].grid_forget()
                self.res_max_entries[i].grid_forget()

        # Move the "Infinite Thickness" label
        inf_thickness_label = self.thick_min_entries[self.MAX_LAYERS - 1]
        inf_thickness_label.grid(row=curr_num_layers+2, column=1, columnspan=2)

    def pickFile(self, file=""):
        if file == "":
            # # get file
            resistivity_file = filedialog.askopenfilename(initialdir="/",
                                                          title="Open File",
                                                          filetypes=(("Text Files", "*.txt"),
                                                                     ("All Files", "*.*")))

            # dir for testing
            # resistivity_file = filedialog.askopenfilename(initialdir="/home/ajv234/Documents/VESinverse",
            #                                               title="Open File",
            #                                               filetypes=(("Text Files", "*.txt"),
            #                                                          ("All Files", "*.*")))
        else:
            resistivity_file = file
        self.file_view.config(text=resistivity_file)
        file_handle = open(resistivity_file, "r")
        file_list = file_handle.readlines()

        # when printing, skip first 2 lines: data starts in line 3.
        for i in range(0, len(file_list)):
            print(file_list[i])

        # algorithm to use is on line 1 (second line).
        if int(file_list[1].strip()) == 1:
            algorithm_choice = 1
        elif int(file_list[1].strip()) == 2:
            algorithm_choice = 2
        else:
            print('Algorithm choice on line 2 must be 1 or 2', file=sys.stderr)
            sys.exit(-1)
        self.VI.set_index(algorithm_choice)

        # number of data values
        data_length = len(file_list) - 3
        self.VI.set_ndat(data_length)

        g_adat = [0]*data_length          # g_adat and g_rdat (gui_xdat) are temporary arrays that this function uses and then
        g_rdat = [0]*data_length          # passes through the VI's adat and rdat setter

        # for each data line
        for i in range(3, len(file_list)):
            fields = file_list[i].split()
            spacing_val = float(fields[0].strip())
            # print('-->' + spacing_val + '<--')
            resis_val = float(fields[1].strip())
            # print('-->' + resis_val + '<--')

            # TODO: better name for adat or spacing_val?: what are these values?
            g_adat[i-3] = spacing_val
            g_rdat[i-3] = resis_val

        self.VI.set_adat(g_adat)
        self.VI.set_rdat(g_rdat)

        # TODO: do we handle files with the ending line of 0 0 ? Should we?

        # Instead of doing v I am just calling the function readData() from VESinverse
        # compute log10 values of adat and rdat
        self.VI.readData()

    def numLayersChanged(self, *args):
        # Clear displayed results
        if self.computed_results_labels != []:
            for labels in self.computed_results_labels:
                labels.grid_forget()
        self.computed_results_labels = []

        new_num_layers = self.num_layers_var.get()
        if new_num_layers != self.curr_num_layers:
            print(f"num_layers changed from {self.curr_num_layers} to {new_num_layers}")
            self.displayChosenLayers(self.curr_num_layers, new_num_layers)
        # Store new value as current value
        self.curr_num_layers = new_num_layers

    def computation(self):

        # g_small = self.VI.get_small()       # g_small, and g_xlarge are local instances of small and xlarge
        # g_xlarge = self.VI.get_xlarge()     # from VESinverse
        t_min = []
        t_max = []
        r_min = []
        r_max = []

        # set small[] and xlarge[]
        for i in range(self.curr_num_layers - 1):
            t_min.append(self.thick_min_layer[i].get())
        for i in range(self.curr_num_layers - 1):
            t_max.append(self.thick_max_layer[i].get())
        for i in range(self.curr_num_layers):
            r_min.append(self.res_min_layer[i].get())
        for i in range(self.curr_num_layers):
            r_max.append(self.res_max_layer[i].get())

        self.VI.set_thickness_minimum(t_min)
        self.VI.set_thickness_maximum(t_max)
        self.VI.set_resistivity_minimum(r_min)
        self.VI.set_resistivity_maximum(r_max)

        self.VI.set_layers(self.curr_num_layers)
        self.VI.computePredictions()

        self.viewModel()

    def viewModel(self):
        self.thickness_label.grid_forget()
        self.resistivity_label.grid_forget()
        self.errmin_label.grid_forget()
        # Somewhere in here remove the labels when computing predictions for a new layer
        g_pkeep = self.VI.get_pkeep()
        g_errmin = self.VI.get_errmin()
        g_layer_index = self.VI.get_layer_index()

        for i in range(0, self.curr_num_layers - 1):
            print(i, g_pkeep[i], g_pkeep[i + self.curr_num_layers - 1])
            self.thickness_label = Label(self.layerinputframe,
                                         text=str(round(g_pkeep[i], 3)))
            self.thickness_label.grid(row=3+i, column=3)
            self.resistivity_label = Label(self.layerinputframe,
                                           text=str(round(g_pkeep[self.curr_num_layers+i-1], 3)))
            self.resistivity_label.grid(row=3+i, column=4)

        self.thickness_label = Label(self.layerinputframe,
                                     text="Infinite")
        self.thickness_label.grid(row=2+self.curr_num_layers, column=3)

        self.resistivity_label = Label(self.layerinputframe,
                                       text=str(round(g_pkeep[g_layer_index-1], 3)))
        self.resistivity_label.grid(row=2+self.curr_num_layers, column=4)

        self.errmin_label = Label(self.layerinputframe,
                                  text=f"RMS error of Fit = {round(g_errmin, 3)}")
        self.errmin_label.grid(row=3+self.curr_num_layers, column=3, columnspan=2)

    def parse_input(self):
        parser = argparse.ArgumentParser()
        # These are all the options for Command Line Arguments,
        # however the thick and res varients could used better names
        # TODO: maybe use regex to clean up how it handles thick and res inputs
        parser.add_argument("-i", "--iter", nargs=1, help="Fills in the iterator")
        parser.add_argument("-l", "--layers", nargs=1, help="How many layers to use")
        parser.add_argument("-f", "--file", help="Add file path")
        parser.add_argument("-ti", "--thick_min", nargs='*', help="The inputs for the thick min values")
        parser.add_argument("-ta", "--thick_max", nargs='*', help="The inputs for the thick max values")
        parser.add_argument("-ri", "--resmin", nargs='*', help="The inputs for the res min values")
        parser.add_argument("-ra", "--resmax", nargs='*', help="The inputs for the res max values")
        args = parser.parse_args()
        if args.iter:
            self.iterator = IntVar(self.window, int(args.iter[0]))
        if args.layers:
            self.num_layers_var = IntVar(self.window, int(args.layers[0]))
            self.num_layers = self.curr_num_layers = int(args.layers[0])
        if args.file:
            self.is_input_file = True
            self.input_file = args.file
        if args.thick_min:
            # args.<argument> is a list, and args.<argument>[0] is always a string
            # as of right now the numbers must be separated by a comma and no space
            # but I want to add it so that the number can be spaced by multiple different things
            thick_min = args.thick_min[0]
            thick_min = thick_min.split(',')
            print(thick_min)
            for i in range(self.num_layers-1):
                self.thick_min_layer.append(IntVar(self.window, int(thick_min[i])))
        if args.thick_max:
            thick_max = args.thick_max[0]
            thick_max = thick_max.split(',')
            for i in range(self.num_layers-1):
                self.thick_max_layer.append(IntVar(self.window, int(thick_max[i])))
        if args.resmin:
            res_min = args.resmin[0]
            res_min = res_min.split(',')
            for i in range(self.num_layers):
                self.res_min_layer.append(IntVar(self.window, int(res_min[i])))
        if args.resmax:
            res_max = args.resmax[0]
            res_max = res_max.split(',')
            for i in range(self.num_layers):
                self.res_max_layer.append(IntVar(self.window, int(res_max[i])))


if __name__ == '__main__':
    window = Tk()
    VS = VESgui(window)
    if len(sys.argv) >= 2:
        VS.parse_input()
    VS.display()

    window.mainloop()
