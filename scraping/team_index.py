from scraping.Page import Page
from db.models import team, team_season

do_not_scrape = ['id', 'metadata', 'team_url', 'team_relationship']

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

class TeamSeason(team_season):
    def __init__(self, team_url):
        self.team_url = team_url

    def get_all_row_data(self, row):
            myattrs = dir(self.__class__.__bases__[0])
            for attr in myattrs:
                if not attr.startswith('__') and not attr.startswith('_') and attr not in do_not_scrape:
                    try:
                        value = row.select_one('[data-stat={}]'.format(attr)).text
                        value = value.replace('*','')
                        value = value.replace('+','')
                    except:
                        value = 0 #for now. should add logging
                    if not value:
                        value = -1
                    setattr(self, attr, value)

    def ping(self, row):
        self.get_all_row_data(row)


class Team(Page, team):
    def __init__(self, name:str, url:str):
        self.team_name = name
        self.url = url

    def get_team_seasons(self, cutoff_year=None):
        self.load_page('https://www.pro-football-reference.com/teams/' + self.url)
        table_rows = self.bs.select_one('table tbody').contents
        seasons = []
        for row in table_rows:
            if row == '\n':
                continue
            try:
                if int(row.select_one('[data-stat=year_id]').text) < cutoff_year:
                    continue
            except: #the team pages have intermediate table headers
                continue
            team_season = TeamSeason(self.url)
            team_season.ping(row)
            seasons.append(team_season)
        return seasons
