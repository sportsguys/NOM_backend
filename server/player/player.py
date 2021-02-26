from server.player.minisom import MiniSom
import numpy as np
import pickle

def _get_indices_of_k_smallest(arr, k):
    """ Returns tuple of lists of indicies in the form
        ([x0, x1, .. ,xk], [y0, y1, .. , yk])\n
        More dimensions add lists to the tuple ie ([xk],[yk],[zk])
    """
    return tuple(np.array(np.unravel_index(np.argpartition(arr.ravel(), k), 
        arr.shape))[:, range(min(k, 0), max(k, 0))])
class PlayerModel():
    def __init__(self, name='test', data=None, labels=None):
        self.name = name
        self.som = None
        self.dataset = data # not yet normalized for training
        self.labels = labels

    #TODO add percentile normalization,
    #
    def gen_test_data(self):
        """ Randomly generate probability table because we a need non-uniform random distribution.

            Create samples and assign label that follows pattern in samples.

            Returns tuple of lists data, labels
        """
        p=np.random.randint(low=1, high=10, size=(1,50))
        p = p / p.sum(axis=1, keepdims=1)
        data = []
        labels = []
        for i in range (100):
            sample = np.random.choice(50, 10, replace=False, p=p[0])
            data.append(sample)
            labels.append(np.sum(sample))
        self.dataset, self.labels = data, labels

    def value_normalize(self):
        """ normalize feature vectors in the dataset to contain 
            values [0,1] based on mean and standard deviation
            
            self.dataset and self.data are separate to allow for other normalization techniques 
        """
        self.data = (self.dataset - np.mean(self.dataset, axis=0)) / np.std(self.dataset, axis=0)

    def train_model(self):
        n_features = len(self.data[0])
        # create SOM and train weights to cluster samples
        self.som = MiniSom(10, 10, n_features, sigma=.4, learning_rate=.6,
                    neighborhood_function='gaussian', random_seed=10)
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

    def score_avg_neighborhood(self):
        """ Assign scores to samples based on average score of closest 3 neurons.

            Return list of scores with the same shape as and corresponding to data
        """
        scores = np.zeros(len(self.data))
        lm = self.som.labels_map(self.data, self.labels)
        for i, sample in enumerate(self.data):
            activation_map = self.som.activate(sample)
            cls = _get_indices_of_k_smallest(activation_map, 3)
            for j, x in enumerate(cls[0]):
                neuron = (x, cls[1][j])
                n_scores = lm[neuron]
                if n_scores:
                    for k, score in enumerate(n_scores):
                        scores[i] += score
                        scores[i] /= k+1
        return scores.tolist()

    def _k_greatest_neurons(self, lm, k):
        winners = []
        for position, p_scores in lm.items():
            winners.append((position, np.max(p_scores)))
            if len(winners) > k:
                winners.sort(key=lambda kv: kv[1])
                winners.pop(0)
        return winners

    def score_dist_from_greatest_k(self, k=5):
        """ Assign scores to samples based on distance from neurons containting the 
            k greatest scores. 

            Return list of scores with the same shape as and corresponding to data\n
        """
        scores = np.zeros(len(self.data))
        lm = self.som.labels_map(self.data, self.labels)
        winners = self._k_greatest_neurons(lm, k)
        for i, sample in enumerate(self.data):
            am = self.som.activate(sample)
            for neuron, _ in winners:
                # neuron is a centroid coordinate
                scores[i] += (1 / am[neuron[0]][neuron[1]]) 
                # lower activation value = closer to neuron. using 1 might be arbitrary
        return scores