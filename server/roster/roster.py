from math import log10
import numpy as np
from db.constants import yearly_caps, min_roster_dist

class RosterModel():
    def _mock_polys(self):
        polys = [
            [-1/5, 2/3, 0, 0],
            [-1/3, 1, 0, 0]
        ]
        return polys

    def allocate(self, cash, polys):
        gradients = list(map(np.polyder, polys))
        salaries = np.zeros(len(polys))
        delta = cash / 1000.0
        for dont_loop_a_hundred_million_times in range(1,1000):
            next_dollar = list(map(log10, salaries+delta))
            grad_vals = list(map(np.polyval, gradients, next_dollar))
            salaries[np.argmax(grad_vals)] += delta
        return salaries

    def min_salary(self, year):
        return 375000 + (year-2011)*15000

    def avg_min_sal(self):
        total_min_sal = 0
        for i, year in enumerate(yearly_caps.keys()):
            total_min_sal += self.min_salary(year)
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
