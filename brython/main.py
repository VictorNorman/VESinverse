from browser import bind, window, document, html
from VESinverse import VESinverse

class web_gui:
    def __init__(self):
        self.VI = VESinverse()
        document['file-upload'].bind('input', self.read_file)
        document['Compute'].bind('click', self.computePredictions)
        document['Show_graph'].bind('click', self.showGraph)
        self.layer_dropdown()
        self.layers = 3
        self.inputs()
        # self.viewModel()
        

    def read_file(self, e):
        def onload(e):
            document['file-text'].value = e.target.result
            my_str = e.target.result
            file_list = my_str.split("\n")
            print(file_list)

            # line 1 chooses what algorithm to run
            if int(file_list[1]) == 1:
                algorithm_choice = 1
                print(algorithm_choice)
            elif int(file_list[1]) == 2:
                algorithm_choice = 2
            self.VI.set_index(algorithm_choice)

            data_length = len(file_list) - 3
            self.VI.set_ndat(data_length)

            g_adat = [0]*data_length
            g_rdat = [0]*data_length

            for i in range(3, len(file_list)):
                line_str = file_list[i].split()
                spacing_val = float(line_str[0].strip())
                print(f"spacing_val: {spacing_val}")
                resis_val = float(line_str[1].strip())
                print(f"resis_val: {resis_val}")

                g_adat[i-3] = spacing_val
                g_rdat[i-3] = resis_val

            self.VI.set_adat(g_adat)
            self.VI.set_rdat(g_rdat)

            self.VI.readData()

        resistivity_file = document['file-upload'].files[0]
        reader = window.FileReader.new()
        reader.readAsText(resistivity_file)
        reader.bind('load', onload)

    def layer_dropdown(self):
        document['layer_choice'] <= "Choose layer: "
        dropdown = html.SELECT(html.OPTION(i) for i in range(6))
        dropdown.bind("change", self.changeLayer)
        dropdown.selectedIndex = 3
        document['layer_choice'] <= dropdown

    def changeLayer(self, e):
        self.layers = e.target.selectedIndex
        self.inputs()
        

    def inputs(self):
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
        
        t_min = []
        t_max = []
        r_min = []
        r_max = []
        for i in range(self.layers - 1):
            t_min.append(float(document[f'thick_min{i}'].value))
            t_max.append(float(document[f'thick_max{i}'].value))
        for i in range(self.layers):
            r_min.append(float(document[f'res_min{i}'].value))
            r_max.append(float(document[f'res_max{i}'].value))
        
        self.VI.set_thickness_minimum(t_min)   # thickness_minimum is not being set or somehow the getter is not working
        self.VI.set_thickness_maximum(t_max)
        self.VI.set_resistivity_minimum(r_min)
        self.VI.set_resistivity_maximum(r_max)

        print(f"adat: {self.VI.get_adat()} \nrdat: {self.VI.get_rdat()}")
        print(t_min)
        # print(self.VI.get_thickness_minimum())
        print(self.VI.get_thickness_maximum())
        print(self.VI.get_resistivity_minimum())
        print(self.VI.get_resistivity_maximum())
        self.VI.computePredictions()
        # self.viewModel()

    # def viewModel(self):
    #     heading = html.H1(text = "Thickness results,  Resistivity resluts")
    #     document['results'] <= heading

    
    def showGraph(self, e):
        print("Also might not work")