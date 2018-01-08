from __future__ import print_function, division
import csv
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_score, recall_score
import numpy as np

def loadData():
    with open('Skin_NonSkin.txt', 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        data = []
        for row in reader:
            if len(row) != 0:
                row = tuple([int(num) for num in row])
                data.append(row)
        return data

dataSet = loadData()
dataTrain, dataTest = train_test_split(dataSet, test_size=0.33)
classifier = GaussianNB()
trainInputs = [row[:3] for row in dataTrain]
trainOutputs = [row[3] for row in dataTrain]
classifier.fit(trainInputs, trainOutputs)
testInputs = [row[:3] for row in dataTest]
testOutputs = [row[3] for row in dataTest]
predictedOutputs = classifier.predict(testInputs)
print('Preciznost:', precision_score(testOutputs, predictedOutputs))
print('Senzitivnost:', recall_score(testOutputs, predictedOutputs))
