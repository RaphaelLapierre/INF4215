#-*- coding: latin-1 -*-
import pickle
from os import path
from Agent import Agent
from Glie import glie

# Agent pour choisir les pays de départ
# Adapté de l'agent de TicTacToe de Michel Gagnon
class ChooseStartingCountryAgent(Agent):
    def __init__(self, gamma):
        Agent.__init__(self)
        self._fileName = "startingCountry.pickle"
        self.gamma = gamma
        self.load()
        self.lastState = None
        self.lastAction = None
        self.stateActionList = []

    def load(self):
        if path.isfile(self._fileName):
            self.nbQ, self.q, self.alpha = pickle.load(open(self._fileName, 'rb'))

    def save(self):
        pickle.dump((self.nbQ, self.q, self.alpha), open(self._fileName, 'wb'))

    def appendLastIteration(self, newState):
        self.stateActionList.append((self.lastState, self.lastAction, newState))
        self.lastState = None
        self.lastAction = None

    def chooseStartingCountry(self, remainingCountry, ownedCountries, allCountries):
        rem = ([r.getName() for r in remainingCountry])
        rem.sort()
        own = [o.getName() for o in ownedCountries]
        own.sort()
        currentState = (tuple(rem), tuple(own))
        if(self.lastState and self.lastAction):
            self.appendLastIteration(currentState)

        currentAction = glie(self, currentState, 1.1, 10, currentState[0])
        self.lastState = currentState
        self.lastAction = currentAction
        return next(country for country in remainingCountry if country.getName() is currentAction)

    def onGameWon(self):
        self.setQs(1)

    def onGameLost(self):
        self.setQs(-1)

    def setQs(self, reward):
        for state, action, newState in self.stateActionList:
            self.setQ(state, action, self.QValue(state, action) +
                      self.alphaValue(state, action) *
                      (reward + self.gamma * self.getMaxQValue(newState, newState[0]) - self.QValue(state, action)))
        #self.save()
