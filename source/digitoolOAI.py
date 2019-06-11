#!/usr/bin/python3
import requests
import json
import xml.etree.ElementTree as ET
# http://www.openarchives.org/OAI/openarchivesprotocol.html

def tag(root,tag):
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class Digitool:
    server = "dingo.ruk.cuni.cz:8881"
    metadataPrefix = "oai_dc"
    identifierPrefix = "oai:DURCharlesUniPrague.cz:"
    xmlDirname = "28.5.2019/digital_entities/"

    def __init__(self,oai_set):
        self.oai_set = oai_set

    def download_list(self):
        url = ( "http://" + self.server + "/OAI-PUB?" +  
            "verb=ListRecords" + 
            "&metadataPrefix=" + self.metadataPrefix + 
            "&set=" + self.oai_set )
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
        self.list = list(recursion(url,None))
    
    def get_attachement(self, oai_id):
        try:
            tree = ET.parse(self.xmlDirname + str(oai_id) + ".xml")
        except:
            #ručně ověřeno tohle padá na náhledech co vypadaji jako děti
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
            yield from self.get_attachement(record)

    def get_oai_id(self, record):
        header=tag(record,"header")
        identifier=tag(header,"identifier").text
        return identifier.split(":")[-1]

    def gather_attachements(self):
        self.attachements = []
        for record in self.list:
            oai_id = self.get_oai_id(record)
            print(oai_id)
            self.attachements += list(self.get_attachement(oai_id))

    def print_attachements(self):
        for attachement in self.attachements:
            print(attachement)



#dt = Digitool("oai_kval") 
#dt.download_list()

#tree = ET.ElementTree(dt.list[0])
#tree.write(open('test.xml','wb'))
#print(len(dt.list))
#print(list(dt.get_attachement(104691))) #obyčejný 
#print(list(dt.get_attachement(20659))) 
#dt.gather_attachements()
#dt.print_attachements()
