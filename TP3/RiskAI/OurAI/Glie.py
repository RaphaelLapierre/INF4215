#-*- coding: latin-1 -*-
import random

#Implémentation de la méthode GLIE pour le machine learning
#Basé sur l'implémentation de Michel Gagnon pour le jeu de TicTacToe

#On favorise les actions qui ont été peu essayées en leur attribuant
#arbitrairement une récompense plus élevée
def glie(agent, currentState, reward, minCount, possibleActions):
    def f(u,n):
        return u if n >= minCount else reward

    qVals = agent.getQValues(currentState,possibleActions)
    random.shuffle(qVals)
    return max([(f(val,agent.countQ(currentState,a)),a) for (a,val) in qVals])[1]