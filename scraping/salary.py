from scraping.Page import Page
from db.models import salary

do_not_scrape = ['id', 'metadata', 'player_id', 'player_relationship', 'team_season_id', 'team_season_relationship', 'year']

class PlayerSalary(Page, salary):

    def __init__(self, year, team):
        self.year = year
        self.team = team

    def ping(self, row):
        salary = row.select_one('[data-stat=salary]').text
        if salary == '':
            return
        name = row.select_one('[data-stat=player]').text
        url = row.select_one('[data-stat=player] a').attrs['href']
        name = name.replace('*', '')
        name = name.replace('+', '')
        salary = salary.replace('$', '')
        salary = salary.replace(',', '')
        av = row.select_one('[data-stat=av]').text
        
        self.salary = salary
        self.player_url = url
        self.av = av
        self.name = name


class PlayerSalaryIndex(Page):
    def __init__(self, year, team):
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
            player_salary = PlayerSalary(self.year, self.team)
            player_salary.ping(row)
            salaries.append(player_salary)

        return salaries
    



        