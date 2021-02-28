from db.models import qb, wr, rb, defense

do_not_scrape = ['id', 'metadata', 'player_id', 'player_relationship']

class Position():

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
                    value = 0
                setattr(self, attr, value)

""" These all look the same but theyre not """
class QB(qb, Position):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

    def ping(self, row):
        self.get_all_row_data(row)
class WR(wr, Position):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

    def ping(self, row):
        self.get_all_row_data(row)
class RB(rb, Position):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

    def ping(self, row):
        self.get_all_row_data(row)

class Defense(defense, Position):
    def __init__(self, player_id):
        self.player_id = player_id # the foreign key to players

    def ping(self, row):
        self.get_all_row_data(row)

