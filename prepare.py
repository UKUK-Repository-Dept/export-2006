#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET


#collection_handle = "1233456789/4413" #dc
community_id = "152"
bare_url = "https://gull.is.cuni.cz/rest"

def get_collections_id(community_id):
    url = bare_url + "/communities/" + community_id + "/collections"
    response = requests.get(url)
    for collection in json.loads(response.text):
        yield collection["id"]

def get_items_id(collection_id):
    url = bare_url + "/collections/" + str(collection_id) + "/items"
    response = requests.get(url, params="limit=3000")
    for item in json.loads(response.text):
        yield item["id"]
    
def get_item(item_id):
    url = bare_url + "/items/" + str(item_id) 
    response = requests.get(url)
    return json.loads(response.text)

def get_interni_id(item_id):
    handle = get_item(item_id)['handle']
    url = "https://gull.is.cuni.cz/oai/request?verb=GetRecord&identifier=oai:dspace.cuni.cz:" \
          + handle + "&metadataPrefix=xoai"
    response = requests.get(url)
    match = "oai:DURCharlesUniPrague.cz:"
    ending = "</field>"
    for row in response.text.split("\n"):
        start = row.find(match)
        if start > 0:
            return row[start+len(match):-len(ending)]

def get_filenames(xml_filename):
    tree = ET.parse('digital_entities/'+xml_filename)
    root = tree.getroot()
    for stream_ref in root.findall("./*stream_ref"):
        filename = stream_ref.find('file_name').text
        yield filename



#collection_ids = get_collections_id(community_id)
collection_ids = [242, 244]
#print(list(get_items_id(collection_ids[0])))

#for item_id in get_items_id(collection_ids[0]):
#    xml_filename = str(get_interni_id(item_id)) + ".xml"
#    print(xml_filename)

for xml_filename in open("xml_filenames.txt","r"):
    filenames = get_filenames(xml_filename)
    for filename in filenames:
            if filename != None:
                    print(filename)