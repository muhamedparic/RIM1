import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

rgbImage = cv.imread('airport.jpg')

gsImage = cv.cvtColor(rgbImage, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale', gsImage)

resizedImage = cv.resize(rgbImage, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resizedImage)

blurredImage = cv.filter2D(rgbImage, -1, (1 / 9) * np.ones((3, 3)))
cv.imshow('Blurred', blurredImage)

edgeAmplifiedImage = cv.add(rgbImage, cv.subtract(rgbImage, blurredImage))
#cv.imshow('Edges amplified', edgeAmplifiedImage)

edges = cv.Laplacian(gsImage, -1)
cv.imshow('Edges', edges)

bitwiseNot = cv.bitwise_not(edges)
cv.imshow('Bitwise not', bitwiseNot)

rgbConverted = cv.cvtColor(rgbImage, cv.COLOR_BGR2RGB)
edgesAmplifiedConverted = cv.cvtColor(edgeAmplifiedImage, cv.COLOR_BGR2RGB)

plt.subplot(2, 1, 1)
plt.title('Original')
plt.imshow(rgbConverted)
plt.subplot(2, 1, 2)
plt.title('Edges amplified')
plt.imshow(edgesAmplifiedConverted)
plt.show()

highBoostImage = cv.addWeighted(rgbImage, 1, cv.subtract(rgbImage, blurredImage), 4, 0)

plt.plot()
plt.subplot(3, 1, 1)
plt.title('Original')
plt.imshow(rgbConverted)
plt.subplot(3, 1, 2)
plt.title('Low boost')
plt.imshow(edgesAmplifiedConverted)
plt.subplot(3, 1, 3)
plt.title('High boost')
plt.imshow(cv.cvtColor(highBoostImage, cv.COLOR_BGR2RGB))
plt.show()

bilateralBlurred = cv.bilateralFilter(rgbImage, 9, 75, 75)
bilateralEdgeAmplified = cv.add(rgbImage, cv.subtract(rgbImage, bilateralBlurred))
beaConverted = cv.cvtColor(bilateralEdgeAmplified, cv.COLOR_BGR2RGB)

plt.plot()
plt.subplot(2, 1, 1)
plt.title('Standard edge amplified')
plt.imshow(edgesAmplifiedConverted)
plt.subplot(2, 1, 2)
plt.title('Bilateral smoothing edge amplified')
plt.imshow(beaConverted)
plt.show()

plt.plot()
plt.subplot(2, 1, 1)
plt.title('Using OpenCV add')
plt.imshow(beaConverted)
plt.subplot(2, 1, 2)
plt.title('Using NumPy addition')
plt.imshow(cv.cvtColor(rgbImage + cv.subtract(rgbImage, bilateralBlurred), cv.COLOR_BGR2RGB))
plt.show()

cv.waitKey()
cv.destroyAllWindows()
