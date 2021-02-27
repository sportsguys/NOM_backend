from abc import abstractclassmethod
import requests
import mysql.connector as msc
from bs4 import BeautifulSoup

class Page:

    def load_page(self, url):
        response = requests.get(url)
        self.bs = BeautifulSoup(response.text, 'html.parser')
        




    


