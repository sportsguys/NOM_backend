from flask import Blueprint, request
from flask.json import jsonify
from server.salary.salary_data import SalaryDataLoader
from server.value.routes import score_position
from server.salary.salary import CashModel
from db.constants import roles

bp = Blueprint('salary_model', __name__)
@bp.route('/test', methods=['GET'])
def fit_salary_curve_endpoint():
    pass

def fit_salary_curve(position_category):
    cm = CashModel(position_category)
    dl = SalaryDataLoader()

    for key, value in roles.items():
            if position_category.upper() in value:
                role = key
                break

    try:
        salaries, scores, years, ts_ids, labels = dl.get_salaries(position_category, role)
    except RuntimeError:
        print("Position not yet scored")
        score_position(position_category)
        salaries, scores, years, ts_ids, lables = dl.get_salaries(position_category, role)

    beta_coeff = cm.beta_coeff(scores, labels)
    normed_salaries = cm.normalize_salaries(salaries, years)
    combined_salaries, combined_scores = cm.depth(normed_salaries, scores, ts_ids)
    coeffs = cm.fit_points(combined_salaries, combined_scores, beta_coeff)

    return coeffs, beta_coeff
