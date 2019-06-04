#!/usr/bin/python3
import requests
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
        print(response.text)
    
    def logout(self):
        response = requests.post(
            self.url+'/logout', 
            headers=self.headers, 
            )
        response.raise_for_status()
        self.token = response.text

    def hui(self):
        pass


ds = Dspace()
ds.logout()