# coding=utf-8
from os import path
import pickle
from Glie import glie
from Agent import Agent
from MoveAction import MoveAction

class FortifyingAgent(Agent):
    def __init__(self, gamma):
        Agent.__init__(self)
        self._fileName = "fortify.pickle"
        self.load()
        self.gamma = gamma
        self.lastState = None
        self.lastAction = None
        self.lastScore = 0

    def load(self):
        if path.isfile(self._fileName):
            self.nbQ, self.q, self.alpha = pickle.load(open(self._fileName, 'rb'))

    def save(self):
        pickle.dump((self.nbQ, self.q, self.alpha), open(self._fileName, 'wb'))

    def moveTroop(self, turnAttackResults, ownedCountries, allCountries):
        currentState = self.getCurrentState(ownedCountries)
        possibleActions = self.getPossibleActions(ownedCountries.values())
        currentAction = None
        if possibleActions:
            currentAction = glie(self, currentState, 1.1, 10, possibleActions)

        self.lastState = currentState
        self.lastAction = currentAction
        self.lastScore = self.getScore(ownedCountries)

        if currentAction:
            startCountry = ownedCountries[currentAction[0]]
            endCountry = ownedCountries[currentAction[1]]
            return MoveAction(startCountry, endCountry, max(1, startCountry.getNbTroops()/2))

    def getPossibleActions(self, ownedCountries):
        actions = []
        for country in [o for o in ownedCountries if o.getNbTroops() > 1]:
            for neighbour in [c for c in country.getNeighbours() if c.getOwner() is country.getOwner()]:
                actions.append((country.getName(), neighbour.getName()))
        return actions

    def getCurrentState(self, ownedCountries):
        currentState = [(country.getName(), self.isInDanger(country)) for country in ownedCountries.values()]
        currentState.sort(key=lambda x: x[1])
        return tuple(currentState)

    def isInDanger(self, ownedCountry):
        inDanger = False
        for country in ownedCountry.getNeighbours():
            if country.getOwner is not ownedCountry.getOwner():
                inDanger = country.getNbTroops() > ownedCountry.getNbTroops()
        return inDanger


    def getScore(self, ownedCountries):
        return len(ownedCountries)

    def feedback(self, ownedCountries):
        if not self.lastAction and not self.lastState:
            pass

        newScore = self.getScore(ownedCountries)
        if newScore > self.lastScore:
            reward = 1
        elif newScore == self.lastScore:
            reward = 0
        else:
            reward = -1

        self.setQs(reward, self.lastState, self.lastAction, self.getCurrentState(ownedCountries))
        self.lastAction = None
        self.lastState = None

    def setQs(self, reward, state, action, newState):
        self.setQ(state, action, self.QValue(state, action) +
                      self.alphaValue(state, action) *
                      (reward + self.gamma * self.getMaxQValue(newState, range(0, len(newState))) - self.QValue(state, action)))

