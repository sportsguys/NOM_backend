from flask import Flask
import server.config as conf

def create_app():
    app = Flask(__name__)
    app.config.from_object(conf.dev)
    
    from server.player import routes as player_routes
    app.register_blueprint(player_routes.bp, url_prefix='/player')

    
    return app