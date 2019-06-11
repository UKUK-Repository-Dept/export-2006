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

    def get_oai_id(self, record):
        header=tag(record,"header")
        identifier=tag(header,"identifier").text
        return identifier.split(":")[-1]
    
    def get_metadata(self, record, metadata_type):
        metadata=tag(record,"metadata")
        metadata=tag(metadata,metadata_type)
        for child in metadata:
            yield (child.tag, child.text)

