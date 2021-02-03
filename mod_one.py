from flask import Blueprint, request

modulee = Blueprint("mod_one", __name__, url_prefix='/route1')

@modulee.route('/', methods=['GET'])
def hello():
    return 'Hello, World'