from flask import g, current_app
import sqlalchemy as s 

def get_db():

    if "db" not in g:
        g.db = connect_db(current_app.config)
    return g.db

def connect_db(config):
    engine = s.create_engine(config.get('DB_URI'))
    try: 
        engine.connect().close()
        print("connected to db")
        return engine
    except s.exc.OperationalError as e:
        print("could not connect to db")
        raise(e)