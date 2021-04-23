from db.models import qb, wr, rb, defense, kicker, player_season

do_not_scrape = ['id', 'metadata', 'player_id', 'player_relationship', 'player_season_id', 'player_season_relationship', 'team_season_id', 'team_season_relationship']

class RowScraper():

    def ping(self, row):
        self.get_all_row_data(row)
        try:
            self.team = row.select_one('[data-stat=team] a').attrs['href'].split('/')[2]
        except:
            pass

    def get_all_row_data(self, row):
        myattrs = dir(self.__class__.__bases__[0])
        for attr in myattrs:
            if not attr.startswith('__') and not attr.startswith('_') and attr not in do_not_scrape:
                try:
                    value = row.select_one('[data-stat={}]'.format(attr)).text
                    value = value.replace('*','')
                    value = value.replace('+','')
                    value = value.replace('%','')
                except Exception as e:
                    print(e)
                    value = 0 #for now. should add logging
                if not value and value != '0.0' and value != 0:
                    value = -1
                setattr(self, attr, value)

""" These all look the same, and pointless, but theyre not the same """

class PlayerSeason(player_season, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

class QB(qb, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players
      
class WR(wr, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

class RB(rb, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

class Defense(defense, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

class Kicker(kicker, RowScraper):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

