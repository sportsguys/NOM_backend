from flask import Flask
from server.db import db

def create_app(config_file):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    
    from server.module1 import mod1
    app.register_blueprint(mod1.bp, url_prefix='/route1')

    return app


def setup_database(app):
    pass
    #with app.app_context():
        #db.create_all()
    #db.session.commit()   

if __name__ == '__main__':
    print("in main")
    app = create_app('config.py')
    setup_database(app)
    app.run()