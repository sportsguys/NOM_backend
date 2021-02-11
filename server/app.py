from flask import Flask
from flask.globals import session
import server.config as conf


def start():
    app = Flask(__name__)
    app.config.from_object(conf.dev)

    from server.module1 import mod1
    app.register_blueprint(mod1.bp, url_prefix='/route1')
    
    app.run()