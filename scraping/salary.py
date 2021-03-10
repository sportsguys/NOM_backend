from scraping.Page import Page
from db.models import salary
from scraping.team_index import TeamSeason

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
        self.load_page(self.url)
        comment_parent = self.bs.select_one('#all_games_played_team')
        self.load_page(comment_parent.contents[4])
        self.tbody = self.bs.contents[0].contents[1].contents[0].contents[1].contents[7]


    def scrape_salaries(self):
        salaries_list = []
        for row in self.tbody:
            pass
            #Here is where I implement the logic for scraping the salaries off the page and making them into a tuple.
        return salaries_list


