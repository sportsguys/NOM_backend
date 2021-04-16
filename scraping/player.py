from scraping.player_seasons import QB, WR, RB, Defense, Kicker
from scraping.Page import Page
from db.models import player

class Player(Page, player):
    def __init__(self, name:str, url:str, position:str):
        self.name = name
        self.position = position
        self.url = url

    def get_seasons(self): 
        self.load_page('https://www.pro-football-reference.com' + self.url)
        table_rows = self.bs.select_one('table tbody').contents
        seasons = []
        for row in table_rows:
            if row == '\n':
                continue
            try:
                season = player_season_table_switch[self.position](self.id)
            except KeyError as e:
                print(e, 'position not recognized')
                continue
            season.ping(row)
            if int(season.year_id) < 2000:
                continue
            seasons.append(season)
        return seasons

# module level variable only needs to be initialized once 
player_season_table_switch = {  
    'QB': QB,
    'WR': WR,
    'TE': WR,
    'RB': RB,
    'CB': Defense,
    'DB': Defense,
    'OLB': Defense,
    'LB': Defense,
    'DL': Defense,
    'DE': Defense,
    'K' : Kicker,
    'HB': RB,
    'FB': RB,
    'DT': Defense,
    'ILB': Defense,
    'EDGE': Defense
}
