from tkinter import *
import sys
from VESinverse_ajv234 import VESinverse

class VESgui:
    def __init__(self, window):
        self.window = window
        self.window.title("VES Inverse Monte Carlo")
        self.window.configure(background="gainsboro")

        self.VI = VESinverse()

        self.MAX_LAYERS = 5
        self.num_layers = self.VI.get_layers()
        self.num_layers_var = IntVar(self.window, 3)
        self.iterator = IntVar(self.window, self.VI.get_iter())

        self.thick_min_layer = []
        self.thick_max_layer = []
        self.res_min_layer = []
        self.res_max_layer = []
        self.thick_min_entries = []
        self.thick_max_entries = []
        self.res_min_entries = []
        self.res_max_entries = []
        
    def display(self):
        self.preframe = Frame(self.window, background="gainsboro")
        self.preframe.pack(side=TOP, anchor=NW)
        
        self.display_text()
        self.display_buttons()
        self.displayChosenLayers(0, 3)

    def display_text(self):
        # File Path Label
        selected_file = Label(self.preframe, bg="gainsboro", text="Selected File Path")
        selected_file.grid(row=1, column=2)

        # Layer menu label
        dropdown_label = Label(self.preframe, bg="gainsboro",
                               text="Number of Layers", width=20)
        dropdown_label.grid(row=1, column=3)

        # Iteration box label
        iter_label = Label(self.preframe, bg="gainsboro",
                           text="Number of Iterations", width=20)
        iter_label.grid(row=1, column=4)

        self.layerinputframe = Frame(self.window, background="gainsboro")
        self.layerinputframe.pack(side=TOP, anchor=SW)

        # thickness and resistivity labels
        Label(self.layerinputframe, bg="gainsboro", font=("TkDefaultFont", 13),
              text="Model Range in Thickness (m)").grid(row=1, column=1, columnspan=3, pady=5)
        Label(self.layerinputframe, bg="gainsboro", font=("TkDefaultFont", 13),
              text="Model Range in Resistivity (m)").grid(row=1, column=5, columnspan=3, pady=5)

        # thickness minimum values
        Label(self.layerinputframe, bg="gainsboro",
              text="Minimum\nValue", width=15).grid(row=2, column=1)
        # thickness maximum values
        Label(self.layerinputframe, bg="gainsboro",
              text="Maximum\nValue", width=15).grid(row=2, column=2)

        # thickness and resistivity prediction labels
        Label(self.layerinputframe, bg="gainsboro",
              text="Thickness\nPrediction", width=15).grid(row=2, column=3)
        Label(self.layerinputframe, bg="gainsboro",
              text="Resistivity\nPrediction", width=15).grid(row=2, column=4)
        
        # resistivity minimum values
        Label(self.layerinputframe, bg="gainsboro",
              text="Minimum\nValue", width=15).grid(row=2, column=6)
        # resistivity maximum values
        Label(self.layerinputframe, bg="gainsboro",
              text="Maximum\nValue", width=15).grid(row=2, column=7)
        
        # note while testing
        Label(self.layerinputframe, bg="gainsboro", font=("TkDefaultFont", 7),
              text="  --> For predictable results, enter 1 10 5 75 20 2 500 200 100 3000").grid(row=8, column=1, columnspan=3, pady=5)
        
    def display_buttons(self):

        # ------------  below code originally by Rebeca DiCosola ------------
        # ------------  edited by AJ Vrieland
        
        # file explore button
        file_view = Label(self.preframe, bg="gainsboro", text="No file",
                        width=40, wraplength=220, justify="center")
        file_view.grid(row=2, column=2)
        file_explore = Button(self.preframe, text="Select Resistivity Data File")
                            #command=pickFile)              # Will create command later
        file_explore.grid(row=1, column=1, rowspan=2)

        # drop down menu to pic number of layers
        layerlist = list(range(1, self.MAX_LAYERS+1))
        layersmenu = OptionMenu(self.preframe, self.num_layers_var, *layerlist)
        layersmenu.config(bg="gainsboro")
        layersmenu.grid(row=2, column=3)
        #self.num_layers_var.trace("w", <function_name>) # does something when the dropdown menue is changed

        # box to enter number of iterations
        iterentry = Entry(self.preframe, textvariable=self.iterator, width=10)
        iterentry.grid(row=2, column=4, pady=5)

        # - 1 here because bottom layer has Infinite thickness
        for i in range(self.MAX_LAYERS - 1):
            self.thick_min_layer.append(IntVar(self.window))
            self.thick_min_entries.append(Entry(
                self.layerinputframe, textvariable=self.thick_min_layer[i], width=10))
       
        # Add "Infinite" label to bottom of left column.
        # We store it in the thick_min_entries list so that when the number of
        # layers changes, we can remap it.  BUT IT IS NOT AN ENTRY!
        infinite_thickness_label = Label(self.layerinputframe, bg="gainsboro",
                                        text="Infinite Thickness")
        infinite_thickness_label.grid(row=self.num_layers+2, column=1, columnspan=2)
        self.thick_min_entries.append(infinite_thickness_label)

        #thick_max
        for i in range(self.MAX_LAYERS - 1):
            self.thick_max_layer.append(IntVar(self.window))
            self.thick_max_entries.append(Entry(
                self.layerinputframe, textvariable=self.thick_max_layer[i], width=10))
        
        #res_min
        for i in range(self.MAX_LAYERS):
            self.res_min_layer.append(IntVar(self.window))
            self.res_min_entries.append(Entry(
                self.layerinputframe, textvariable=self.res_min_layer[i], width=10))

        #res_max
        for i in range(self.MAX_LAYERS):
            self.res_max_layer.append(IntVar(self.window))
            self.res_max_entries.append(Entry(
                self.layerinputframe, textvariable=self.res_max_layer[i], width=10))
        
        # ------------------ Buttons at the bottom ----------------------

        executionframe = Frame(self.window, background="gainsboro")
        executionframe.pack(side=BOTTOM, anchor=SW)
        execute_VES = Button(executionframe, text="Compute Predictions")      #"Compute Predictions" button
                            #command=self.VI.computePredictions)                      #Calls the computePredictions() function
        execute_VES.grid(row=1, column=1, padx=10, pady=5)

        # plot curves button
        plot_curves = Button(executionframe, text="Plot the Curves")
                            #command=plotCurves)
        plot_curves.grid(row=1, column=2, padx=10, pady=5)

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

if __name__ == '__main__':
    window = Tk()
    VS = VESgui(window)
    VS.display()
    window.mainloop()