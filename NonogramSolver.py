import numpy as np
import matplotlib.image as mpimg
from collections import deque
from functools import reduce

class NonogramSolver:
    def __init__(self, hints):
        self.hints = hints
        self.height = len(self.hints[0])
        self.width = len(self.hints[1])
        self.state = np.array([[0 for i in range(self.width)] for j in range(self.height)])
        self.changedRows = set()
        self.changedCols = set()
        self.order = np.diff([sum([len(y) for y in x]) for x in hints])[0] <= 0
        self.missing = self.width * self.height
        self.verbose = False
        self.__states = {-1: '.', 0: '?', 1: 'X'}
        self.__pixels = {-1: 0xFF, 0: 0x80, 1: 0x00}

    def __str__(self):
        return "\n".join([''.join([self.__states[y] for y in x]) for x in self.state])

    def saveImage(self, filepath):
        img = np.zeros((self.height,self.width))
        for i in range(self.height):
            for j in range(self.width):
                img[i][j] = self.__pixels[self.state[i][j]]
        self.img = img.astype(np.uint8)
        mpimg.imsave(filepath, self.img, cmap = 'gray')

    def __howManyMissing(self):
        return np.sum(self.state == 0)

    def solve(self):
        self.possibilitiesRows = [[NonogramSolver.Holes.holesToSolutions(y, x) for y in NonogramSolver.Holes.getAll(len(x)+1, self.width - sum(x) - (len(x)-1) )] for x in self.hints[0]]
        self.possibilitiesCols = [[NonogramSolver.Holes.holesToSolutions(y, x) for y in NonogramSolver.Holes.getAll(len(x)+1, self.height - sum(x) - (len(x)-1) )] for x in self.hints[1]]

        step = 0
        while True:
            if self.order:
                self.__rowsAND(step)
                self.__removeBadCols()
                self.__colsAND(step)
                self.__removeBadRows()
            else:
                self.__colsAND(step)
                self.__removeBadRows()
                self.__rowsAND(step)
                self.__removeBadCols()
            if self.verbose:
                print(self)
                print(self.width * '-')
            if self.__howManyMissing() == 0 or self.__howManyMissing() == self.missing:
                break
            self.missing = self.__howManyMissing()
            step += 1
        if self.verbose:
            print(self.width * '=')
            print(self)
            print(self.width * '=')

    @staticmethod
    def __logicalAND(arr1, arr2):
        tmp = arr1.copy()
        tmp[arr1 != arr2] = 0
        return tmp

    def __rowsAND(self, step):
        ind = list(self.changedRows) if step > 0 else range(len(self.possibilitiesRows))
        newRows = list(map(lambda y: reduce(lambda p, q: NonogramSolver.__logicalAND(p, q), y) if len(y) > 0 else y, [self.possibilitiesRows[x] for x in ind]))
        self.changedCols.clear()
        for i in range(len(ind)):
            diff = self.state[ind[i],:] != newRows[i]
            self.changedCols.update(np.where(diff)[0])
            self.state[ind[i],diff] = newRows[i][diff]

    def __colsAND(self, step):
        ind = list(self.changedCols) if step > 0 else range(len(self.possibilitiesCols))
        newCols = list(map(lambda y: reduce(lambda p, q: NonogramSolver.__logicalAND(p, q), y) if len(y) > 0 else y, [self.possibilitiesCols[x] for x in ind]))
        self.changedRows.clear()
        for i in range(len(ind)):
            diff = self.state[:,ind[i]] != newCols[i]
            self.changedRows.update(np.where(diff)[0])
            self.state[diff,ind[i]] = newCols[i][diff]


    def __removeBadRows(self):
        for i in self.changedRows:
            ok = [NonogramSolver.__checkSolution(self.state[i,:], x) for x in self.possibilitiesRows[i]]
            self.possibilitiesRows[i] = [self.possibilitiesRows[i][j] for j in np.arange(len(ok))[ok]]
        if not np.all(list(map(len, self.possibilitiesRows))):
            self.__invalid()

    def __removeBadCols(self):
        for i in self.changedCols:
            ok = [NonogramSolver.__checkSolution(self.state[:,i], x) for x in self.possibilitiesCols[i]]
            self.possibilitiesCols[i] = [self.possibilitiesCols[i][j] for j in np.arange(len(ok))[ok]]
        if not np.all(list(map(len, self.possibilitiesCols))):
            self.__invalid()

    @staticmethod
    def __checkSolution(arr, sol):
        for i in range(len(arr)):
            if arr[i] == 1 and sol[i] == -1 or arr[i] == -1 and sol[i] == 1:
                return False
        return True

    def __invalid(self):
        raise Exception("Obrazek logiczny niemożliwy do rozwiązania!")

    # klasa sluzaca do generowania dziur i propozycji poczatkowych
    class Holes:
        possibilities = deque([])

        @staticmethod
        def getAll(places, points):
            NonogramSolver.Holes.possibilities = deque([])
            NonogramSolver.Holes.fillHoles(None, places, points)
            return list(NonogramSolver.Holes.possibilities)

        @staticmethod
        def fillHoles(holes, lvl, rem):
            if lvl <= 0 or rem < 0:
                return
            if holes is None:
                holes = [0] * lvl
            if lvl == 1:
                holes[len(holes)-1] = rem
                NonogramSolver.Holes.possibilities.append(holes)
            else:
                counter = rem
                while counter >= 0:
                    holes2 = list(holes)
                    holes2[len(holes)-lvl] = counter
                    NonogramSolver.Holes.fillHoles(holes2, lvl-1, rem-counter)
                    counter -= 1

        @staticmethod
        def holesToSolutions(holes, hints):
            tmp = deque([])
            for _ in range(holes[0]):
                tmp.append(-1)
            for i in range(len(hints)):
                for _ in range(hints[i]):
                    tmp.append(1)
                if i < (len(hints) - 1):
                    tmp.append(-1)
                for _ in range(holes[i+1]):
                    tmp.append(-1)
            return np.array(tmp, dtype=np.int8)