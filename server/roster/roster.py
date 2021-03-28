from math import log10
import numpy as np

class RosterModel():
    def __init__(self, polys=None):
        if not polys:
            self.polys = self._test_data()
        else:
            self.polys = polys

    def _test_data(self):
        polys = [
            [-1/5, 2/3, 0, 0],
            [-1/3, 1, 0, 0]
        ]
        return polys
    
    def allocate_cash(self):
        cash = 1000
        gradients = list(map(np.polyder, self.polys))
        salaries = np.zeros(2)
        for dollar in range(2,cash+1):
            next_dollar = list(map(log10, salaries+dollar))
            grad_vals = list(map(np.polyval, gradients, next_dollar))
            salaries[np.argmax(grad_vals)] += 1

        return salaries