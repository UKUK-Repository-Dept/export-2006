#!/usr/bin/python3
import os
import requests, json
import xml.etree.ElementTree as ET

def tag(root,tag):
    try:
        subtree=list(r for r in root if tag in r.tag)[0]
    except:
        raise Exception("No tag {}".format(tag))
    return subtree

class DigitoolXML:
    def __init__(self, dirname, skip_missing = False):
        self.dirname = dirname
        self.xml_dirname = dirname+'/digital_entities'
        self.skip_missing = skip_missing

    def get_attachements(self, filename):
        if self.skip_missing:
            try:
                tree = ET.parse(self.xml_dirname+'/'+filename)
            except:
                return
        else:
            tree = ET.parse(self.xml_dirname+'/'+filename)

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
            yield from self.get_attachements(record+".xml")


    def get_category(self, filename):
        tree = ET.parse(self.xml_dirname+"/"+filename)
        root = tree.getroot()
        label = tag(tag(tag(root,"digital_entity"),"control"),"label")
        note = tag(tag(tag(root,"digital_entity"),"control"),"note")
        ingest = tag(tag(tag(root,"digital_entity"),"control"),"ingest_name")
        return (label.text,ingest.text,note.text)

    def categorize_ingest(self, attachements, ingest_list):
        category = {}
        for tag in ingest_list:
            category[tag] = []
            for attachement in attachements:
                oai_id = attachement.split("_")[0]
                label, ingest, note = self.get_category(oai_id+".xml")
                if ingest != None and tag in ingest:
                    category[tag].append(attachement)
        category['other'] = []
        category['None'] = []
        for attachement in attachements:
            oai_id = attachement.split("_")[0]
            label, ingest, note = self.get_category(oai_id+".xml")
            if ingest == None:
                category['None'].append(attachement)
            else:
                other = True
                for tag in ingest_list:
                    if tag in ingest:
                        other = False
                if other:
                    category['other'].append(attachement)
        return category
    
    def categorize_note(self, attachements, note_list):
        category = {}
        for tags in note_list:
            category[str(tags)] = []
            for attachement in attachements:
                oai_id = attachement.split("_")[0]
                label, ingest, note = self.get_category(oai_id+".xml")
                if note != None and note in tags:
                    category[str(tags)].append(attachement)
        category['other'] = []
        category['None'] = []
        for attachement in attachements:
            oai_id = attachement.split("_")[0]
            label, ingest, note = self.get_category(oai_id+".xml")
            if note == None:
                category['None'].append(attachement)
            else:
                other = True
                for tags in note_list:
                    for tag in tags:
                        if tag == note:
                            other = False
                if other:
                    category['other'].append(attachement)
        return category

def print_all_label(xml_dirname,filename):
    def has_category(oai_id,category,type):
        if type=="note":
            if note != None:
                return note in category
            else:
                return False
        if type=="note-other":
            if note == None:
                return False
            for tags in category:
                for tag in tags:
                    if tag == note:
                        return False
            return True
        if type=="note-None":
            if note == None:
                return True
            return False
    
#    print("\nIngesty:")
    ingests = ["ksp", "mff", "psy", "Dousova", "uisk", "Dodatky", "Hubl", "smes", "nadm_velikost", "12345"] 
    category = {}
    for tag in ingests:
        category[tag] = [ row[:-1] for row in open(filename,"r") \
            if has_category(row[:-1],tag,"ingest") ]
    category["jiná"] = [ row[:-1] for row in open(filename,"r") \
        if has_category(row[:-1],ingests,"ingest-other") ]
    category["žádná"] = [ row[:-1] for row in open(filename,"r") \
        if has_category(row[:-1],None,"ingest-None") ]
    sum = 0
    for tag, list_id in category.items():
        sum += len(list_id)
        if len(list_id) < 100:
            print("\n",tag,len(list_id))
            for oai_id in list_id:
                label, ingest, note = get_category(xml_dirname,oai_id+".xml")
                print(oai_id, label, ingest, tag)

#    print("celkem",sum)
    
    #print("\nNote:")
    notes = [["HTF"],["FFUk","FF","FF UK","FFUK"],["etf","ETF"],["MFF"],["PF"],["FTVS"],["2LF","LF2","2LF -"],["FSV","FSV IMS","FSV_IKSZ","FSV ISS","FSV IPS"],["FHS"],["3LF"]]
    category = {}
    for tag in notes:
        category[str(tag)] = [ row[:-1] for row in open(filename,"r") \
            if has_category(row[:-1],tag,"note") ]
    category["jiná"] = [ row[:-1] for row in open(filename,"r") \
        if has_category(row[:-1],notes,"note-other") ]
    category["žádná"] = [ row[:-1] for row in open(filename,"r") \
        if has_category(row[:-1],None,"note-None") ]
    #sum = 0
    #for tag, list_id in category.items():
    #    sum += len(list_id)
    #    print(tag,len(list_id))
    #print("celkem",sum)

    #print(category["FF"])
    #print(len(set(category["MFF"]).intersection(set(category["FF"]))))
    for oai_id in category["žádná"]:
        label, ingest, note = get_category(xml_dirname,oai_id+".xml")
        #if label == None:
        #    print(oai_id)

#print_label("3.5.2019/digital_entities","103446.xml","label")
#print_all_label("28.5.2019/digital_entities","opomenute_soubory.txt")
#print_special("3.5.2019/digital_entities",127578.xml","posu")
#print_special("3.5.2019/digital_entities","55070.xml","posu")
#print_all_special("3.5.2019/digital_entities","posu")

#print(check_mentions("100132_Huml_etf_dis.pdf"))
#print(check_all_mentions("3.5.2019/ls_streams.txt"))
#print_childs("67905.xml")
#print_all_child('28.5.2019/digital_entities')
