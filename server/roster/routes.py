from flask import Blueprint
from flask.globals import request
from server.roster.roster import RosterModel
from db.constants import position_map
from server.salary.routes import fit_salary_curve
import time

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
    tstart = time.time()
    curves = {}
    for position in position_map.keys():
        if position == 'OL':
            continue
        start = time.time()
        curves[position] = fit_salary_curve(position)
        end = time.time()
        print("time to generate fit for {} = {}".format(position, end-start))
    rm = RosterModel()
    cash = rm.remaining_cash()
    ol_cash = cash / 4.0
    cash *= 0.75 #OL gets 0.25
    allocations = rm.allocate(cash, list(curves.values()))
    optimal = {}
    for i, (key, value) in enumerate(curves.items()):
        optimal[key] = allocations[i]
    optimal['OL'] = ol_cash
    tend = time.time()
    print('time spent generating optimal team distribution: {} seconds'.format(tend-tstart))
    return 0

def evaluate_team(team_name, year):
    pass

def compare_teams(team_a, team_b, year_a, year_b):
    pass

optimal_dist()
"""
score position = list of scored players
find Bcoeff between pos score and label value
model relationship between label and B_pos * log(salary)
"""