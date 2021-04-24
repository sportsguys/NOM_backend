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
        for ts_id in enumerate(ts_ids):
            res[ts_id] = [0,0]

        return res

    def fit_points(self, normed_salaries, scores):
        instances = []
        for i, proportion in enumerate(normed_salaries):
            try:
                instances.append((proportion, scores[i]))
            except:
                continue

        instances = sorted(instances, key=lambda x: x[0], reverse=True)
        prop_data = np.array(instances)
        xax = prop_data[:,0]
        lax = np.log2(xax)
        yax = prop_data[:,1]
        yax = np.delete(yax, np.where(lax<=0))
        xax = np.delete(xax, np.where(lax<=0))
        lax = np.delete(lax, np.where(lax<=0))
        coeffs = np.polyfit(lax, yax, 3)
        return coeffs
