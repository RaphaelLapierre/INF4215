# coding=utf-8
from os import path
import pickle
from Glie import glie
from Agent import Agent
from AttackAction import AttackAction

class AttackAgent(Agent):
    def __init__(self, gamma):
        Agent.__init__(self)
        self._fileName = "attackQ.pickle"
        self.load()
        self.gamma = gamma
        self.lastState = None
        self.lastAction = None

    def load(self):
        if path.isfile(self._fileName):
            self.nbQ, self.q, self.alpha = pickle.load(open(self._fileName, 'rb'))

    def save(self):
        pickle.dump((self.nbQ, self.q, self.alpha), open(self._fileName, 'wb'))

    def declareAttack(self, ownedCountries, allCountries):
        currentState = self.getState(ownedCountries)

        #on s'interesse seulement au nombre de troop dans les pays qui peuvent
        #s'attaquer
        currentStateQ = tuple([zone[0].getNbTroops() - zone[1].getNbTroops() for zone in currentState])
        possibleActions = range(0, 2**len(currentState))
        #Pour chaque frontiere, on peut attaquer ou ne rien faire, il y a donc 2**n choix possibles
        #on peut encode un action dans un nombre binaire, ou chaque bit represente une frontiere
        #si le bit est a 1, on attaque, sinon on ne fait rien

        currentAction = glie(self, currentStateQ, 1.1, 10, possibleActions)

        actions = [x is '1' for x in '{0:b}'.format(currentAction)]
        attackActionList = []
        attackIndex = 0
        for attack in actions:
            if attack:
                attackActionList.append(AttackAction(currentState[attackIndex][0], currentState[attackIndex][1], 3))
            attackIndex += 1


        self.lastState = currentStateQ
        self.lastAction = currentAction

        return attackActionList

    def onAttackResult(self, reward, ownedCountries):
        newState = tuple([zone[0].getNbTroops() - zone[1].getNbTroops() for zone in self.getState(ownedCountries.values())])

        self.setQ(self.lastState, self.lastAction, self.QValue(self.lastState, self.lastAction) +
                      self.alphaValue(self.lastState, self.lastAction) *
                      (reward + self.gamma * self.getMaxQValue(newState, range(0, len(newState))) - self.QValue(self.lastState, self.lastAction)))

    def onGameEnded(self):
       # self.save()
        pass

    def getState(self, ownedCountries):
        zoneDeGuerre = []
        for country in ownedCountries:
            for voisin in country.getNeighbours():
                if voisin.getOwner() is not country.getOwner():
                    zoneDeGuerre.append((country, voisin))
        return zoneDeGuerre
