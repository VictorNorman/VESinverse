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
        self.num_layers_var = IntVar(self.window, 3)
        self.iterator = IntVar(self.window, self.VI.get_iter())
        
    def display(self):
        # ------------  below code originally by Rebeca DiCosola ------------
        # ------------  edited by AJ Vrieland
        # file explore button
        preframe = Frame(self.window, background="gainsboro")
        preframe.pack(side=TOP, anchor=NW)
        selected_file = Label(preframe, bg="gainsboro", text="Selected File Path")
        selected_file.grid(row=1, column=2)
        file_view = Label(preframe, bg="gainsboro", text="No file",
                        width=40, wraplength=220, justify="center")
        file_view.grid(row=2, column=2)
        file_explore = Button(preframe, text="Select Resistivity Data File")
                            #command=pickFile)              # Will create command later
        file_explore.grid(row=1, column=1, rowspan=2)

        # drop down menu to pic number of layers
        dropdown_label = Label(preframe, bg="gainsboro",
                               text="Number of Layers", width=20)
        dropdown_label.grid(row=1, column=3)
        layerlist = list(range(1, self.MAX_LAYERS+1))
        layersmenu = OptionMenu(preframe, self.num_layers_var, *layerlist)
        layersmenu.config(bg="gainsboro")
        layersmenu.grid(row=2, column=3)
        #self.num_layers_var.trace("w", <function_name>) # does something when the dropdown menue is changed

        # box to enter number of iterations
        iter_label = Label(preframe, bg="gainsboro",
                           text="Number of Iterations", width=20)
        iter_label.grid(row=1, column=4)
        iterentry = Entry(preframe, textvariable=self.iterator, width=10)
        iterentry.grid(row=2, column=4, pady=5)


if __name__ == '__main__':
    window = Tk()
    VS = VESgui(window)
    VS.display()
    window.mainloop()