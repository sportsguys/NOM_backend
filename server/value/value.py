from math import sqrt
from server.value.minisom import MiniSom
import numpy as np
import pickle

def _get_indices_of_k_smallest(arr, k):
    """ Returns tuple of lists of indicies in the form
        ([x0, x1, .. ,xk], [y0, y1, .. , yk])\n
        More dimensions add lists to the tuple ie ([xk],[yk],[zk])
    """
    return tuple(np.array(np.unravel_index(np.argpartition(arr.ravel(), k), 
        arr.shape))[:, range(min(k, 0), max(k, 0))])

class ValueModel():
    def __init__(self, name='test', data=None, labels=None):
        self.name = name
        self.som = None
        self.data = data
        self.labels = labels

    def gen_test_data(self):
        """ Randomly generate probability table because we a need non-uniform random distribution.

            Create samples and assign label that follows pattern in samples.

            Returns tuple of lists data, labels
        """
        probability_table = np.random.randint(low=1, high=10, size=(1,50))
        probability_table = probability_table / probability_table.sum(axis=1, keepdims=1)
        data = []
        labels = []
        for iter in range (100):
            sample = np.random.choice(50, 10, replace=False, p=probability_table[0])
            data.append(sample)
            labels.append(np.sum(sample))
        return data, labels

    def train_model(self):
        n_features = len(self.data[0])
        xy = int(sqrt(10*sqrt(len(self.data))))
        # create SOM and train weights to cluster samples
        self.som = MiniSom(xy, xy, n_features, sigma=.4, learning_rate=.5)
        self.som.pca_weights_init(self.data)
        self.som.train(self.data, 100)

    def save_model(self):
        with open(self.name + '.p', 'wb') as outfile:
            pickle.dump(self.som, outfile)

    def load_model(self, name):
        if name:
            try:
                with open(name + '.p', 'rb') as infile:
                    self.som = pickle.load(infile)
            except:
                print('could not load model {}'.format(name))

    def score_one_avg(self, sample, k):
        """ score sample according to average value of the
            samples centroids plus k-1 closest neurons
        """
        lm = self.som.labels_map(self.data, self.labels)
        am = self.som.activate(sample)
        cls = _get_indices_of_k_smallest(am, k)
        total = 0
        num = 0
        for i, x in enumerate(cls[0]):
            neuron = (x, cls[1][i])
            nscores = lm[neuron]
            if nscores:
                for k, score in enumerate(nscores):
                    total += score
                    num += 1
        total /= num
        return total

    def _k_greatest_neurons(self, lm, k):
        winners = []
        for position, p_scores in lm.items():
            winners.append((position, np.max(p_scores)))
            if len(winners) > k:
                winners.sort(key=lambda kv: kv[1])
                winners.pop(0)
        return winners

    def score_one_dist(self, sample, k):
        """ score sample according to inverse distance 
            from neurons containing k greatest labels 
        """
        lm = self.som.labels_map(self.data, self.labels)
        winners = self._k_greatest_neurons(lm, k)
        am = self.som.activate(sample)
        score = 0
        for neuron, _ in winners:
            score += (1/am[neuron[0]][neuron[1]])
        return score

    