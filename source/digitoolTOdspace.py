#!/usr/bin/python3
import os
import click
from digitoolOAI import Digitool
from dspace import Dspace

@click.command()
@click.option('--dspace_admin_username', prompt='email', help='Dspace admin email')
@click.option('--dspace_admin_passwd', prompt='passwd', help='Dspace admin passwd')

def run(dspace_admin_passwd, dspace_admin_username):
    click.echo('Hello word')
    dt = Digitool("oai_kval") 
    #dt.download_list()
    ds = Dspace(dspace_admin_username,dspace_admin_passwd)
    #ds.new_item(273,metadata,["lorem-ipsum.pdf"])
  #  ds.logout()


if __name__ == '__main__':
    run()
