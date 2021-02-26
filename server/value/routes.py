from flask import Blueprint
from flask.json import jsonify
#from server.db import get_db
from server.value.value import ValueModel

bp = Blueprint("player_model", __name__)

@bp.route('/test', methods=['GET'])
def generate_model():
    #request_data = request.get_json()
    
    vm = ValueModel()
    vm.gen_test_data()
    vm.value_normalize()
    vm.train_model()

    nscores = vm.score_dist_from_greatest_k()

    res = {}
    for i, score in enumerate(nscores):
        res[i] = score
    return jsonify(res)
