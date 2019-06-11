#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace


@click.group()
def cli():
    pass

@cli.command()
@click.option('--label', prompt='label', type=click.Choice(['ingest','note']), help='Choose label to categorize')
def categorize(label):
    def forgot_attachements(oai_attachements, xml_attachements_list):
        for row in open(xml_attachements_list,"r"):
            if not row[:-1] in oai_attachements:
                yield row[:-1]
    
    dt = Digitool("oai_kval") 
    dtx = DigitoolXML("28.5.2019",skip_missing=True)
    dt.download_list()
    dt.gather_attachements(dtx)

    forgot = list(forgot_attachements(dt.attachements,"28.5.2019/ls_streams.txt"))

    ingests = ["ksp", "mff", "psy", "Dousova", "uisk", "Hubl", "smes", "nadm_velikost", "12345"] 
    notes = [["HTF"],["FFUk","FF","FF UK","FFUK"],["etf","ETF"],["MFF"],["PF"],["FTVS"],["2LF","LF2","2LF -"],["FSV","FSV IMS","FSV_IKSZ","FSV ISS","FSV IPS"],["FHS"],["3LF"]]
    
    category = dtx.categorize_ingest(forgot,ingests)
    if label == 'note':
        category = dtx.categorize_note(category['None'],notes)
    
    sum = 0
    for tag, list_id in category.items():
        sum += len(list_id)
        print(tag,len(list_id))
    print("celkem",sum)


metadata = {"metadata":[ 
            { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
            { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
            { "key": "dc.title", "language": "pt_BR", "value": "Od jinud" } 
            ]}


@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
def run(dspace_admin_passwd, dspace_admin_username):
    dt = Digitool("oai_kval") 
    dt.download_list()
    #tree = ET.ElementTree(dt.list[0])
    #tree.write(open('test.xml','wb'))
    #print(len(dt.list))
    #print(list(dt.get_attachement(104691))) #obyčejný 
    #print(list(dt.get_attachement(20659))) 
    dt.gather_attachements()
    #dt.print_attachements()
    #forgot = list(forgot_attachements(dt.attachements,"28.5.2019/ls_streams.txt"))
    print(dt.attachements[0:10])

    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    #ds.handle("123456789/23900")
    #ds.new_item(273,metadata,["lorem-ipsum.pdf"])
    #ds.delete_all_item(273)
    #ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
    #ds.delete_bitstream([6654,6655])
    #ds.list_bitstream()
    ds.logout()

if __name__ == '__main__':
    #run()
    cli()
