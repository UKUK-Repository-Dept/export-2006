#!/usr/bin/python3
from digitoolOAI import Digitool
from dspace import Dspace
import os

dt = Digitool("oai_kval") 
dt.download_list()

#tree = ET.ElementTree(dt.list[0])
#tree.write(open('test.xml','wb'))

print("hui")

metadata = {"metadata":[ 
            { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
            { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
            { "key": "dc.title", "language": "pt_BR", "value": "Od jinud" } 
            ]}
ds = Dspace()
#ds.handle("123456789/23900")
ds.new_item(273,metadata,["lorem-ipsum.pdf"])
#ds.hui()
#ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
#ds.delete_bitstream([6654,6655])
#ds.list_bitstream()
ds.logout()