import requests
from bs4 import BeautifulSoup

class Page:

    def request_page(self, url):
        response = requests.get(url)
        self.bs = BeautifulSoup(response.text, "html.parser")

    def load_page(self, filename):
        with open(filename) as fp:
            self.bs = BeautifulSoup(fp, "html5lib")
        