from flask import Flask
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.dev)
    
    from server.value import routes as value_routes
    app.register_blueprint(value_routes.bp, url_prefix='/player')

    
    return app