import copy
import config
import numpy as np
from db.constants import position_map
from db.db import connect_db, get_engine, get_session
from db.models import *
from scraping.player import player_season_table_switch
from sqlalchemy import and_, select, bindparam, update, insert
from sqlalchemy.orm.session import sessionmaker


class PlayerDataLoader():
    def __init__(self):
        self.engine = get_engine()
        #self.engine = connect_db(config.dev.DB_URI)
        #Session = sessionmaker(bind=self.engine, autoflush=True)
        #self.sess = Session()
        self.sess = get_session()

    def get_vectors(self, objlist):
        rows = []
        non_dims = ['age', 'id', 'player_id', 'team_season_id', 'player_season_id', 'year_id', 'team', 'av', 'g', 'gs']
        for item in objlist:
            item = copy.copy(item)
            [item.__dict__.pop(key, None) for key in non_dims]
            vec = list(item.__dict__.values())[1:]
            vec = [0 if i==-1 else i for i in vec]
            rows.append(vec)
        return rows

    def create_dataset(self, poss: str, start, end, role) -> list:
        pos_table = player_season_table_switch[poss.upper()]

        for key, value in position_map.items():
            if poss.upper() in value:
                positions = value

        if role == 'defense':
            stmt = (
                    select(pos_table, team_season.points_opp).
                    join(pos_table.player_relationship).
                        filter(player.position.in_(positions)).
                    join(pos_table.team_season_relationship).
                    join(pos_table.player_season_relationship).
                        filter(and_(player_season.year_id >= start, player_season.av != 0))#.join(
                    #cap_hit, cap_hit.player_season_id == pos_table.player_season_id)
            )
        else:
            stmt = select(pos_table, team_season.points).join(
                    pos_table.player_relationship).filter(player.position.in_(positions)).join(
                    pos_table.team_season_relationship).join(
                    pos_table.player_season_relationship).filter(and_(
                        player_season.year_id >= start, player_season.av != 0))#.join(
                    #cap_hit, cap_hit.player_season_id == pos_table.player_season_id)

        rows = self.sess.execute(stmt).all()

        seasons = list(list(zip(*rows))[0])
        labels = list(list(zip(*rows))[1])
        #salaries = list(list(zip(*rows))[2])
        data = self.get_vectors(seasons)

        return seasons, labels, data, #salaries

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
        return 2*((dataset - np.min(dataset, axis=0)) / (np.max(dataset, axis=0) - np.min(dataset, axis=0)))-1

    def zscore_norm(self, dataset: np.ndarray) -> np.ndarray :
        dataset = np.array(dataset)
        zero_cols = np.argwhere(np.all(dataset[..., :] == 0, axis = 0))
        dataset = np.delete(dataset, zero_cols, axis=1)
        return (dataset - np.mean(dataset, axis=0)) / np.std(dataset, axis=0)

    def save_scores(self, score_values, seasons):
        ids = [s.player_season_id for s in seasons]
        existing_score_ids = self.sess.execute(select(score.player_season_id).filter(score.player_season_id.in_(ids))).all()
        existing_score_ids = [r.player_season_id for r in existing_score_ids]
        update_params = []
        insert_params = []

        for i, season in enumerate(seasons):
            if season.player_season_id in existing_score_ids:
                update_params.append({'ps_id': season.player_season_id,'value': score_values[i]})
            else:
                insert_params.append({'player_season_id': season.player_season_id,'value': score_values[i],'player_id':season.player_id})

        if update_params:
            update_stmt = (
                update(score).
                where(score.player_season_id == bindparam('ps_id')).
                values(value = 'value')
            )
            with self.engine.begin() as conn:
                conn.execute(update_stmt,update_params)

        if insert_params:
            with self.engine.begin() as conn:
                conn.execute(insert(score), insert_params)