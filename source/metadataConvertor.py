# TODO kodovani
class MetadataConvertor:
    purl = [ 
            '{http://purl.org/dc/elements/1.1/}title', # na konci je všude [rukopis], před tím to je ok
            '{http://purl.org/dc/elements/1.1/}creator', #vice hodnot katedry by šlo teoreticky třídit
            '{http://purl.org/dc/elements/1.1/}type', # viz type_type, ale neoveřené bo kodování
            '{http://purl.org/dc/elements/1.1/}date', # rok 2002 nebo [2002]
            '{http://purl.org/dc/elements/1.1/}publisher', # většinou Praha, občas jiné město občas bordel
            '{http://purl.org/dc/elements/1.1/}language', # cajk pár hodnot
            '{http://purl.org/dc/elements/1.1/}description', #totalně růné mnoho tisiciznakových
            '{http://purl.org/dc/elements/1.1/}subject', #někdy keywords, někdy fakulta, někdy 'bakalářská práce'
            '{http://purl.org/dc/elements/1.1/}identifier', #dva typy odkazů
            '{http://purl.org/dc/elements/1.1/}rights', # u 17 objektů, něco z toho nejsou regulerni stringy
            '{http://purl.org/dc/elements/1.1/}relation',# jen jednou - odpad
            ]
    type_tyes = [
            'text',
            'dizertace',
            'manuscriptext',
            'manuscripttext',
            'diplomovÃ© prÃ¡cefd132022czenas',
            'rigorÃ³znÃ­ prÃ¡cefd132407czenas',
            'bakalÃ¡ÅskÃ© prÃ¡cefd132403czenas',
            'zÃ¡vÄ<U+009B>reÄ<U+008D>nÃ© prÃ¡ce',
            'habilitaÄ<U+008D>nÃ­ prÃ¡ce',
            ]
    language_values = [ 'cze', 'ger', 'eng', 'slo', 'fre', 'pol' ]
    example_return = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Pokus" } 
                ]}

    def convertYear(self, year):
        if year[0] == '[':
            year = year[1:]
        if len(year) > 4 and year[-1] == ']':
            year = year[:-1]
        if len(year) > 4 and year[4] == '?':
            year = year[:-1]
        if 'prosinec ' in year:
            year = year[9:]
        if 'jen' in year:
            year = year[8:]
        assert len(year) == 4
        assert int(year) > 1919
        assert int(year) < 2019
        return year

    def convertDC(self, record, oai_id):
        for tag, value in record:
            if 'date' in tag:
                if oai_id in ['77317','77441','71436','75970']: # TODO špatné metadata
                    continue
                year = self.convertYear(value)
            if 'language' in tag:
                assert value in self.language_values
            if 'description' in tag:
                pass
                #if len(value) > 300:
                #    print(oai_id,len(value))
            #if 'relation' in tag:
            #    print(oai_id,len(value))
            #    print(value)
        return self.example_return
    
    def convertRecord(self, record, oai_id):
        #for tag, value in record:
        #    print(tag,value)
        return self.example_return
