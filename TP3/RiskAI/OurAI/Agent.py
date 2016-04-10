#-*- coding: latin-1 -*-

# Agent pour choisir les pays de départ
# Adapté de l'agent de TicTacToe de Michel Gagnon
class Agent:
    def __init__(self):
        self.initQ()

    def initQ(self):
        self.nbQ = {}
        self.q = {}
        self.alpha = {}

    def QValue(self,grid,action):
        if (grid,action) in self.q:
            return self.q[(grid,action)]
        else:
            return 0.0

    def countQ(self,grid,action):
        if (grid,action) in self.nbQ:
            return self.nbQ[(grid,action)]
        else:
            return 0

    def alphaValue(self,grid,action):
        if (grid,action) in self.alpha:
            return self.alpha[(grid,action)]
        else:
            return 1.0

    def setQ(self,grid,action,value):
        self.q[(grid,action)] = value
        if (grid,action) in self.nbQ:
            self.nbQ[(grid,action)] += 1
        else:
            self.nbQ[(grid,action)] = 1
        if (grid,action) in self.alpha:
            self.alpha[(grid,action)] *= 0.99
        else:
            self.alpha[(grid,action)] = 1

    def getMaxQAction(self,grid, possibleActions):
        return  max([(self.QValue(grid,a),a) for a in possibleActions])[1]

    def getMaxQValue(self,grid, possibleActions):
        if len(possibleActions) == 0:
            return 0
        else:
            return  max([self.QValue(grid,a) for a in possibleActions])

    def getQValues(self,grid, possibleActions):
        return  [(a,self.QValue(grid,a)) for a in possibleActions]