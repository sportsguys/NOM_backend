import numpy as np
from db.constants import yearly_caps

class CashModel():
    def __init__(self, position_category):
        self.position = position_category

    def normalize_salaries(self, salaries, years):
        normed = []
        for i, salary in enumerate(salaries):
            ratio = yearly_caps[years[i]] / np.mean(list(yearly_caps.values()))
            normed.append(salary / ratio)
        return normed

    def depth(self, salaries, scores, ts_ids):
        res = {}
        for ts_id in ts_ids:
            res[ts_id] = [0,0]
        for i, ts_id in enumerate(ts_ids):
            res[ts_id][0] += salaries[i]
            res[ts_id][1] += scores[i]
        sals = list(list(zip(*res.values())))[0]
        scores = list(list(zip(*res.values())))[1] 
        return sals, scores

    def fit_points(self, normed_salaries, scores):
        #xax = normed_salaries[:,0]
        lax = np.log2(normed_salaries)
        yax = np.array(scores)
        yax = np.delete(yax, np.where(lax<=0))
        #xax = np.delete(xax, np.where(lax<=0))
        lax = np.delete(lax, np.where(lax<=0))
        coeffs = np.polyfit(lax, yax, 4)
        return coeffs
