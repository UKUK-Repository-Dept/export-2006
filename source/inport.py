#!/usr/bin/python3
from digitoolOAI import Digitool
import os

dt = Digitool("oai_kval") 
dt.download_list()

#tree = ET.ElementTree(dt.list[0])
#tree.write(open('test.xml','wb'))

print("hui")