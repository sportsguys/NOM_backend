import pywebcopy
from pywebcopy.parsers import MultiParser
from scraping.Page import Page
from db.models import salary
from pywebcopy import save_webpage
from scraping.team_index import TeamSeason
from pywebcopy import save_webpage, WebPage, config
import os
import requests as r
from bs4 import BeautifulSoup

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


current_dir = os.path.dirname(os.path.realpath(__file__))



class PlayerSalary(salary):

    def __init__(self):
        pass

#Use this class to loop through all of the teams different pages and years to obtain a tuple of the values that need to be inserted using the ORM.
#The URL passed to this class should be structured 'https://www.pro-football-reference.com/teams/atl/2015_roster.htm' with the team and the year changing.
class PlayerSalaryIndex(Page):
    def __init__(self, year, team):
        self.year = year
        self.team = team
        self.base_url = 'https://www.pro-football-reference.com/teams/'
        self.url = self.base_url + team + '/' + str(year) + '_roster.htm'
    
    def download_page(self):
        download_args = {
            'project_folder': current_dir,
            'project_name': 'rosters',
            'over_write': True,
            'bypass_robots': True,
            'load_css': False,
            'load_images': False
        }
        try:
            with time_limit(10):
                save_webpage(self.url, **download_args)
        except TimeoutException as e:
            print('timedout')


def download_rosters(session):
    base_url = 'www.pro-football-reference.com/teams/'
    team_seasons = session.query(TeamSeason).all()
    for team_season in team_seasons:
        if int(team_season.year_id) < 2015:
            continue
        team_dir = current_dir + '/rosters/' + base_url + team_season.team_url
        if not os.path.exists(team_dir):
            os.makedirs(team_dir)
        downloaded = False
        for filename in os.listdir(team_dir):
            if filename.endswith(str(team_season.year_id)+'_roster.htm'):
                downloaded = True
                continue
        if downloaded:
            continue
        psi = PlayerSalaryIndex(team_season.year_id, team_season.team_url)
        psi.download_page()


"""
    def scrape_salaries(self):
        salaries_list = []
        for row in self.salaries.contents:
            #Here is where I implement the logic for scraping the salaries off the page and making them into a tuple.
        return salaries_list
"""


