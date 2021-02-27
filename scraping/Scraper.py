from scraping.positions import *
from scraping.player_index import PlayerIndex
import string, config
from db.db import connect_db, init_db
from sqlalchemy.orm import sessionmaker, Session

#Create a list, probably a CSV of the players names. Find a pattern in the URL and manipulate that here. Can read through a txt file with all URL and then perform async operation on that players stats.
##while("file isn't empty"): while this loop runs keep obtaining URL and making a Page object with URL.
# url = "https://www.pro-football-reference.com/players/S/SharSh00.htm"
def create_player_list():
    letters = list(string.ascii_uppercase)
    base_url = 'https://www.pro-football-reference.com/players/'
    players = []
    for letter in letters:
        url = base_url + letter
        idx = PlayerIndex(url)
        players.append(idx.scrape_players())
    return players

#create_player_list()
brett = QB('https://www.pro-football-reference.com/players/F/FavrBr00.htm')
brett.ping()

def test_orm():
    engine = connect_db(config.dev.DB_URI)
    init_db(engine)

    brett = QB('https://www.pro-football-reference.com/players/F/FavrBr00.htm')
    brett.ping()
    clyde = RB('https://www.pro-football-reference.com/players/E/EdwaCl00.htm')
    clyde.ping()
    jerry = WR('https://www.pro-football-reference.com/players/R/RiceJe00.htm')
    jerry.ping()
    skip = TE('https://www.pro-football-reference.com/players/S/SharSh00.htm')

    Session = sessionmaker(bind = engine)
    session = Session()
    brett.name = 'brett'
    clyde.name = 'clyde'
    jerry.name = 'jerry'
    session.add_all([
        brett, clyde, jerry
    ])
    session.commit()

