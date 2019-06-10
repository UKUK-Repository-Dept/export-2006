#!/usr/bin/python3
import requests
import json
import os

class Dspace:
    url = "https://gull.is.cuni.cz/rest"
    headers= { 
        "content-type": "application/json",
        }


    def __init__(self):
        try:
            self.user = os.environ['DSPACE_USER']
            self.passwd = os.environ['DSPACE_PASSWD']
        except KeyError as e:
            print("Please set DSPACE_USER and DSPACE_PASSWD variables.")
            raise e
        self.login = {
            'email': self.user,
            'password': self.passwd
        }
        response = requests.post(
            self.url+'/login', 
            headers=self.headers, 
            json=self.login
            )
        response.raise_for_status()
        self.token = response.text
        self.headers["rest-dspace-token"]= self.token
    
    def logout(self):
        response = requests.post(
            self.url+'/logout', 
            headers=self.headers, 
            )
        response.raise_for_status()
        self.token = response.text

    
    def list_bitstream(self):
        response = requests.get(
            self.url+'/items/5781/bitstreams', 
            headers=self.headers, 
            )
        for key in json.loads(response.text)[0].keys():
            print(key+":")
            for bitstream in json.loads(response.text):
                print(bitstream[key])
    
    def post_new_bitstream(self, item_id, filename, description=None):
        files = {
            'file': open("lorem-ipsum.pdf",'rb')
        }
        params={
            'name': filename,
            'description': description,
            'mineType': 'application/pdf',
        }
        requests.post(
            self.url+'/items/'+str(item_id)+'/bitstreams/',
            headers=self.headers,
            files=files,
            verify=False,
            params=params,
        )
    
    def delete_bitstream(self,delete):
        for d in delete:
            requests.delete(
                self.url+'/items/5781/bitstreams/'+str(d),
                headers=self.headers,
                )

    def handle(self, handle):
        response = requests.get(
            self.url+'/handle/'+handle, 
            headers=self.headers, 
            )
        handle_json = json.loads(response.text)
        for key in handle_json.keys():
            print(key,handle_json[key])
    
    def new_item(self, collection_id, metadata, files):
        response = requests.post(
            self.url+'/collections/'+str(collection_id)+'/items', 
            headers=self.headers,
            #headers= { "content-type": "application/xml", "rest-dspace-token": self.token, },
            json=metadata, 
            ).text
        print("hui",response.text)
        for filename in files:
            self.post_new_bitstream(filename, filename)
    
    def hui(self):
        response = requests.get(
            #self.url+'/communities 
            #self.url+'/collections/94', 
            #self.url+'/items/5781', 
            #self.url+'/items/5781/metadata', 
            self.url+'/items/5781/bitstreams', 
            headers=self.headers, 
            )
        print("hui",response.text)


metadata = {"metadata":[ 
            { "key": "dc.contributor.author", "value": "LAST, FIRST" }, 
            { "key": "dc.creator", "value": "prvni" }, 
            { "key": "dc.creator", "value": "druhy" }, 
            { "key": "dc.description", "language": "pt_BR", "value": "DESCRICAO" }, 
            { "key": "dc.description.abstract", "language": "pt_BR", "value": "ABSTRACT" }, 
            { "key": "dc.title", "language": "pt_BR", "value": "Se souborem" } 
            ]}
ds = Dspace()
#ds.handle("123456789/23900")
ds.new_item(273,metadata,["lorem-ipsum.pdf"])
#ds.hui()
#ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
#ds.delete_bitstream([6654,6655])
#ds.list_bitstream()
ds.logout()
