#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from dspace import Dspace


if __name__ == '__main__':
    click.echo('Hello word')
    dt = Digitool("oai_kval") 
    #dt.download_list()
    ds = Dspace()
    #ds.new_item(273,metadata,["lorem-ipsum.pdf"])
    ds.logout()
