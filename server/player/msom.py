from minisom import MiniSom
import numpy as np

def get_indices_of_k_smallest(arr, k):
    idx = np.argpartition(arr.ravel(), k)
    return tuple(np.array(np.unravel_index(idx, arr.shape))[:, range(min(k, 0), max(k, 0))])

# randomly generate probability table because we a need non-uniform random distribution
p=np.random.randint(low=1, high=10, size=(1,50))
p = p / p.sum(axis=1, keepdims=1)
data = []
labels = []
# create samples and assign label that follows pattern in samples 
for i in range (100):
    sample = np.random.choice(50, 10, replace=False, p=p[0])
    data.append(sample)
    labels.append(np.sum(sample))
# normalize all feature dimensions to [0,1]
data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

# create SOM and train weights to cluster samples
som = MiniSom(10,10,10, sigma=.4, learning_rate=.6,
              neighborhood_function='gaussian', random_seed=10)
som.pca_weights_init(data)
som.train(data, 100)

# assign scores to samples based on average score of closest 3 neurons
scores = np.zeros(len(data))
lm = som.labels_map(data, labels)
for i, sample in enumerate(data):
    activation_map = som.activate(sample)
    cls = get_indices_of_k_smallest(activation_map, 3)
    for j, x in enumerate(cls[0]):
        neuron = lm[(x, cls[1][j])]
        if neuron:
            k = 1
            for key, value in neuron.items():
                scores[i] += key * value
                scores[i] /= k
                k += 1
