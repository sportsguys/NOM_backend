from flask import Blueprint
from flask.json import jsonify
#from server.db import get_db
from server.player.player import PlayerModel

bp = Blueprint("player_model", __name__)

@bp.route('/test', methods=['GET'])
def generate_model():
    #request_data = request.get_json()
    
    pm = PlayerModel()
    pm.gen_test_data()
    pm.value_normalize()
    pm.train_model()

    nscores = pm.score_dist_from_greatest_k()

    res = {}
    for i, score in enumerate(nscores):
        res[i] = score
    return jsonify(res)
