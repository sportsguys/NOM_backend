from scraping.team_index import Team, TeamIndex
from scraping.player import Player
from scraping.player_index import PlayerIndex
import string, config
from db.db import connect_db, init_db
from sqlalchemy.orm import sessionmaker
from db.models import team_season
from sqlalchemy import and_

def create_player_list():
    letters = list(string.ascii_uppercase)
    base_url = 'https://www.pro-football-reference.com/players/'
    players = []
    for letter in letters:
        url = base_url + letter
        idx = PlayerIndex(url)
        players.extend(idx.scrape_players())
    return players


def test_player_season_orm():
    engine = connect_db(config.dev.DB_URI)
    Session = sessionmaker(bind = engine, autoflush=True)
    session = Session()
    guys = session.query(Player).all()
    for guy in guys:
        seasons = guy.get_seasons()
        for season in seasons:
            season.team_season_id = session.query(team_season.id).filter(and_(
                team_season.team_url == season.team, team_season.year_id == season.year_id)).one().id
        session.add_all(seasons)
        session.commit()
    session.close()

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

def test_team_orm():
    url = 'https://www.pro-football-reference.com/teams/'
    ti  = TeamIndex(url)
    team_list = ti.scrape_teams()
    teams = []
    for team_info in team_list:
        teams.append(Team(*team_info))
    engine = connect_db(config.dev.DB_URI)
    Session = sessionmaker(bind = engine)
    session = Session()
    session.add_all(teams)
    session.commit()
    
def test_team_season_orm():
    base_url = 'https://www.pro-football-reference.com/teams/'
    engine = connect_db(config.dev.DB_URI)
    Session = sessionmaker(bind = engine)
    session = Session()
    teams = session.query(Team).all()
    session.close()
    for team in teams:
        session = Session()
        seasons = team.get_team_seasons(2000)
        session.add_all(seasons)
        session.commit()
        session.close()
     

engine = connect_db(config.dev.DB_URI)
init_db(engine)

#test_team_orm()
#test_team_season_orm()
#test_player_orm()
test_player_season_orm()
