from TabuSearch import TabuSearch
import random
import numpy as np
import matplotlib.pyplot as plt

options = {
    'itemCount': 200,
    'dimensions': 1,
    'maxStagnationCounter': 100,
    'diversificationFlips': 3,
    'tabuListSize': 50,
    'maxIterations': 100
}

weights = [[random.randint(1, 1000) for _ in range(options['itemCount'])]]
values = [random.randint(1, 1000) for _ in range(options['itemCount'])]
capacities = [20000]

results = np.arange(25).reshape(5, 5)

for y, maxIterations in enumerate(range(100, 600, 100)):
    for x, tabuListSize in enumerate(range(5, 30, 5)):
        options['maxIterations'] = maxIterations
        options['tabuListSize'] = tabuListSize
        ts = TabuSearch(options, weights, values, capacities)
        results[y, x] = ts.Run()[1]

plt.imshow(results, cmap='hot', interpolation='nearest')
plt.show()
