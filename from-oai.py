#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET

server="dingo.ruk.cuni.cz:8881"
verb="ListRecords"
metadataPrefix="oai_dc"
oai_sets=["oai_kval","oai_kvalDC"]
# nacte 3455,411 praci

def get_oai_metadata(oai_set):
    url = "http://"+server+"/OAI-PUB?verb="+verb+"&metadataPrefix="+metadataPrefix+"&set="+oai_set
    def recursion(url, resumptionToken):
        if resumptionToken is None:
            response = requests.get(url)
        else:
            response = requests.get(url+"&resumptionToken="+resumptionToken)
        root = ET.fromstring(response.text)
        ListRecord=list(r for r in root if "ListRecords" in r.tag)[0]
        for child in ListRecord:
            if "record" in child.tag: 
                yield child
            elif "resumptionToken" in child.tag:
                resumptionToken = child.text
                yield from recursion(url,resumptionToken)
            else:
                raise "Unknown tag"
    return recursion(url,None)

records = get_oai_metadata(oai_sets[1])
first = list(records)[0]
#print( ET.tostring(first) )

#for child in first: