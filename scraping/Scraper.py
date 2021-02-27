from scraping.positions import *
from scraping.player_index import PlayerIndex
import string
from db.db import init_db

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

init_db()

brett = QB('https://www.pro-football-reference.com/players/F/FavrBr00.htm')
clyde = RB('https://www.pro-football-reference.com/players/E/EdwaCl00.htm')
jerry = WR('https://www.pro-football-reference.com/players/R/RiceJe00.htm')
skip = TE('https://www.pro-football-reference.com/players/S/SharSh00.htm')

