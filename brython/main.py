from browser import bind, window, document, html

def read_file(e):
        def onload(e):
            document['file-text'].value = e.target.result
            print(document['file-text'].value[22])
        
        resistivity_file = document['file-upload'].files[0]
        reader = window.FileReader.new()
        reader.readAsText(resistivity_file)
        # file_handle = open(resistivity_file.name, 'r')
        # file_list = file_handle.readlines()
        # print(resistivity_file.path)
        reader.bind('load', onload)

document['file-upload'].bind('input', read_file)