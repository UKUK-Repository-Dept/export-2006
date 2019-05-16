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
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
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

def get_filenames(interni_id):
    try:
        tree = ET.parse('digital_entities/'+str(interni_id)+".xml")
    except:
        #print(interni_id)
        return
    root = tree.getroot()
    for stream_ref in root.findall("./*stream_ref"):
        filename = stream_ref.find('file_name').text
        if filename != None:
            yield filename
    subrecords = []
    for relations in root.findall("./*relations"):
        for relation in relations:
            relation_type = relation.find('type').text
            if relation_type == "include":
                pid = relation.find('pid').text
                subrecords.append(pid)
    for record in subrecords:
        yield from get_filenames(record)

def hui(record):
    header=tag(record,"header")
    identifier=tag(header,"identifier").text
    oai_id = identifier.split(":")[-1]
    files=list(get_filenames(oai_id))
#    print(files)
    for file in files:
        print(file)
#    if len(files) != 0:
#        print(oai_id)
#        metadata=tag(tag(record,"metadata"),"record")
#        for child in metadata:
#            print(child.tag, child.text)

    

records = get_oai_records(oai_sets[0])
#first = list(records)[0]
#print( ET.tostring(first) )
#hui(first)
for record in records:
    hui(record)
records = get_oai_records(oai_sets[1])
#first = list(records)[0]
#print( ET.tostring(first) )
#hui(first)
for record in records:
    hui(record)