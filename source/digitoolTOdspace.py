#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from digitoolXML import DigitoolXML
from dspace import Dspace
from convertor import Convertor


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
    dtx = DigitoolXML("28.5.2019", skip_missing=True)
    dt.download_list()

    attachements = []
    for record in dt.list:
        oai_id = dt.get_oai_id(record)
        attachements += list(dtx.get_attachements(str(oai_id)+".xml"))


    forgot = list(forgot_attachements(attachements,"28.5.2019/ls_streams.txt"))

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


@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
def dspace(dspace_admin_passwd, dspace_admin_username):
    metadata = {"metadata":[ 
                { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
                { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
                { "key": "dc.title", "language": "pt_BR", "value": "Od jinud" } 
                ]}
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    #ds.handle("123456789/23900")
    #ds.new_item(273,metadata,["lorem-ipsum.pdf"])
    ds.delete_all_item(273)
    #ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
    #ds.delete_bitstream([6654,6655])
    #ds.list_bitstream()
    ds.logout()

@cli.command()
def descriptions():
    dt = Digitool("oai_kval") 
    dt.download_list()
    dtx = DigitoolXML("28.5.2019", skip_missing=True)
    c = Convertor()
    
    problems = []
    for record in dt.list:
        oai_id = dt.get_oai_id(record)
        attachements = list(dtx.get_attachements(oai_id+".xml",full=True))
        if len(attachements) == 0:
            #print(oai_id)
            continue
        descriptions = c.generate_description(attachements)
        if isinstance(descriptions, list):
            continue
#        print(attachements)
        print(descriptions)
#    print("problems",problems)


@cli.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')
@click.option('--test/--run', default=True, help='Test print or pushing on server')
#TODO --yes operator by byl lepši než test
def convert(dspace_admin_passwd, dspace_admin_username, test):
    dt = Digitool("oai_kval") 
    dt.download_list()
    #print(list(dt.get_attachement(104691))) #obyčejný 
    dtx = DigitoolXML("28.5.2019")
    c = Convertor()
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    
    problems = []
    for record in dt.list[0:10]:
        oai_id = dt.get_oai_id(record)
        original_metadata = list(dt.get_metadata(record,"dc"))
        converted_metadata = c.convert(original_metadata)
        attachements = list(dtx.get_attachements(oai_id+".xml"))
        if test:
            click.clear()
            for i in original_metadata:
                print(i)
            print()
            for i in converted_metadata['metadata']:
                print(i)
            print()
            print(attachements)
            if not click.confirm("Is converting OK?", default=True):
                problems.append(oai_id)
        else:
            ds.new_item(273,converted_metadata,[("lorem-ipsum.pdf","application/pdf","Dokument")])
    click.clear()
    print("problems",problems)
    ds.logout()

if __name__ == '__main__':
    cli()
