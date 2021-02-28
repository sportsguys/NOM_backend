from scraping.positions import QB, WR, RB
from scraping.Page import Page
from db.models import player

class Player(Page, player):
    def __init__(self, name:str, url:str, position:str):
        self.name = name
        self.position = position
        self.url = url

    def get_seasons(self): 
        self.load_page(self.url)
        table_rows = self.bs.select_one('table tbody').contents
        seasons = []
        for row in table_rows:
            if row != '\n':
                season = switch[self.position](self.name)
                season.ping(row)
                seasons.append(season)
        return seasons

# module level variable only needs to be initialized once        
switch = {  
    'QB': QB,
    'WR': WR,
    'TE': WR,
    'RB': RB
}