import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

def lucas_kanade(slika1, slika2, prozor):
    pilImage1 = Image.open('data/' + slika1)
    pilImage2 = Image.open('data/' + slika2)
    if pilImage1.size != pilImage2.size:
        raise ValueError('Images have different dimensions')
    assert prozor % 2 == 1
    img1 = np.array(pilImage1).astype(np.int32)
    img2 = np.array(pilImage2).astype(np.int32)
    size = pilImage1.height, pilImage1.width
    del pilImage1
    del pilImage2
    dX = np.zeros(size)
    dY = dX.copy()
    dT = dX.copy()
    for i in range(size[0]):
        for j in range(size[1]):
            dX[i, j] = img1[i, np.clip(j + 1, 0, size[1] - 1)] - img1[i, j]
            dY[i, j] = img1[np.clip(i + 1, 0, size[0] - 1), j] - img1[i, j]
            dT[i, j] = img2[i, j] - img1[i, j]
    windowSize = 2 * prozor + 1
    U = np.zeros((math.ceil(size[0] / windowSize), math.ceil(size[1] / windowSize)))
    V = U.copy()
    for i in range(0, size[0], windowSize):
        for j in range(0, size[1], windowSize):
            xSlice = dX[i:np.clip(i + windowSize, 0, size[0]), j:np.clip(j + windowSize, 0, size[1])]
            ySlice = dY[i:np.clip(i + windowSize, 0, size[0]), j:np.clip(j + windowSize, 0, size[1])]
            tSlice = dT[i:np.clip(i + windowSize, 0, size[0]), j:np.clip(j + windowSize, 0, size[1])]
            xSquared = np.sum(np.square(xSlice))
            ySquared = np.sum(np.square(ySlice))
            xy = np.sum(np.multiply(xSlice, ySlice))
            xtNeg = -np.sum(np.multiply(xSlice, tSlice))
            ytNeg = -np.sum(np.multiply(ySlice, tSlice))
            mat1 = np.array([[xSquared, xy], [xy, ySquared]])
            mat2 = np.array([xtNeg, ytNeg])
            mv = np.dot(np.linalg.inv(mat1), mat2)
            U[i // windowSize, j // windowSize] = mv[1]
            V[i // windowSize, j // windowSize] = mv[0]
    # plt.quiver(range(0, size[0], windowSize), range(0, size[1], windowSize), U, V)
    plt.quiver(U, V)
    plt.show()


lucas_kanade('Teddy/frame10.png', 'Teddy/frame11.png', 7)
