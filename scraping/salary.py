import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from scraping.Page import *
from db.models import salary
from sqlalchemy.orm import sessionmaker
from pywebcopy import save_webpage


class PlayerSalary(salary):

    def __init__(self, name:str, team:str, year:int, salary:int):
        self.name = name
        self.team = team
        self.year = year
        self.salary = salary


#Use this class to loop through all of the teams different pages and years to obtain a tuple of the values that need to be inserted using the ORM.
#The URL passed to this class should be structured 'https://www.pro-football-reference.com/teams/atl/2015_roster.htm' with the team and the year changing.
class PlayerSalaryIndex(LocalPage):
    def __init__(self, url):
        if url:
            save_wepage(url, os.path.realpath(__file__))
            self.load_page(file)
            
"""
    def scrape_salaries(self):
        salaries_list = []
        for row in self.salaries.contents:
            #Here is where I implement the logic for scraping the salaries off the page and making them into a tuple.
        return salaries_list
"""

class TeamIndex(Page):
    def __init__(self, url=None):
        if url:
            self.load_page(url)
            self.teams = self.bs.select_one('#teams_active tbody')

    def scrape_teams(self):
        """ return list of PFR-relative team tuples containing name and url"""
        team_list = []
        for row in self.teams.contents:
            if row == '\n':
                continue
            try:
                url = row.contents[0].contents[0].attrs['href'].split('/')[2]
                team_name = row.contents[0].text
            except:
                continue
            team_list.append((team_name, url))

        return team_list

def test_salary_orm():
    team_tuples = TeamIndex("https://www.pro-football-reference.com/teams/").scrape_teams()
    #This allows us to go to all the team pages and checkout their rosters to get all the salary data for every team.
    for pair in team_tuples:
        base_year = '2015'
        current_year = '2020'
        while(int(base_year) <= int(current_year)):
            url = "https://www.pro-football-reference.com/teams/" + pair[1] + "/" + base_year + "_roster.htm"
            si = PlayerSalaryIndex(url)
            salary_list = si.scrape_salaries()
            salaries = []
            for salary in salary_list:
                salaries.append(PlayerSalary(*salary))
            base_year = str(int(base_year) + 1)
        engine = connect_db(config.dev.DB_URI)
        init_db(engine)
        Session = sessionmaker(bind = engine)
        session = Session()
        session.add_all(salary_list)
        session.commit()
        session.close()

test_salary_orm()
        