import numpy as np
from db.constants import yearly_caps

class CashModel():
    def __init__(self, position_category):
        self.position = position_category

    def beta_coeff(self, scores, labels):
        scores = np.array(scores)
        labels = np.delete(labels, np.where(np.mean(scores) - scores > 1.5*np.std(scores)))
        scores = np.delete(scores, np.where(np.mean(scores) - scores > 1.5*np.std(scores)))
        lin_fit = np.polyfit(scores, labels, 1)
        bcoeff = abs(lin_fit[0]) * (1/np.std(labels)) * (1/np.std(scores))
        return bcoeff

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

    def fit_points(self, normed_salaries, scores, beta_coeff):
        log_salary = np.log2(normed_salaries)
        y_ax = np.array(scores)
        y_ax = np.delete(y_ax, np.where(log_salary<=0))
        log_salary = np.delete(log_salary, np.where(log_salary<=0))
        y_ax *= beta_coeff
        coeffs = np.polyfit(log_salary, y_ax, 2)
        return coeffs
