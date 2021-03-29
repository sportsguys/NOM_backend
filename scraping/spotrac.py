import requests
from bs4 import BeautifulSoup
from db.models import cap_hit
headers = {
    # log into spotrac with a browser and copy the Cookie header for PHPSESSID
    'Cookie': 'PHPSESSID=mgv74cmrm33dccbin18ui1sm2jhiecfq'
}

class SpotracTeams():
    def __init__(self):
        self.url = 'https://www.spotrac.com/nfl'
        res = requests.get(self.url, headers=headers)
        self.document = BeautifulSoup(res.content, 'html.parser')

    def team_url_list(self):
        urls = []
        container = self.document.select_one('.teams .teamlist')
        for item in container.contents:
            if item == '\n':
                continue
            urls.append(item.select_one('a').attrs['href'])
        return urls


class CapPage():
    def __init__(self, url):
        self.url = url
        res = requests.get(self.url, headers=headers)
        self.document = BeautifulSoup(res.content, 'html.parser')

    def scrape_caps(self):
        caps = []
        cap_table = self.document.select_one('tbody')
        if cap_table is None:
            return
        for row in cap_table.contents:
            if row == '\n':
                continue
            salary_season = CapHit()
            salary_season.ping(row)
            caps.append(salary_season)
        return caps
            

class CapHit(cap_hit):
    def ping(self, row):
        cap_hit_titles = [
            'Cap Hit',
            'Cap Hit / Active Pup',
            'Cap Hit / Transition',
            'Cap Hit / Franchise',
            'Cap Hit / Player'
        ]
        for title in cap_hit_titles:
            cap_hit = row.select_one('[Title="{}"]'.format(title))
            if cap_hit is not None:
                cap_hit = cap_hit.text
                break
        cap_hit = self.replace_money_chars(cap_hit)
        try:
            self.hit = int(cap_hit)
        except ValueError as e:
            self.hit = 0
        self.name = row.select_one('a').text
        self.position = row.select_one('.center').text

    def replace_money_chars(self, cap_hit):
        cap_hit = cap_hit.replace('$', '')
        cap_hit = cap_hit.replace(' ', '')
        cap_hit = cap_hit.replace(',', '')
        return cap_hit