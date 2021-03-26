from flask import Blueprint
from roster.roster import RosterModel


bp = Blueprint("roster_model", __name__)
@bp.route('/test', methods=['GET'])
def roster_model():
    rm = RosterModel()