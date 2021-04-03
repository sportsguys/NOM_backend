from flask import Blueprint
from flask.globals import request
from roster.roster import RosterModel

bp = Blueprint("roster_model", __name__)

@bp.route('/optimal', methods=['GET'])
def optimal_dist_endpoint():
    return optimal_dist()

@bp.route('/eval_team', methods=['GET'])
def eval_endpoint():
    team = request.args.get('team')
    year = request.args.get('year')
    return evaluate_team(team, year)

@bp.route('compare_teams', methods=['GET'])
def compare_endpoint():
    teama = request.args.get('teama')
    yeara = request.args.get('yeara')
    teamb = request.args.get('teamb')
    yearb = request.args.get('yearb')
    return compare_teams(teama, teamb, yeara, yearb)   



def optimal_dist():
    pass

def evaluate_team(team_name, year):
    pass

def compare_teams(team_a, team_b, year_a, year_b):
    pass