# coding=utf-8
from os import path
import pickle
from Glie import glie
from Agent import Agent
from AttackAction import AttackAction

class AttackAgent(Agent):
    def __init__(self, gamma, filename):
        Agent.__init__(self)
        self._fileName = filename + "attackQ.pickle"
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

    def declareAttack(self, ownedCountries, allCountries):
        currentState = self.getCurrentState(ownedCountries)

        #on s'interesse seulement au nombre de troop dans les pays qui peuvent
        #s'attaquer
        currentStateQ = tuple([self.getArmyDiff(zone[0].getNbTroops(), zone[1].getNbTroops()) for zone in currentState])
        possibleActions = range(0, 2**len(currentState))
        #Pour chaque frontiere, on peut attaquer ou ne rien faire, il y a donc 2**n choix possibles
        #on peut encode un action dans un nombre binaire, ou chaque bit represente une frontiere
        #si le bit est a 1, on attaque, sinon on ne fait rien
        currentAction = None
        attackActionList = []
        if possibleActions:
            currentAction = glie(self, currentStateQ, 1.1, 100, possibleActions)
            actions = [x == '1' for x in '{0:b}'.format(currentAction)]
            attackIndex = 0
            for attack in actions:
                if attack:
                    attackActionList.append(AttackAction(currentState[attackIndex][0], currentState[attackIndex][1], 3))
                attackIndex += 1

        self.lastState = currentStateQ
        self.lastAction = currentAction
        self.lastScore = self.getScore(ownedCountries, allCountries)

        if len(attackActionList) == 0:
            self.onAttackResult(-0.5, ownedCountries)

        return attackActionList


    def getArmyDiff(self, troops1, troops2):
        diff = troops1 - troops2
        if diff < -10:
            return -10
        if diff > 10:
            return 10

        return diff

    def onAttackResult(self, reward, ownedCountries):
        newState = tuple([self.getArmyDiff(zone[0].getNbTroops(), zone[1].getNbTroops()) for zone in self.getCurrentState(ownedCountries)])
        self.setQs(reward, self.lastState, self.lastAction, newState)
        self.lastAction = None
        self.lastState = None

    def onGameEnded(self):
       # self.save()
        pass

    def getCurrentState(self, ownedCountries):
        zoneDeGuerre = []
        for country in ownedCountries:
            for voisin in country.getNeighbours():
                if voisin.getOwner() != country.getOwner() and country.getNbTroops() > 1:
                    zoneDeGuerre.append((country, voisin))
        return zoneDeGuerre

    def getScore(self, ownedCountries, allCountries):
        name = ownedCountries[0].getOwner()
        score = 0
        for country in allCountries:
            if country.getOwner() == name:
                score += country.getNbTroops()
            else:
                score -= country.getNbTroops()
        return score


    def feedback(self, ownedCountries, allCountries):
        if not self.lastAction and not self.lastState:
            pass

        newScore = self.getScore(ownedCountries.values(), allCountries)
        if newScore > self.lastScore:
            reward = 1
        elif newScore == self.lastScore:
            reward = -0.5
        else:
            reward = -1

        newState = tuple([self.getArmyDiff(zone[0].getNbTroops(), zone[1].getNbTroops()) for zone in self.getCurrentState(ownedCountries.values())])
        self.setQs(reward, self.lastState, self.lastAction, newState)
        self.lastAction = None
        self.lastState = None

    def setQs(self, reward, state, action, newState):

        self.setQ(state, action, self.QValue(state, action) +
                      self.alphaValue(state, action) *
                      (reward + self.gamma * self.getMaxQValue(newState, range(0, 2**len(newState)-1)) - self.QValue(state, action)))