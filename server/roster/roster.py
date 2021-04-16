from math import log2
from server.roster.roster_data import RosterDataLoader
import numpy as np
from db.constants import yearly_caps, min_roster_dist, position_map

class RosterModel():
    def _mock_polys(self):
        polys = [
            [-1/5, 2/3, 0, 0],
            [-1/3, 1, 0, 0]
        ]
        return polys

    def _log_val(self, lcoeff, bias, x):
        return lcoeff * np.log2(x) + bias

    def allocate(self, cash, polys):
        polys = np.array(polys)
        salaries = np.zeros(len(polys))
        delta = cash / 1000.0
        salaries += 375000
        cash -= 375000*len(salaries)
        for dont_loop_a_hundred_million_times in range(1,1000):
            next_dollar = np.log2(salaries+delta)
            curr_dollar = np.log2(salaries)
            new = np.array(list(map(np.polyval, polys, next_dollar)))
            old = np.array(list(map(np.polyval, polys, curr_dollar)))
            grad_vals = new - old
            salaries[np.argmax(grad_vals)] += delta
        return salaries

    def min_rookie_salary(self, year):
        return 375000 + (year-2011)*15000

    def min_salary(self, year, n_years):
        return self.min_rookie_salary(year) + (n_years * 75000)

    def avg_min_sal(self):
        total_min_sal = 0
        for i, year in enumerate(yearly_caps.keys()):
            total_min_sal += self.min_rookie_salary(year)
        return total_min_sal / (i+1)

    def min_cap_dist(self):
        min_cap_dist = {}
        m = self.avg_min_sal()
        for key, val in min_roster_dist.items():
            min_cap_dist[key] = m * val
        return min_cap_dist

    def remaining_cash(self):
        mcd = self.min_cap_dist()
        remaining_cash = np.mean(list(yearly_caps.values()))
        for value in mcd.values():
            remaining_cash -= value
        return remaining_cash

    def positional_spending(self, team_name, year):
        spending = {}
        dl = RosterDataLoader()
        team_dist = dl.team_spending(team_name, year)
        for pos, val in team_dist.items():
            for cat, members in position_map.items():
                if pos in members:
                    try:
                        spending[cat] += val
                    except KeyError:
                        spending[cat] = val
        return spending
