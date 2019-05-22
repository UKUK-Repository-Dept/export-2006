#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET

server="dingo.ruk.cuni.cz:8881"
verb=["ListRecords","ListMetadataFormats"]
metadataPrefix="oai_dc"
oai_sets=["oai_kval","oai_kvalDC"]
# nacte 3455,411 praci
identifier_prefix = "oai:DURCharlesUniPrague.cz:"

def tag(root,tag):
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

def get_oai_records(oai_set):
    url = "http://"+server+"/OAI-PUB?verb="+verb[0]+"&metadataPrefix="+metadataPrefix+"&set="+oai_set
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

def get_oai_id(record):
    header=tag(record,"header")
    identifier=tag(header,"identifier").text
    return identifier.split(":")[-1]

def hui(record):
    header=tag(record,"header")
    identifier=tag(header,"identifier").text
    oai_id = identifier.split(":")[-1]
    files=list(get_filenames(oai_id))
    return files
#    if len(files) != 0:
#        print(oai_id)
#        metadata=tag(tag(record,"metadata"),"record")
#        for child in metadata:
#            print(child.tag, child.text)



records0 = list(get_oai_records(oai_sets[0]))
records1 = list(get_oai_records(oai_sets[1]))

for record in records1:
    print(get_oai_id(record))

def search_records(phrase):
    for record in records0 + records1:
        str_rec = str(ET.tostring(record))
        if phrase in str_rec:
            yield record

def list_format(filename):
    for row in open(filename,"r"):
        oai_id = row[:-1]
        url = "http://"+server+"/OAI-PUB?verb="+verb[1]+"&identifier="+identifier_prefix+oai_id
        response = requests.get(url).text
        if "id does not exist" not in response:
            root = ET.fromstring(response)
            metadataFormats=tag(root,"ListMetadataFormats")
            for metadata in metadataFormats:
                child = tag(metadata,"metadataPrefix")
                print( child.text)

def list_without_metadata(filename):
    for row in open(filename,"r"):
        oai_id = row.split("_")[0]
        url = "http://"+server+"/OAI-PUB?verb="+verb[1]+"&identifier="+identifier_prefix+oai_id
        response = requests.get(url).text
        if "id does not exist" in response:
            print(oai_id)

#url = "http://"+server+"/OAI-PUB?verb="+verb[1]+"&identifier="+identifier_prefix
#print(url)
#list_without_metadata("opomenute_soubory.txt")

#test_id="104691" #obyčejný 
#test_id="103446"
#for r in search_records(test_id):
#    #print(str(ET.tostring(r)))
#    print(hui(r))