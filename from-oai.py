#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET

server="dingo.ruk.cuni.cz:8881"
verb="ListRecords"
metadataPrefix="oai_dc"
oai_sets=["oai_kval","oai_kvalDC"]
# nacte 3455,411 praci
#3892

def tag(root,tag):
    subtree=list(r for r in root if tag in r.tag)[0]
    if subtree is None:
        raise "No tag "+tag
    return subtree


def get_oai_records(oai_set):
    url = "http://"+server+"/OAI-PUB?verb="+verb+"&metadataPrefix="+metadataPrefix+"&set="+oai_set
    def recursion(url, resumptionToken):
        if resumptionToken is None:
            response = requests.get(url)
        else:
            response = requests.get(url+"&resumptionToken="+resumptionToken)
        root = ET.fromstring(response.text)
        ListRecord=tag(root,"ListRecords")
        for child in ListRecord:
            if "record" in child.tag: 
                yield child
            elif "resumptionToken" in child.tag:
                resumptionToken = child.text
                yield from recursion(url,resumptionToken)
            else:
                raise "Unknown tag"
    return recursion(url,None)

def hui(record):
    metadata=tag(record,"metadata")
    for child in metadata:
        print(child.tag) 

records = get_oai_records(oai_sets[1])
first = list(records)[0]
#print( ET.tostring(first) )
hui(first)
#for child in first: