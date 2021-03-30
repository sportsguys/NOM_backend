from sqlalchemy.orm.session import sessionmaker
from db.db import connect_db, get_engine
import config 
from db.models import *
import copy


class ValueDataLoader():
    def __init__(self):
        #engine = get_engine()
        engine = connect_db(config.dev.DB_URI)
        Session = sessionmaker(bind=engine, autoflush=True)
        self.sess = Session()

    def get_vectors(self, objlist):
        rows = []
        non_dims = ['age', 'id', 'player_id', 'team_season_id', 'year_id', 'team', 'av']
        for item in objlist:
            item = copy.copy(item)
            [item.__dict__.pop(key, None) for key in non_dims]
            rows.append(list(item.__dict__.values())[1:-2]) #slice instance state and relationship objects
        return rows

v = ValueDataLoader()
wrs = v.sess.query(wr).all()
wrdata = v.get_vectors(wrs)

print('ope')
