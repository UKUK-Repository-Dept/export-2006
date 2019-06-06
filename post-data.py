#!/usr/bin/python3
import requests
import json
import os

class Dspace:
    url = "https://gull.is.cuni.cz/rest"
    headers= { "content-type": "application/json"}

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
        response = requests.post(
            self.url+'/items/'+str(item_id)+'/bitstreams/',
            headers=self.headers,
            files=files,
            verify=False,
            params=params,
        )
    
    def delete_bitstream(self,delete):
        for d in delete:
            response = requests.delete(
                self.url+'/items/5781/bitstreams/'+str(d),
                headers=self.headers,
                )


ds = Dspace()
#ds.hui()
#ds.post_new_bitstream(5781,"lorem-ipsum.pdf")
ds.delete_bitstream([6654,6655])
ds.list_bitstream()
ds.logout()
