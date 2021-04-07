from flask import Blueprint
from flask.json import jsonify
from flask.wrappers import Request
from server.value.valuenet import ValueNet
from server.value.value import ValueModel
import numpy as np

roles = {
    'offense': ['QB', 'RB', 'TE', 'WR'],
    'defense': ['DL', 'LB', 'DB'],
    'kicker': ['K']
}

bp = Blueprint("player_model", __name__)
@bp.route('/test', methods=['GET'])
def value_model_endpoint():
    pass
    # request_data = Request.get_json()
    # dres, seasons = value_model()
    # return jsonify(dres)
    

def value_model(category_name: str):
    from server.value.dataloader import ValueDataLoader
    dl = ValueDataLoader()
    for key, value in roles.items():
        if category_name.upper() in value:
            role = key
    
    all_seasons = dl.batch_player_seasons(category_name, 2007, 2020)
    tr_seasons, data, labels = dl.create_dataset(all_seasons, role)

    data_normed = dl.zscore_norm(data)
    
    vm = ValueModel(category_name, data_normed, labels)
    try:
        vm.load_model(category_name)
    except:
        vm.train_model()
    
    dres = {}
    dscores = vm.score_set_dist(data_normed, 6, role)
    for i, season in enumerate(tr_seasons):
        key = season.player_relationship.name + ' ' + str(season.year_id)
        dres[key] = dscores[i] * season.av
    dres = dict(sorted(dres.items(), key=lambda item: item[1], reverse=True))
    
    return dres, tr_seasons

