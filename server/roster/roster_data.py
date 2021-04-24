import config
from db.db import connect_db, get_session
from db.models import cap_hit, team, team_season, player_season, score
from sqlalchemy import and_, select
from sqlalchemy.orm.session import sessionmaker
from db.constants import position_map

class RosterDataLoader():
    def __init__(self):
        #self.db = get_session()
        engine = connect_db(config.dev.DB_URI)
        Session = sessionmaker(bind=engine, autoflush=True)
        self.db = Session()

    def team_spending(self, team_name, year):
        cap_hits = self.db.query(cap_hit).filter(
            cap_hit.team_season_id == self.db.query(team_season.id).filter(and_(
                team_season.year_id == year, 
                team_season.team_url == self.db.query(team.url).filter(
                    team.team_name == team_name
                )
            ))
        ).all()
        distribution = {}
        for hit in cap_hits:
            try:
                distribution[hit.position] += hit.hit
            except KeyError:
                distribution[hit.position] = hit.hit
        return distribution

    def positional_spending(self, team_name, year):
        spending = {}
        team_dist = self.team_spending(team_name, year)
        for pos, val in team_dist.items():
            for cat, members in position_map.items():
                if pos in members:
                    try:
                        spending[cat] += val
                    except KeyError:
                        spending[cat] = val
        return spending

    def check_allocation(self, team_name, year):
        sid_query = (select(team_season.id).filter(and_(team_season.team_url == team_name, team_season.year_id == year)))
        season_id = self.db.execute(sid_query).one()._data[0]
        stmt = (
            select(cap_hit.name, cap_hit.position, cap_hit.hit, score.value).
                filter(and_(cap_hit.team_season_id == season_id, score.player_season_id == cap_hit.player_season_id))
        )
        rows = self.db.execute(stmt).all()
        sal_totals = {}
        score_totals = {}
        for row in rows:
            for key, val in position_map.items():
                if row[1] in val:
                    try:
                        sal_totals[key] += row[2]
                        score_totals[key] += row[3]
                        break
                    except KeyError:
                        sal_totals[key] = row[2]
                        score_totals[key] = row[3]
                        break

        return sal_totals, score_totals

    

