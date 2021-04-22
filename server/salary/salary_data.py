import config
from db.db import connect_db, get_session
from db.models import cap_hit
from sqlalchemy import and_
from sqlalchemy.orm.session import sessionmaker
import pickle

class SalaryDataLoader():
    def __init__(self):
        #self.db = get_session()
        engine = connect_db(config.dev.DB_URI)
        Session = sessionmaker(bind=engine, autoflush=True)
        self.sess = Session()

    def get_salaries(self, scores: list, seasons: list):
        salaries = []
        good_seasons = []
        good_scores = []
        for i, season in enumerate(seasons):
            salary = self.sess.query(cap_hit).filter(and_(
                cap_hit.team_season_id == season.team_season_id,
                cap_hit.name == season.player_relationship.name
            )).all()
            try:
                salaries.append(salary[0].hit)
                good_seasons.append(season)
                good_scores.append(scores[i])
            except:
                continue

        return salaries, good_scores, good_seasons
