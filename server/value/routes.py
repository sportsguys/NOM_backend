from flask import Blueprint
from flask.json import jsonify
from server.value.valuenet import ValueNet
from server.value.value import ValueModel

bp = Blueprint("player_model", __name__)
@bp.route('/test', methods=['GET'])
def generate_model():
    #request_data = request.get_json()
    #res = train_test()
    pass


def train_test():
    from server.value.dataloader import ValueDataLoader
    dl = ValueDataLoader()

    all_seasons = dl.batch_player_seasons('qb', 2011, 2019)
    tr_seasons, data, labels = dl.create_dataset(all_seasons, 'offense')

    mm_data = dl.zscore_norm(data)

    vm = ValueModel('test', mm_data, labels)
    vm.train_model()

    ares = {}
    dres = {}
    labels_for_reference = {}
    for i, season in enumerate(tr_seasons):
        key = season.player_relationship.name + str(season.year_id)
        ares[key] = vm.score_one_avg(mm_data[i], 5) * season.av
        dres[key] = vm.score_one_dist(mm_data[i], 1) * season.av
        labels_for_reference[key] = labels[i]
    ares = dict(sorted(ares.items(), key=lambda item: item[1], reverse=True))
    dres = dict(sorted(dres.items(), key=lambda item: item[1], reverse=True))
    labels_for_reference = dict(sorted(labels_for_reference.items(), key=lambda item: item[1], reverse=True))
    return None

train_test()