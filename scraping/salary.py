from scraping.Page import Page
from db.models import salary

do_not_scrape = ['id', 'metadata', 'player_id', 'player_relationship', 'team_season_id', 'team_season_relationship', 'year']

class PlayerSalary(Page, salary):

    def __init__(self, salary, yearVal, team, name, url):
        setattr(self, 'name', name)
        setattr(self, 'salary', salary)
        setattr(self, 'year', yearVal)
        setattr(self, 'team', team)
        setattr(self, 'player_url', url)


#Use this class to loop through all of the teams different pages and years to obtain a tuple of the values that need to be inserted using the ORM.
#The URL passed to this class should be structured 'https://www.pro-football-reference.com/teams/atl/2015_roster.htm' with the team and the year changing.


class PlayerSalaryIndex(Page):
    def __init__(self, year, team):
        if year >= 2015:
            self.year = year
            self.team = team
            self.base_url = 'https://www.pro-football-reference.com/teams/'
            self.url = self.base_url + team + '/' + str(year) + '_roster.htm'
            self.load_page(self.url)
            comment_parent = self.bs.select_one('#all_games_played_team')
            self.parse_html(comment_parent.contents[4])
            self.tbody = self.bs.contents[0].contents[1].contents[0].contents[1].contents[7]

    def scrape_salaries(self):
        salaries = []
        for row in self.tbody.contents:
            if row == '\n':
                continue
            salary = row.select_one('[data-stat=salary]').text
            name = row.select_one('[data-stat=player]').text
            url = row.select_one('[data-stat=player] a').attrs['href']
            name = name.replace('*', '')
            name = name.replace('+', '')
            if salary == '':
                 continue
            salary = salary.replace('$', '')
            salary = salary.replace(',', '')
            salaries.append((int(salary), self.year, self.team, name, url))
        return salaries
    



        