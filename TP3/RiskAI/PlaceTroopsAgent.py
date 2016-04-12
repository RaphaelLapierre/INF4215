# coding=utf-8
from os import path
import pickle
from Glie import glie
from Agent import Agent
from PlaceTroopsAction import PlaceTroopsAction

class PlaceTroopsAgent(Agent):

    def __init__(self, gamma, filename):
        Agent.__init__(self)
        self._fileName = filename + "placeTroops.pickle"
        self.load()
        self.gamma = gamma
        self.lastState = None
        self.lastAction = None
        self.lastScore = 0
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

    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        currentState = self.getCurrentState(ownedCountries)

        #action possible: ajouter 1 armée sur un pay
        possibleActions = range(0, len(ownedCountries))

        currentAction = glie(self, currentState, 1.1, 100, possibleActions)
        self.lastState = currentState
        self.lastAction = currentAction
        self.lastScore = self.getScore(ownedCountries)

        chosenCountry = currentState[currentAction][0]

        placeTroopAction = []
        placeTroopAction.append(PlaceTroopsAction(chosenCountry, nbTroopsToPlace))
        return placeTroopAction

    def getCurrentState(self, ownedCountries):
        currentState = [(country.getName(), self.isInDanger(country)) for country in ownedCountries]
        currentState.sort(key=lambda x: x[1])
        return tuple(currentState)

    def isInDanger(self, ownedCountry):
        inDanger = False
        for country in ownedCountry.getNeighbours():
            if country.getOwner() != ownedCountry.getOwner():
                inDanger = country.getNbTroops() >= ownedCountry.getNbTroops()
        return inDanger

    def getScore(self, ownedCountries):
        score = 0
        for country in ownedCountries:
            score += country.getNbTroops()
            for voisin in country.getNeighbours():
                if country.getOwner() != voisin.getOwner():
                    score -= voisin.getNbTroops()
        return score


    def feedback(self, ownedCountries):
        if not self.lastAction and not self.lastState:
            pass

        newScore = self.getScore(ownedCountries.values())
        if newScore > self.lastScore:
            reward = 1
        elif newScore == self.lastScore:
            reward = 0
        else:
            reward = -1

        self.setQs(reward, self.lastState, self.lastAction, self.getCurrentState(ownedCountries.values()))
        self.lastAction = None
        self.lastState = None

    def setQs(self, reward, state, action, newState):
        self.setQ(state, action, self.QValue(state, action) +
                      self.alphaValue(state, action) *
                      (reward + self.gamma * self.getMaxQValue(newState, range(0, len(newState))) - self.QValue(state, action)))
