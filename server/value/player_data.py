import copy
import config
import numpy as np
from db.constants import position_map
from db.db import connect_db, get_engine
from db.models import *
from scraping.player import player_season_table_switch
from sqlalchemy import and_, select
from sqlalchemy.orm.session import sessionmaker


class PlayerDataLoader():
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
            vec = list(item.__dict__.values())[1:-2]
            vec = [0 if i==-1 else i for i in vec]
            rows.append(vec)
        return rows

    def create_dataset(self, poss: str, start, end) -> list:
        pos_table = player_season_table_switch[poss.upper()]

        for key, value in position_map.items():
            if poss.upper() in value:
                positions = value

        stmt = select(pos_table, team_season.points).join_from(pos_table, team_season).filter(
            and_(pos_table.av != 0, pos_table.year_id >= start, pos_table.year_id <= end)).join_from(
                pos_table, player).filter(player.position.in_(positions))

        rows = self.sess.execute(stmt).all()

        seasons = list(list(zip(*rows))[0])
        labels = list(list(zip(*rows))[1])
        data = self.get_vectors(seasons)

        return seasons, labels, data

    def one_player_season(self, poss: str, name, year):
        season_table = player_season_table_switch[poss.upper()]
        season = self.sess.query(season_table).filter(
            season_table.year_id == year).join(
                season_table.player_relationship).filter_by(name=name)
        season = season.all()
        return season[0]

    def minmax_norm(self, dataset):
        dataset = np.array(dataset)
        zero_cols = np.argwhere(np.all(dataset[..., :] == 0, axis = 0))
        dataset = np.delete(dataset, zero_cols, axis=1)
        return ((dataset - np.min(dataset, axis=0)) / (np.max(dataset, axis=0) - np.min(dataset, axis=0)))

    def zscore_norm(self, dataset: np.ndarray) -> np.ndarray :
        dataset = np.array(dataset)
        zero_cols = np.argwhere(np.all(dataset[..., :] == 0, axis = 0))
        dataset = np.delete(dataset, zero_cols, axis=1)
        return (dataset - np.mean(dataset, axis=0)) / np.std(dataset, axis=0)
