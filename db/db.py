from flask import g
from flask.globals import current_app
import sqlalchemy as s
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

def connect_db(db_uri):
    engine = s.create_engine(db_uri)
    try: 
        engine.connect().close()
        print("connected to db")
        return engine
    except s.exc.OperationalError as e:
        print("could not connect to db")
        raise(e)

def get_engine() -> Engine:
    if "db" not in g:
        g.db = connect_db(current_app.config['DB_URI'])
    return g.db

def get_session():
    if "session" not in g:
        Session = sessionmaker(bind=get_engine(), autoflush=True)
        g.session = Session()
    return g.session
    
Base = declarative_base()
def init_db(engine):
    db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
    import db.models
    Base.metadata.create_all(bind=engine)
    