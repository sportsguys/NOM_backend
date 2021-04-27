from flask import Blueprint, jsonify
from flask.globals import request
from server.roster.roster import RosterModel
from db.constants import position_map
from server.salary.routes import fit_salary_curve
from server.roster.roster_data import RosterDataLoader
import json

bp = Blueprint("roster_model", __name__)

@bp.route('/optimal', methods=['GET'])
def optimal_dist_endpoint():
    dist, scores = optimal_dist()
    total = {
        "allocations": dist,
        "scores": scores
    }
    jsonified = jsonify(total)
    return jsonified

@bp.route('/eval_team', methods=['GET'])
def eval_endpoint():
    team = request.args.get('team')
    year = request.args.get('year')
    sal_totals, score_totals = evaluate_team(team, year)
    total = {
        "allocations": sal_totals,
        "scores": score_totals
    }
    jsonified = jsonify(total)
    return jsonified

@bp.route('compare_teams', methods=['GET'])
def compare_endpoint():
    teama = request.args.get('teama')
    yeara = request.args.get('yeara')
    teamb = request.args.get('teamb')
    yearb = request.args.get('yearb')
    return compare_teams(teama, teamb, yeara, yearb)   



def optimal_dist():
    curves = {}
    for position in position_map.keys():
        if position == 'OL':
            continue
        curves[position] = fit_salary_curve(position)
    rm = RosterModel()
    cash = rm.remaining_cash()
    ol_cash = cash / 4.0
    cash *= 0.75 #OL gets 0.25
    allocations, scores = rm.allocate(cash, list(curves.values()))
    optimal = {}
    op_scores = {}
    for i, (key, value) in enumerate(curves.items()):
        optimal[key] = allocations[i]
        op_scores[key] = scores[i]
    optimal['OL'] = ol_cash
    op_scores['OL'] = "Unknown"
    return optimal, op_scores

def evaluate_team(team_name, year):
    #Team name must be inserted using 3 character value from url on pfr
    # ie. Kansas City Chiefs - kan
    rdl = RosterDataLoader()
    res = rdl.check_allocation(team_name, year)
    return res

def compare_teams(team_a, team_b, year_a, year_b):
    pass

optimal_dist()
#evaluate_team('oti', 2018)