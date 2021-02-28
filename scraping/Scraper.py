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

test_player_orm()