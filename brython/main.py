from browser import bind, window, document, html
from VESinverse import VESinverse

def read_file(e):
        def onload(e):
            document['file-text'].value = e.target.result
            my_str = e.target.result
            file_list = my_str.split("\n")
            print(file_list)

            # line 1 chooses what algorithm to run
            if int(file_list[1]) == 1:
                algorithm_choice = 1
            elif int(file_list[1]) == 2:
                algorithm_choice = 2
            VI.set_index(algorithm_choice)

            data_length = len(file_list) - 3
            VI.set_ndat(data_length)

        resistivity_file = document['file-upload'].files[0]
        reader = window.FileReader.new()
        reader.readAsText(resistivity_file)
        # file_handle = open(resistivity_file.name, 'r')
        # file_list = file_handle.readlines()
        # print(resistivity_file.path)
        reader.bind('load', onload)

VI = VESinverse()
document['file-upload'].bind('input', read_file)