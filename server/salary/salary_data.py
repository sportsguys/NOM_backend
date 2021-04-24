import config
from db.db import connect_db, get_session
from db.models import cap_hit, player_season, score, player
from db.constants import position_map
from sqlalchemy import and_, select
from sqlalchemy.orm.session import sessionmaker

class SalaryDataLoader():
    def __init__(self):
        #self.db = get_session()
        self.engine = connect_db(config.dev.DB_URI)

    def get_salaries(self, poss: str):
        for key, value in position_map.items():
            if poss.upper() in value:
                positions = value

        stmt = (
            select(cap_hit.hit, score.value, player_season.year_id, player_season.team_season_id).
                filter(cap_hit.player_season_id == score.player_season_id).
            join(score.player_relationship).filter(player.position.in_(positions)).
            join(score.player_season_relationship).filter(score.player_season_id == cap_hit.player_season_id)
        )
        with self.engine.begin() as conn:
            rows = conn.execute(stmt).all()
        if rows:
            salaries = list(list(zip(*rows))[0])
            scores = list(list(zip(*rows))[1])
            years = list(list(zip(*rows))[2])
            tsids = list(list(zip(*rows))[3])
        else:
            raise RuntimeError

        return salaries, scores, years, tsids
