from __future__ import print_function, division
import numpy as np
from queue import Queue

class TabuSearch:
    def __init__(self, options, weights, values, capacities):
        self.itemCount = options['itemCount']
        self.dimensions = options['dimensions']
        self.maxStagnationCounter = options['maxStagnationCounter']
        self.diversificationFlips = options['diversificationFlips']
        self.tabuListSize = options['tabuListSize']
        self.maxIterations = options['maxIterations']
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.capacities = np.array(capacities)

        if self.itemCount < 1:
            raise ValueError('Invalid itemCount value')
        if self.dimensions < 1:
            raise ValueError('Invalid dimensions value')
        if self.maxStagnationCounter < 0:
            raise ValueError('Invalid maxStagnationCounter value')
        if self.diversificationFlips < 0 or self.diversificationFlips > self.itemCount:
            raise ValueError('Invalid diversificationFlips value')
        if self.tabuListSize < 0:
            raise ValueError('Invalid tabuListSize value')
        if self.maxIterations < 1:
            raise ValueError('Invalid maxIterations value')
        if weights.shape != (self.dimensions, self.itemCount):
            raise ValueError('Invalid weights matrix')
        if values.shape != (self.itemCount,):
            raise ValueError('Invalid values vector')
        if capacities.shape != (self.dimensions,):
            raise ValueError('Invalid capacities vector')

        # Tabu search state variables
        self.curSolution = np.zeros(self.itemCount)
        self.curSolutionFeasible = True
        self.curInfeasibilityMeasure = 0
        self.bestSolution = np.zeros(self.itemCount)
        self.bestSolutionValue = 0
        self.stagnationCounter = 0
        self.stagnationList = np.zeros(self.itemCount)
        self.tabuSet = set()
        self.tabuQueue = Queue()


    def Run(self):
        """Runs the Tabu search algorithm with the specified options,
        returning the best found solution and its value.
        """
        iteration = 0
        while iteration < self.maxIterations:
            self.Step()
            iteration += 1
        return self.bestSolution, bestSolutionValue

    def Step(self):
        """Runs a single step of the Tabu search algorithm, changing
        the state. Returns None.
        """
        if self.curSolutionFeasible:
            self.StepFeasible()
        else:
            self.StepInfeasible()


    def StepFeasible(self):
        """Called by the Step method if curSolution is feasible.
        """
        newSolution, newSolutionValue = self.FindFeasibleSolution()
        if newSolution != None:
            self.UpdateSolution(newSolution, newSolutionValue)
        else:
            diversified = self.Diversify()
            if not diversified:
                self.MoveToInfeasibleSpace()


    def StepInfeasible(self):
        """Called by the StepFeasible method if no feasible solution can be found
        or by Step if curSolution is infeasible.
        """
        pass


    def Diversify(self):
        """Called by StepFeasible. Returns True if diversification happened,
        False otherwise
        """
        if self.stagnationCounter < self.maxStagnationCounter:
            return False
        else:
            newSolution = self.curSolution.copy()
            for flip in range(self.diversificationFlips):
                idx = self.stagnationCounter.argmax()
                newSolution[idx] = 1
                self.stagnationCounter[idx] = 0
            self.UpdateSolution(newSolution)


    def FindFeasibleSolution(self):
        """Tries adding items into the solution until one is found that is feasible.
        The solution and its value are returned if its found, otherwise
        None, None is returned.
        """
        candidate = self.curSolution.copy()
        for idx, elem in enumerate(self.curSolution):
            if elem == 0:
                candidate[idx] = 1
                if self.Feasible(candidate) and not self.TabuListContains(candidate):
                    return candidate, self.SolutionValue(candidate)
                else:
                    candidate[idx] = 0
        return None, None


    def Feasible(self, solution):
        """solution is a numpy array of ones and zeros. The return value is
        a numpy bool, indicating whether or not the solution is feasible.
        """
        return np.all(np.less_equal(np.dot(self.weights, solution), self.capacities))


    def SolutionValue(self, solution):
        """solution is a numpy array of ones and zeros. The return value is a
        numpy int, or float if there's a weight that's a float.
        """
        return np.sum(np.multiply(solution, self.values))


    def AddToTabuList(self, solution):
        """Adds the solution (a numpy array of ones and zeros) into the tabu
        list
        """
        if len(tabuSet) > self.tabuListSize:
            oldest = self.tabuQueue.get(block=False)
            self.tabuSet.remove(oldest)

        asTuple = tuple(solution)
        self.tabuQueue.put(asTuple, block=False)
        self.tabuSet.add(asTuple)


    def TabuListContains(self, solution):
        return tuple(solution) in self.tabuSet


    def UpdateSolution(self, newSolution, newSolutionValue = None):
        """Updates all state variables.
        """
        self.curSolution = newSolution
        self.AddToTabuList(newSolution)
        if not self.Feasible(newSolution):
            self.curSolutionFeasible = False
        else:
            self.curSolutionFeasible = True
            if newSolutionValue == None:
                newSolutionValue = self.SolutionValue(newSolution)
            if newSolutionValue > self.bestSolutionValue:
                self.UpdateBestSolution(newSolution, newSolutionValue)
            for idx, elem in enumerate(newSolution):
                if elem == 0:
                    self.stagnationList[idx] += 1
                else:
                    self.stagnationList[idx] = 0


    def UpdateBestSolution(self, newBestSolution, newBestSolutionValue):
        """Does not check whether or not newBestSolution is actually better
        than self.bestSolution.
        """
        self.bestSolution = newBestSolution
        self.bestSolutionValue = newBestSolutionValue
        self.stagnationCounter = 0


    def CalcInfeasibilityMeasure(self, solution):
        """Returns the sum of the normalized amounts by which each capacity is
        exceeded.
        """
        resourceUsages = np.dot(self.weights, solution)
        infeasibilityMeasure = 0
        for usage, capacity in zip(resourceUsages, self.capacities):
            if usage > capacity:
                infeasibilityMeasure += (usage - capacity) / capacity
        return infeasibilityMeasure


    def BestInfeasibleSolution(self):
        """Finds the best solution out of any neighboring ones. Returns it
        and its value. Returns None, None if no solution not in the tabu
        list can be found.
        """
        curInfesabileSolution = self.curSolution.copy()
        curInfesabileSolutionValue = self.SolutionValue(bestInfeasibleSolution)
        bestInfeasibleSolution = curInfesabileSolution
        bestInfeasibleSolutionValue = curInfesabileSolutionValue
        pass
        # TODO
