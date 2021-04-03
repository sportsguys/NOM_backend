import copy
import config
from db.db import connect_db, get_engine
from db.models import *
from sqlalchemy import and_
from sqlalchemy.orm.session import sessionmaker
from server.roster.roster_data import position_map
from scraping.player import switch
import numpy as np


class ValueDataLoader():
    def __init__(self):
        #engine = get_engine()
        engine = connect_db(config.dev.DB_URI)
        Session = sessionmaker(bind=engine, autoflush=True)
        self.sess = Session()

    def get_vectors(self, objlist):
        rows = []
        non_dims = ['age', 'id', 'player_id', 'team_season_id', 'year_id', 'team', 'av', 'g', 'gs']
        for item in objlist:
            item = copy.copy(item)
            [item.__dict__.pop(key, None) for key in non_dims]
            rows.append(list(item.__dict__.values())[1:-2]) #slice instance state and relationship objects
        return rows

    def batch_player_seasons(self, poss: str, start, end):
        pos = switch[poss.upper()]
        seasons = self.sess.query(pos).filter(and_(
            pos.year_id >= start, pos.year_id <= end)).join(
            pos.player_relationship).filter_by(position=poss.upper())

        return seasons.all()

    def label_offense_seasons(self, seasons):
        labels = []
        for season in seasons:
            points = self.sess.query(team_season).filter(
                team_season.id == season.team_season_id
            ).all()
            try:
                points = points[0].points
                # currently for qb tinkering
                label = points
            except:
                label = -1
            labels.append(label)
        return labels

    def one_player_season(self, poss: str, name, year):
        pos = switch[poss.upper()]
        season = self.sess.query(pos).filter(
            pos.year_id == year).join(
                pos.player_relationship).filter_by(name=name)
        season = season.all()
        return season[0]

    def minmax_norm(self, dataset):
        return ((dataset - np.min(dataset, axis=0)) / (np.max(dataset, axis=0) - np.min(dataset, axis=0)))

    def zscore_norm(self, dataset):
        return (dataset - np.mean(dataset, axis=0)) / np.std(dataset, axis=0)

    def create_dataset(self, seasons, role):
        labels = []
        data = []
        good_seasons = []
        for season in seasons:
            data_vec = self.get_vectors([season])[0]
            if -1 in data_vec:
                continue
            if role == 'offense':
                label = self.label_offense_seasons([season])[0]
            elif role == 'defense':
                #label = self.label_defense_seasons([season])[0]
                pass
            if label == -1:
                continue
            data.append(data_vec)
            labels.append(label)
            good_seasons.append(season)
        return good_seasons, data, labels