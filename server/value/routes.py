from db.constants import roles
from flask import Blueprint, request
from flask.json import jsonify
from server.value.player_data import PlayerDataLoader
from server.value.value import ValueModel
import numpy as np

bp = Blueprint('player_model', __name__)
@bp.route('/test', methods=['GET'])
def score_position_endpoint():
    position_category = request.args['pos_group']
    dres, seasons = score_position(position_category)
    return jsonify(dres)
    

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
        #vm.save_model()
    
    dres = []
    names = {}
    #dscores = vm.score_set_dist(data_normed, 6, role)
    dscores = vm.score_set_avg(data_normed, 6)
    meen = np.mean(dscores)
    dev = np.std(dscores)
    
    res_seasons = []
    res_labels = []
    for i, season in enumerate(seasons):
        if dscores[i] ==0:
            continue
        #if abs(ascores[i] - meen) > dev*2:
        #    continue
        key = season.player_relationship.name + ' ' + str(season.player_season_relationship.year_id)
        dres.append(dscores[i] )
        names[key] = (dscores[i])
        res_seasons.append(season)
        res_labels.append(labels[i])
    names = dict(sorted(names.items(), key=lambda item: item[1], reverse=True))
    lm = vm.som.labels_map(data_normed, labels)

    return dres, res_seasons, res_labels

score_position('qb')

