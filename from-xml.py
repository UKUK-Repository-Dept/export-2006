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

def get_filenames(dirname,filename):
    tree = ET.parse(dirname+'/'+filename)
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
                #print("children"+pid,relation_type,dirname,filename)
    for record in subrecords:
        yield from get_filenames(dirname,record+".xml")

def print_childs(dirname,filename):
    try:
        tree = ET.parse(dirname+"/"+filename)
    except:
        raise
    root = tree.getroot()
    for relations in root.findall("./*relations"):
        for relation in relations:
            relation_type = relation.find('type').text
            if relation_type == "include":
                pid = relation.find('pid').text
                print(pid)

def print_all_child(dirname):
    for filename in os.listdir(dirname):
        print_childs(dirname,filename)

def check_mentions(dirname,filename):
    dt_id = filename.split("_")[0]
    return filename in get_filenames(dirname,dt_id+".xml")

def check_all_mentions(dirname,filename):
    for row in open(filename,"r"):
        if not check_mentions(dirname,row[:-1]):
            print(row[:-1])

def print_special(dirname,filename,pattern):
    #print("debug"+filename)
    for pdf in get_filenames(dirname,filename):
        if pattern in pdf:
            1+1
            #print(filename)
        
def print_all_special(dirname,pattern):
    for filename in os.listdir(dirname):
        try:
            print_special(dirname,filename,pattern)
        except:
            print(filename)

def print_label(dirname,filename):
    try:
        tree = ET.parse(dirname+"/"+filename)
    except:
        raise
    root = tree.getroot()
    label = tag(tag(tag(root,"digital_entity"),"control"),"label")
    note = tag(tag(tag(root,"digital_entity"),"control"),"note")
    ingest = tag(tag(tag(root,"digital_entity"),"control"),"ingest_name")
    if None == ingest.text:
        if None == note.text:
            print(filename, label.text, note.text)
            pass
        elif "MFF" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "FF" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "PF" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "FTVS" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "2LF" in note.text or "LF2" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "etf" in note.text or "ETF" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "HTF" in note.text:
            #print(filename, label.text, note.text)
            pass
        elif "FSV" in note.text:
            #print(filename, label.text, note.text)
            pass
        else:
            #print(filename, label.text, note.text)
            pass
        pass
    elif "ksp" in ingest.text:
        #print(filename, label.text, ingest.text)
        pass
    elif "psy" in ingest.text: 
        #print(filename, label.text, ingest.text)
        pass
    elif "mff" in ingest.text:
        #print(filename, label.text, ingest.text)
        pass
    elif "uisk" in ingest.text:
        #print(filename, label.text, ingest.text)
        pass
    elif "Dousova" in ingest.text:
        #print(filename, label.text, ingest.text)
        pass
    elif "12345" in ingest.text:
        #print(filename, label.text, ingest.text)
        pass
    else:
        #print(filename, label.text, ingest.text, note.text)
        pass 

def print_all_label(dirname,filename):
    for row in open(filename,"r"):
        oai_id = row.split("_")[0]
        print_label(dirname,oai_id+".xml")

#print_label("3.5.2019/digital_entities","103446.xml","label")
print_all_label("28.5.2019/digital_entities","opomenute_soubory.txt")
#print_special("3.5.2019/digital_entities",127578.xml","posu")
#print_special("3.5.2019/digital_entities","55070.xml","posu")
#print_all_special("3.5.2019/digital_entities","posu")

#print(check_mentions("100132_Huml_etf_dis.pdf"))
#print(check_all_mentions("3.5.2019/ls_streams.txt"))
#print_childs("67905.xml")
#print_all_child('28.5.2019/digital_entities')