from flask import Blueprint, jsonify

bp = Blueprint("mod_one", __name__)

@bp.route('/', methods=['GET'])
def hello():
    res = {'message': 'Hello World'}
    return jsonify(res)