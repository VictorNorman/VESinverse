from browser import bind, window, document, html
# from VESinverse import VESinverse

class web_gui:
    def __init__(self):
        # VI = VESinverse()
        document['file-upload'].bind('input', self.read_file)
        self.layer_dropdown()
        self.inputs()

    def read_file(self, e):
        def onload(e):
            document['file-text'].value = e.target.result
            my_str = e.target.result
            file_list = my_str.split("\n")
            print(file_list)

            # line 1 chooses what algorithm to run
            # if int(file_list[1]) == 1:
            #     algorithm_choice = 1
            # elif int(file_list[1]) == 2:
            #     algorithm_choice = 2
            # VI.set_index(algorithm_choice)

            # data_length = len(file_list) - 3
            # VI.set_ndat(data_length)

        resistivity_file = document['file-upload'].files[0]
        reader = window.FileReader.new()
        reader.readAsText(resistivity_file)
        # file_handle = open(resistivity_file.name, 'r')
        # file_list = file_handle.readlines()
        # print(resistivity_file.path)
        reader.bind('load', onload)

    def layer_dropdown(self):
        document['layer_choice'] <= "Choose layer: "
        dropdown = html.SELECT(html.OPTION(i) for i in range(6))
        dropdown.bind("change", self.changeLayer)
        document['layer_choice'] <= dropdown

    def changeLayer(self, e):
        print("Layer will be changed")

    def inputs(self):
        for i in range(2):
            thickness_inputs = html.INPUT(type = "Text", id = f"thick_min{i}")
            document['thick_input'] <= thickness_inputs
            thickness_inputs = html.INPUT(type = "Text", id = f"thick_max{i}")
            document['thick_input'] <= thickness_inputs
            document['thick_input'] <= html.BR()
        for i in range(3):
            resistivity_inputs = html.INPUT(type = "Text", id = f"res_min{i}")
            document['res_input'] <= resistivity_inputs
            resistivity_inputs = html.INPUT(type = "Text", id = f"res_max{i}")
            document['res_input'] <= resistivity_inputs
            document['res_input'] <= html.BR()
        