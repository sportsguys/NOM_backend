import config
from db.db import connect_db, get_session
from db.models import cap_hit, team, team_season
from sqlalchemy import and_
from sqlalchemy.orm.session import sessionmaker

position_map = {
    'QB': ['QB', 'QB/TE'],
    'RB': ['RB', 'HB', 'FB'],
    'TE': ['TE'],
    'WR': ['WR'],
    'OL': ['G', 'T', 'LT', 'RT', 'C', 'RG', 'LG', 'OG', 'NT', 'OT', 'OL', 'G,T', 'C,G', 'G,C', 'T,G'],
    'DL': ['DT', 'DE', 'DL'],
    'LB': ['OLB', 'ILB', 'LB', 'EDGE'],
    'DB': ['CB', 'FS', 'S', 'SS', 'DB'],
    'K' : ['K', 'P', 'LS']
}


class RosterData():
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



