from math import log10
import numpy as np


yearly_caps = {
    2011: 120375000,
    2012: 120600000,
    2013: 123600000,
    2014: 133000000,
    2015: 143280000,
    2016: 155270000,
    2017: 167000000,
    2018: 177200000,
    2019: 188200000,
    2020: 198200000
}

min_roster_dist = {
    'QB': 2,
    'RB': 4,
    'TE': 3,
    'WR': 5,
    'OL': 8,
    'DL': 8,
    'LB': 7,
    'DB': 9,
    'K' : 2
}

def _mock_polys(self):
    polys = [
        [-1/5, 2/3, 0, 0],
        [-1/3, 1, 0, 0]
    ]
    return polys

def allocate(cash, polys):
    gradients = list(map(np.polyder, polys))
    salaries = np.zeros(2)
    for dollar in range(2,cash+1):
        next_dollar = list(map(log10, salaries+dollar))
        grad_vals = list(map(np.polyval, gradients, next_dollar))
        salaries[np.argmax(grad_vals)] += 1
    return salaries

def min_salary(year):
    return 375000 + (year-2011)*15000

def avg_min_sal():
    total_min_sal = 0
    for i, year in enumerate(yearly_caps.keys()):
        total_min_sal += min_salary(year)
    return total_min_sal / (i+1)

def min_cap_dist():
    min_cap_dist = {}
    m = avg_min_sal()
    for key, val in min_roster_dist.items():
        min_cap_dist[key] = m * val
    return min_cap_dist

def remaining_cash():
    mcd = min_cap_dist()
    remaining_cash = np.mean(list(yearly_caps.values()))
    for value in mcd.values():
        remaining_cash -= value
    return remaining_cash

mean_cash = remaining_cash()

print('hi')