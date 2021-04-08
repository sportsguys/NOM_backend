from flask import Blueprint, request
from flask.json import jsonify
from server.salary.salary_data import SalaryDataLoader
from value.routes import score_position
from server.salary.salary import CashModel

bp = Blueprint('salary_model', __name__)
@bp.route('/test', methods=['GET'])
def fit_salary_curve_endpoint():
    pass

def fit_salary_curve(position_category):
    cm = CashModel(position_category)
    dl = SalaryDataLoader()

    scores, seasons = score_position(position_category)
    salaries, scores, seasons = dl.get_salaries(scores, seasons)
    proportions = dl.normalize_salaries(salaries, seasons)

    coeffs = cm.fit_points(proportions, scores, seasons, salaries)
    return coeffs

fit_salary_curve('qb')
