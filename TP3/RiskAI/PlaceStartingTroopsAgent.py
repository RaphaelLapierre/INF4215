# coding=utf-8
from os import path
import pickle
from Glie import glie
from Agent import Agent
from PlaceTroopsAction import PlaceTroopsAction

class PlaceStartingTroopsAgent(Agent):

    def __init__(self, gamma):
        Agent.__init__(self)
        self._fileName = "placeStartingTroops.pickle"
        self.load()
        self.gamma = gamma
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

    def placeStartingTroopCountry(self, nbTroopsToPlace, ownedCountries, allCountries):
        currentState = self.getCurrentState(ownedCountries)
        if(self.lastState and self.lastAction):
            self.appendLastIteration(currentState)

        #action possible: ajouter 1 armée sur un pay
        possibleActions = range(0, len(ownedCountries))

        currentAction = glie(self, currentState, 1.1, 10, possibleActions)
        self.lastState = currentState
        self.lastAction = currentAction

        chosenCountry = currentState[currentAction][0]

        placeTroopAction = []
        placeTroopAction.append(PlaceTroopsAction(chosenCountry, 1))
        return placeTroopAction

    def getCurrentState(self, ownedCountries):
        currentState = [(country.getName(), self.getDangerIndex(country)) for country in ownedCountries]
        currentState.sort(key=lambda x: x[1])
        return tuple(currentState)

    def getDangerIndex(self, ownedCountry):
        index = ownedCountry.getNbTroops()
        for country in ownedCountry.getNeighbours():

            if country.getOwner() is ownedCountry.getOwner():
                index += country.getNbTroops()
            else:
                index -= country.getNbTroops()

        return index


    def onGameWon(self):
        self.setQs(1)

    def onGameLost(self):
        self.setQs(-1)

    def setQs(self, reward):
        for state, action, newState in self.stateActionList:
            self.setQ(state, action, self.QValue(state, action) +
                      self.alphaValue(state, action) *
                      (reward + self.gamma * self.getMaxQValue(newState, range(0, len(newState))) - self.QValue(state, action)))
        #self.save()
