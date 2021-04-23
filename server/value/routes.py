from db.constants import roles, position_map
from flask import Blueprint, request
from flask.json import jsonify
from server.value.player_data import PlayerDataLoader
from server.value.value import ValueModel
import numpy as np
import math

bp = Blueprint('player_model', __name__)
@bp.route('/test', methods=['GET'])
def score_position_endpoint():
    position_category = request.args['pos_group']
    scores, seasons, labeles = score_position(position_category)
    return jsonify(scores)


def score_position(category_name: str):
    for key, value in roles.items():
        if category_name.upper() in value:
            role = key

    dl = PlayerDataLoader()
    seasons, labels, data = dl.create_dataset(category_name, 2007, 2020, role)
    data_normed = dl.minmax_norm(data)

    vm = ValueModel(category_name, data_normed, labels)
    try:
        vm = vm.load_model(category_name)
    except:
        vm.train_model()
        vm.save_model()
    
    scores = vm.score_set_dist(data_normed, 4, role)
    outliers = np.where(scores-np.mean(scores) > 4*np.std(scores))
    outliers = np.append(outliers, np.where(np.isinf(scores)))
    if max(scores) == math.inf:
        if np.argmax(scores) not in outliers:
            outliers.append(np.argmax(scores))
    labels = np.delete(labels, outliers)
    seasons = np.delete(seasons, outliers)
    scores = np.delete(scores, outliers)

    for i, season in enumerate(seasons):
        if season.av > 2:
            scores[i] = scores[i] * np.log2(season.av)

    dl.save_scores(scores, seasons)
    return scores, seasons, labels

for cat in list(position_map.keys()):
    if cat != 'OL':
        score_position(cat)