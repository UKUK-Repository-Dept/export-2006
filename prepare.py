#!/usr/bin/python3
import requests, json
import xml.etree.ElementTree as ET

# část první z dspace dostávám seznam digitool id

# https://gull.is.cuni.cz/rest/communities/
#community_id = "152" #puvodni import
#community_id = "154" #můj import
community_id = "155" #20.5

bare_url = "https://gull.is.cuni.cz/rest"

def get_collections_id(community_id):
    url = bare_url + "/communities/" + community_id + "/collections"
    response = requests.get(url)
    for collection in json.loads(response.text):
        yield collection["id"]

#collection_ids = get_collections_id(community_id)
#print(list(collection_ids))
#collection_ids = [242, 244] #puvodni
#collection_ids = [267, 266] #nove
collection_ids = [269] 

def get_items_id(collection_id):
    url = bare_url + "/collections/" + str(collection_id) + "/items"
    response = requests.get(url, params="limit=3000")
    for item in json.loads(response.text):
        yield item["id"]
#print(list(get_items_id(268)))

def get_item(item_id):
    url = bare_url + "/items/" + str(item_id) 
    response = requests.get(url)
    return json.loads(response.text)
#print(list(get_item(15070)))

def get_digitool_id(item_id):
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
#print(get_digitool_id(8418))

def prepare_xml_filename_list():
        # pro vytovoreni xml_filenames
        for i in range(len(collection_ids)):
                for item_id in get_items_id(collection_ids[i]):
                        print(get_digitool_id(item_id))
prepare_xml_filename_list()



# část druha z xml dostávám přílohy

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


def print_all_filenames(source_files):
    for xml_filename in open(source_files,"r"):
        filenames = get_filenames(xml_filename[:-5])
        for filename in filenames:
            print(filename)

#print(list(get_filenames(100452)))
#print_all_filenames("xml_filenames.txt")

#import os
# v opomenute_soubory.txt jsou ty z ls na gull export na ktere nevede cesta z dsace
# v opomenute_soubory1.txt jsou ty co jsou zminene jen ve svem xml
# v opomenute_soubory2.txt je zbytek
#for row in open("opomenute_soubory.txt","r"):
#     id = row.split("_")[0]
#     # žádné id není v xml_filenames.txt
#     grep = os.popen("grep "+str(id)+" -r digital_entities/ -l").read()
#     if len(grep.split("\n")) != 2:
#        print(row[:-1])
           

# debug a pomocné
def dspace_item_id_from_digitoll_interni_id(interni_id):
        # TODO zatim nefunkcni
        for i in range(len(collection_ids)):
                for item_id in get_items_id(collection_ids[i]):
                        if get_digitool_id == interni_id:
                                print(item_id, ": ", get_digitool_id(item_id))
