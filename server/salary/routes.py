from flask import Blueprint, request
from flask.json import jsonify
from server.salary.salary_data import SalaryDataLoader
from server.value.routes import score_position
from server.salary.salary import CashModel
import time

bp = Blueprint('salary_model', __name__)
@bp.route('/test', methods=['GET'])
def fit_salary_curve_endpoint():
    pass

def fit_salary_curve(position_category):
    cm = CashModel(position_category)
    dl = SalaryDataLoader()
    total_start = time.time()
    start = time.time()
    scores, seasons, labels = score_position(position_category)
    end = time.time()
    print("time_to_score: {}".format(end - start))
    
    start = time.time()
    salaries, scores, seasons = dl.get_salaries(scores, seasons)
    #dl.save_salaries(position_category, salaries, scores, seasons)
    end = time.time()
    print("time to get salaries: {}".format(end - start))

    start = time.time()
    normed_salaries = cm.normalize_salaries(salaries, seasons)
    end = time.time()
    print("time to norm salaries: {}".format(end - start))

    start = time.time()
    coeffs = cm.fit_points(normed_salaries, scores, seasons, salaries)
    end = time.time()
    print("time to fit: {}".format(end - start))

    total_end = time.time()
    print('total time: {}'.format(total_end - total_start))
    return coeffs

#fit_salary_curve('wr')