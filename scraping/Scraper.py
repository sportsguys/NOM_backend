from scraping.spotrac import CapPage, SpotracTeams
from scraping.salary import PlayerSalary, PlayerSalaryIndex
from scraping.team_index import Team, TeamIndex, TeamSeason
from scraping.player import player_season_table_switch, Player
from scraping.player_index import PlayerIndex
import config, string
from db.db import connect_db, init_db
from sqlalchemy.orm import sessionmaker
from db.models import team_season, player_season, player
from sqlalchemy import and_, select

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
        if guy.position not in player_season_table_switch:
            continue

        seasons, statlines = guy.get_seasons()
        
        for i, season in enumerate(seasons):
            try:
                season.team_season_id = session.query(team_season.id).filter(and_(
                    team_season.team_url == season.team, team_season.year_id == season.year_id)).one().id    
            except Exception as e:
                print(e)
                pass
        session.add_all(seasons)
        session.commit()
        for i, statline in enumerate(statlines):
            try:
                statline.player_season_id = session.query(player_season).filter(and_(
                    player_season.team_season_id == seasons[i].team_season_id, player_season.player_id == statline.player_id)).one().id

                statline.team_season_id = session.query(team_season.id).filter(and_(
                    team_season.team_url == seasons[i].team, team_season.year_id == seasons[i].year_id)).one().id    
            except Exception as e:
                print(e)
                pass
        session.add_all(statlines)
        session.commit()

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
    teams = session.query(Team).all()
    for team in teams:
        seasons = team.get_team_seasons(2000)
        session.add_all(seasons)
        session.commit()
     
def test_salary_orm(session):
    team_seasons = session.query(TeamSeason).all()
    salaries = []
    for team_season in team_seasons:
        if team_season.year_id >= 2015:
            si = PlayerSalaryIndex(team_season.year_id,team_season.team_url)
            salaries.extend(si.scrape_salaries())
    session.add_all(salaries)
    session.commit()

def spotrac_salaries(session):
    cap_hits = []
    teams = session.query(Team.team_name).all()
    spotrac_teams_page = SpotracTeams()
    spotrac_team_urls = spotrac_teams_page.team_url_list()
    for idx, team_url in enumerate(spotrac_team_urls):
        for year in range(2011,2021):
            cap_index_url = team_url + str(year)
            cap_index = CapPage(cap_index_url)
            team_season_cap_hits = cap_index.scrape_caps()
            if team_season_cap_hits is None:
                continue
            for cap_hit in team_season_cap_hits:
                res = session.execute(select(player_season.id).join_from(
                    player_season, player).filter(
                        player.name == cap_hit.name).filter(
                            player_season.year_id == year)).all()
                if res:
                    try:
                        cap_hit.team_season_id = session.query(team_season).filter(and_(
                            team_season.team_url == session.query(Team.url).filter(
                                Team.team_name == teams[idx].team_name), 
                            team_season.year_id == year)
                        ).all()[0].id
                        cap_hit.player_season_id = res[0].id
                        cap_hits.append(cap_hit)
                    except Exception as e:
                        print(e)
                        continue
    session.add_all(cap_hits)
    session.commit()

def populate():
    engine = connect_db(config.dev.DB_URI)
    init_db(engine)
    Session = sessionmaker(bind=engine, autoflush=True)
    session = Session()
    #test_team_orm(session)
    #test_team_season_orm(session)
    #test_player_orm(session)
    #test_player_season_orm(session)
    #test_salary_orm(session)
    #spotrac_salaries(session)
    session.close()

populate()

