import numpy as np

class CashModel():
    def __init__(self, position_category):
        self.position = position_category

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
        yax = prop_data[:,1]
        coeffs = np.polyfit(xax, yax, 4)
        return coeffs
