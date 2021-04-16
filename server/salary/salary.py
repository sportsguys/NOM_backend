import numpy as np
from db.constants import yearly_caps

class CashModel():
    def __init__(self, position_category):
        self.position = position_category

    def normalize_salaries(self, salaries, seasons):
        normed = []
        for i, salary in enumerate(salaries):
            #my_guys_years = list(x.year_id for x in seasons
            #    if x.player_relationship.name == seasons[i].player_relationship.name)
            year = seasons[i].year_id
            #years_played = year - min(my_guys_years)
            #salary -= rm.min_salary(year, years_played)

            ratio = yearly_caps[year] / np.mean(list(yearly_caps.values()))
            normed.append(salary / ratio)

        return normed

    def fit_points(self, proportions, scores, seasons, salaries):
        instances = []
        for i, proportion in enumerate(proportions):
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
