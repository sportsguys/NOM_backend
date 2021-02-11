from flask import Blueprint, jsonify
from server.db import get_db

bp = Blueprint("mod_one", __name__)

@bp.route('/', methods=['GET'])
def hello():
    db = get_db()
    #example
    q = db.execute('show tables').fetchall()
    print(q)
    res = {'message': 'Hello World'}
    return jsonify(res)