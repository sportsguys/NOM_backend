from scraping.player import Player
from scraping.player_index import PlayerIndex
import string, config
from db.db import connect_db, init_db
from sqlalchemy.orm import sessionmaker

def create_player_list():
    letters = list(string.ascii_uppercase)
    base_url = 'https://www.pro-football-reference.com/players/'
    players = []
    for letter in letters:
        url = base_url + letter
        idx = PlayerIndex(url)
        players.extend(idx.scrape_players())
    return players

def test_season_orm():
    engine = connect_db(config.dev.DB_URI)
    init_db(engine)
    Session = sessionmaker(bind = engine)
    session = Session()
    guys = session.query(Player).all() # this grabs Player objects defined in player.py
    session.close()
    for guy in guys:
        session = Session() # close and remake to prevent bloating to 15GB of memory
        # create a list of seasons as defined in positions.py
        seasons = guy.get_seasons()
        session.add_all(seasons)
        session.commit()
        session.close()
# https://media1.tenor.com/images/21e759c7b8f0a2e7b034135b11157351/tenor.gif?itemid=15435775
# ^ you on pro football reference

test_season_orm()

# currently the player index returns a list of tuples with the information to create players
# so the responsibility to create the list of actual player objects falls on this driver module
# which is fine
def test_player_orm():
    players_info = create_player_list()
    player_list = []
    for player in players_info:
        player_list.append(Player(*player))
    engine = connect_db(config.dev.DB_URI)
    # create tables if not present
    init_db(engine) 
    Session = sessionmaker(bind = engine)
    session = Session()
    session.add_all(player_list)
    session.commit()
    session.close()

