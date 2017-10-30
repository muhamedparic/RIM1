import numpy as np
from scipy.spatial import distance

X = np.array([[1,1], [0,0], [1,0], [0,1], [2,2]])

# pomocna funcija za ispisivanje, umjesto pdist funkcije
def print_dist(X, dist_f):
	for i in range(len(X)):
		for j in range(i+1, len(X)):
			print(dist_f(X[i], X[j]))

		
# distance
def euclidean(X1, X2):
	return np.sqrt(np.sum([(x1 - x2) ** 2 for x1, x2 in zip(X1, X2)]) )


def cityblock(X1, X2):
	return np.sum([np.abs(x1-x2) for x1, x2 in zip(X1, X2)])


def minkowski(X1, X2):
	P = 2;
	diffP = [np.abs((x1-x2)**P) for x1, x2 in zip(X1, X2)]
	return np.sum(diffP)**(1./P)

print_dist(X, cityblock)