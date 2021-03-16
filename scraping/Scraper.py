from scraping.salary import *
from scraping.team_index import Team, TeamIndex, TeamSeason
from scraping.player import Player, switch
from scraping.player_index import PlayerIndex
import config, string
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


def test_player_season_orm(session):
    guys = session.query(Player).all()
    for guy in guys:
        if guy.position not in switch:
            continue
        seasons = guy.get_seasons()
        for season in seasons:
            try:
                season.team_season_id = session.query(team_season.id).filter(and_(
                    team_season.team_url == season.team, team_season.year_id == season.year_id)).one().id
            except:
                pass
        session.add_all(seasons)
        session.commit()

# currently the player index returns a list of tuples with the information to create players
# so the responsibility to create the list of actual player objects falls on this driver module
# which is fine
def test_player_orm(session):
    players_info = create_player_list()
    player_list = []
    for player in players_info:
        player_list.append(Player(*player))
    session.add_all(player_list)
    session.commit()

def test_team_orm(session):
    url = 'https://www.pro-football-reference.com/teams/'
    ti  = TeamIndex(url)
    team_list = ti.scrape_teams()
    teams = []
    for team_info in team_list:
        teams.append(Team(*team_info))
    session.add_all(teams)
    session.commit()
    
def test_team_season_orm(session):
    base_url = 'https://www.pro-football-reference.com/teams/'
    teams = session.query(Team).all()
    for team in teams:
        seasons = team.get_team_seasons(2000)
        session.add_all(seasons)
        session.commit()
     
def test_salary_orm(session):
    team_seasons = session.query(TeamSeason).all()
    salaries = []
    salaryOs = []
    for team_season in team_seasons:
        if team_season.year_id >= 2015:
            si = PlayerSalaryIndex(team_season.year_id,team_season.team_url)
            salaries.extend(si.scrape_salaries())
    for salary in salaries:
        salaryOs.append(PlayerSalary(*salary))
    session.add_all(salaryOs)
    session.commit()

def populate():
    engine = connect_db(config.dev.DB_URI)
    init_db(engine)
    Session = sessionmaker(bind=engine, autoflush=True)
    session = Session()
    test_team_orm(session)
    test_team_season_orm(session)
    test_player_orm(session)
    test_player_season_orm(session)
    test_salary_orm(session)
    session.close()

populate()

