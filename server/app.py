from flask import Flask
import server.config as conf

def start():
    app = Flask(__name__)
    app.config.from_object(conf.dev)

    from server.module1 import mod1
    app.register_blueprint(mod1.bp, url_prefix='/route1')
    
    from server.player import routes as player_routes
    app.register_blueprint(player_routes.bp, url_prefix='/player')

    
    app.run()