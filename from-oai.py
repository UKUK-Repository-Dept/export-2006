#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET

server="dingo.ruk.cuni.cz:8881"
verb="ListRecords"
metadataPrefix="oai_dc"
oai_sets=["oai_kval","oai_kvalDC"]

def get_oai_metadata(oai_set):
    url = "http://"+server+"/OAI-PUB?verb="+verb+"&metadataPrefix="+metadataPrefix+"&set="+oai_set
    response = requests.get(url)
    print(url,response.text)

get_oai_metadata(oai_sets[0])
