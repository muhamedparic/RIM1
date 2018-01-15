from TabuSearch import TabuSearch
import random
import numpy as np
import matplotlib.pyplot as plt

options = {
    'itemCount': 50,
    'dimensions': 2,
    'maxStagnationCounter': 50,
    'diversificationFlips': 2,
    'tabuListSize': 200,
    'maxIterations': 50
}

weights = [[random.randint(1, 100) for i in range(50)], [random.randint(1, 100) for i in range(50)]]
values = [random.randint(1, 100) for i in range(50)]
capacities = [1000, 1000]

ts = TabuSearch(options, weights, values, capacities)
print(ts.Run())
options['maxIterations'] = 100
ts = TabuSearch(options, weights, values, capacities)
print(ts.Run())
options['maxIterations'] = 200
ts = TabuSearch(options, weights, values, capacities)
print(ts.Run())
options['maxIterations'] = 500
ts = TabuSearch(options, weights, values, capacities)
print(ts.Run())
options['maxIterations'] = 1000
ts = TabuSearch(options, weights, values, capacities)
print(ts.Run())
