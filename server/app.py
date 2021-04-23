from flask import Flask
import config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.dev)
    app.config['JSON_SORT_KEYS'] = False
    from server.value import routes as value_routes
    app.register_blueprint(value_routes.bp, url_prefix='/player')

    from server.roster import routes as roster_routes
    app.register_blueprint(roster_routes.bp, url_prefix='/roster')

    from server.salary import routes as salary_routes
    app.register_blueprint(salary_routes.bp, url_prefix='/salary')
    
    return app.run(host='0.0.0.0', port=os.getenv('PORT'))