
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
        #TODO tohle celé zkonrolovat eliškou
        bc = ['BC','bp','BP','bc','Bakaraska','baklarka','Bc','Bakalarska','bakalarka','bakalarska','Ba','Bak']
        dp = ['DP','Diplomova','Diplomka','diplomka','diplomova','dp','dP','dip','DIP']
        rp = ['rigorózni','rigo','dis','Dis','RP','rp','rg','phd']
        weird = ['DT-config_guide','Dodatky','clanek','posudek']
        vedouci = ['vedouci']
        oponent = ['opon']
        posudek = ['posud'] + vedouci + oponent
        prilohy = ['Priloh','pril','Obr','příloh','grafy','summary']
        priloha = prilohy + ['chyby','literatura']
        classic_tags = posudek + priloha
        def has(tags, filename):
            for tag in tags:
                if tag in filename:
                    return True
            return False
        if len(files) == 1:
            filename, filetype = files[0]
            if filetype == 'application/pdf':
                if has(dp, filename):
                    return [(filename, filetype, "Diplomová práce")]
                elif has(bc, filename):
                    return [(filename, filetype, "Bakalářská práce")]
                elif has(rp, filename):
                    return [(filename, filetype, "Rigorózní práce")]
                elif has(weird, filename):
                    return [] #TODO
                else:
                    return [(filename, filetype, "Závěrečná práce")]
            else:
                return [] #TODO
        else:
            other = 0
            for filename, filetype in files:
                if not has(classic_tags,filename):
                    other += 1
            if other == 1:
                res = []
                for filename, filetype in files:
                    if has(vedouci, filename):
                        res.append((filename, filetype, "Posudek vedoucího"))
                    elif has(oponent, filename):
                        res.append((filename, filetype, "Posudek oponenta"))
                    elif has(posudek, filename):
                        res.append((filename, filetype, "Posudek"))
                    elif has(prilohy, filename):
                        res.append((filename, filetype, "Příloha"))
                    elif has(['chyby'], filename):
                        res.append((filename, filetype, "Chyby"))
                    elif has(['literatura'], filename):
                        res.append((filename, filetype, "Literatura"))
                    else:
                        if has(dp, filename):
                            res.append((filename, filetype, "Diplomová práce"))
                        elif has(bc, filename):
                            res.append((filename, filetype, "Bakalářská práce"))
                        elif has(rp, filename):
                            res.append((filename, filetype, "Rigorózní práce"))
                        else:
                            res.append((filename, filetype, "Závěrečná práce"))
                return res
            else:
                return [] #TODO
