from browser import bind, window, document, html
from VESinverse import VESinverse
import brycharts
import math

class web_gui:
    def __init__(self):
        self.VI = VESinverse()
        document['file-upload'].bind('input', self.read_file)
        document['Compute'].bind('click', self.computePredictions)
        document['Show_graph'].bind('click', self.showGraph)
        document['iteration'].value = self.VI.get_iter()
        self.layer_dropdown()
        self.layers = 3
        self.inputs()
        # self.viewModel()
        

    def read_file(self, e):
    # I'm not sure why the nested function is necessary
    # but brython documentation shows this is how it is done
        def onload(e):
            # Takes in the string of the file and splits at newlines
            my_str = e.target.result
            file_list = my_str.split("\n")
            # print(file_list)

            # line 1 chooses what algorithm to run
            if int(file_list[1]) == 1:
                algorithm_choice = 1
                # print(algorithm_choice)
            elif int(file_list[1]) == 2:
                algorithm_choice = 2
            self.VI.set_index(algorithm_choice)

            # Sets ndat in VESinverse based on length of data in file
            data_length = len(file_list) - 3
            self.VI.set_ndat(data_length)

            # Initializing some local variables to put 
            # file data into
            g_adat = [0]*data_length
            g_rdat = [0]*data_length

            # Puts data from file into the local variables
            for i in range(3, len(file_list)):
                line_str = file_list[i].split()
                spacing_val = float(line_str[0].strip())
                # print(f"spacing_val: {spacing_val}")
                resis_val = float(line_str[1].strip())
                # print(f"resis_val: {resis_val}")

                g_adat[i-3] = spacing_val
                g_rdat[i-3] = resis_val

            # Passes the local variables back into VESinverse
            # to be used in computation
            self.VI.set_adat(g_adat)
            self.VI.set_rdat(g_rdat)

            # self.VI.readData()

        # Takes in the file selected, converts it into a string
        # and sends it to the onload nested function 
        resistivity_file = document['file-upload'].files[0]
        reader = window.FileReader.new()
        reader.readAsText(resistivity_file)
        reader.bind('load', onload)

    def layer_dropdown(self):
        # Displays the layer dropdown initialized at 3 layers
        # and passes changes to the changeLayer function
        document['layer_choice'] <= "Choose layer: "
        dropdown = html.SELECT(html.OPTION(i) for i in range(6))
        dropdown.bind("change", self.changeLayer)
        dropdown.selectedIndex = 3
        document['layer_choice'] <= dropdown

    def changeLayer(self, e):
        # Puts new layer # into self.layers and calls self.inputs()
        self.layers = e.target.selectedIndex
        self.inputs()
        

    def inputs(self):
        # On inital call will draw number of text boxes based on number of layers
        # When called through a change of layers, it first clears the screen and 
        # draws layers based on new number of layers and passes number of layers to
        # VESinverse
        document['thick_input'].clear()
        document['res_input'].clear()
        for i in range(self.layers - 1):
            thickness_inputs = html.INPUT(type = "Text", id = f"thick_min{i}")
            document['thick_input'] <= thickness_inputs
            thickness_inputs = html.INPUT(type = "Text", id = f"thick_max{i}")
            document['thick_input'] <= thickness_inputs
            document['thick_input'] <= html.BR()
        for i in range(self.layers):
            resistivity_inputs = html.INPUT(type = "Text", id = f"res_min{i}")
            document['res_input'] <= resistivity_inputs
            resistivity_inputs = html.INPUT(type = "Text", id = f"res_max{i}")
            document['res_input'] <= resistivity_inputs
            document['res_input'] <= html.BR()
        self.VI.set_layers(self.layers)
        
    def computePredictions(self, e):
        # Takes in the inputs from the text boxes and puts passes them to
        # VESinverse 

        # Initalizing local variables to put input values into and then pass these
        # directly to VESinverse
        t_min = []
        t_max = []
        r_min = []
        r_max = []
        # Reads inputs into above mentioned local variables based on number of layers
        for i in range(self.layers - 1):
            t_min.append(float(document[f'thick_min{i}'].value))
            t_max.append(float(document[f'thick_max{i}'].value))
        for i in range(self.layers):
            r_min.append(float(document[f'res_min{i}'].value))
            r_max.append(float(document[f'res_max{i}'].value))
        
        # Passing local variables to VESinverse via setter methods
        self.VI.set_iter(int(document['iteration'].value))
        self.VI.set_thickness_minimum(t_min)
        self.VI.set_thickness_maximum(t_max)
        self.VI.set_resistivity_minimum(r_min)
        self.VI.set_resistivity_maximum(r_max)
        self.VI.set_random(0)

        # Initiallize some variables within VESinverse based on inputs and file
        # then computes prediction and outputs results
        self.VI.computePredictions()
        self.viewModel()

    def viewModel(self):
        # Displays the outputs of the computation underneath the input boxes
        # TODO: Not working fully atm, the infinite span is not displaying
        document['results'].clear()
        heading = html.H4("Thickness results,  Resistivity results")
        document['results'] <= heading
        results = self.VI.get_pkeep()
        layer_index = self.VI.get_layer_index()
        for i in range(self.layers - 1):
            output = html.H4("%9.1f:   \t%9.3f  \t%9.3f" % (i+1, results[i], results[self.layers+i-1]))
            document['results'] <= output
            document['results'] <= html.BR()
            print(i)
        infinite = html.H4("%9.1f:  Infinite   %9.3f" % (self.layers, results[layer_index-1]))
        document['results'] <= infinite

    
    def showGraph(self, e):
        x_axis = self.VI.get_x_axis()
        y_axis = self.VI.get_y_axis()
        blue_x = self.VI.get_blue_x()
        blue_y = self.VI.get_blue_y()
        red_x = self.VI.get_red_x()
        red_y = self.VI.get_red_y()
        rpn = self.VI.get_resistivity_point()
        graph_dict = {}
        red_coordinates = []
        blue_coordinates = []
        line_coordinates = []

        for i in range(self.VI.get_ndat()):
            red_coordinates.append((math.log10(red_x[i]), math.log10(red_y[i])))
            blue_coordinates.append((math.log10(blue_x[i]), math.log10(blue_y[i])))
        
        for i in range(rpn):
            line_coordinates.append((math.log10(x_axis[i]), math.log10(y_axis[i])))


        graph_dict.update({"Red" : red_coordinates})
        graph_dict.update({"Blue" : blue_coordinates})
        graph_dict.update({"Line" : line_coordinates})

        print(graph_dict)

        data = brycharts.PairedDataDict("X", "Y", graph_dict)
        brycharts.LineGraph(document, data)