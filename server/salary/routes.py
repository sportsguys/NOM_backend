from flask import Blueprint, request
from flask.json import jsonify
from server.salary.salary_data import SalaryDataLoader
from server.value.routes import score_position
from server.salary.salary import CashModel

bp = Blueprint('salary_model', __name__)
@bp.route('/test', methods=['GET'])
def fit_salary_curve_endpoint():
    pass

def fit_salary_curve(position_category):
    cm = CashModel(position_category)
    dl = SalaryDataLoader()

    try:
        salaries, scores, years, ts_ids = dl.get_salaries(position_category)
    except RuntimeError:
        print("Position not yet scored")
        score_position(position_category)
        salaries, scores, years, ts_ids = dl.get_salaries(position_category)

    normed_salaries = cm.normalize_salaries(salaries, years)
    combined_salaries, combined_scores = cm.depth(normed_salaries, scores, ts_ids)
    coeffs = cm.fit_points(normed_salaries, scores)

    return coeffs

fit_salary_curve('LB')