
class Convertor:
    def __init__(self):
        pass

    def convert(self, record):
        return {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Pokus" } 
                ]}
    
    def generate_description(self, files):
        if len(files) == 1:
            filename, filetype = files[0]
            if filetype == 'application/pdf':
                return 'cajk'
#            if "DP" in files[0]:
#            if "DP" in files[0]:
#                print
            return filename, filetype
        else:
            return 'cajk'
