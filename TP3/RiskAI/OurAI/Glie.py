#-*- coding: latin-1 -*-
import random

#Impl�mentation de la m�thode GLIE pour le machine learning
#Bas� sur l'impl�mentation de Michel Gagnon pour le jeu de TicTacToe

#On favorise les actions qui ont �t� peu essay�es en leur attribuant
#arbitrairement une r�compense plus �lev�e
def glie(agent, currentState, reward, minCount, possibleActions):
    def f(u,n):
        return u if n >= minCount else reward

    qVals = agent.getQValues(currentState,possibleActions)
    random.shuffle(qVals)
    return max([(f(val,agent.countQ(currentState,a)),a) for (a,val) in qVals])[1]