from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    from . import mod_one
    app.register_blueprint(mod_one.modulee)

    return app