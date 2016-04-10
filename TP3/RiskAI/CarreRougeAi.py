# coding=utf-8
from RiskAI.AI import AI
from RiskAI.AttackAgent import AttackAgent
from RiskAI.ChooseStartingCountryAgent import ChooseStartingCountryAgent
from RiskAI.PlaceStartingTroopsAgent import PlaceStartingTroopsAgent
from RiskAI.PlaceTroopsAction import PlaceTroopsAction

__author__ = 'GND'


class CarreRougeAI(AI):

    def __init__(self):
        self._startingCountryAgent = ChooseStartingCountryAgent(gamma=1)
        self.saveLastStartCountry = True
        self.saveLastPlaceStartingTroop = True
        self._placeStartingTroopsAgent = PlaceStartingTroopsAgent(gamma=1)
        self.attackAgent = AttackAgent(gamma=1)


    # Choose a starting country one at the time
    #
    # remainingCountries : the countries that are not chosen yet
    # ownedCountries : the countries that you own so far
    # allCountries : all countries
    #
    # return : one element of the remainingCountries list
    def chooseStartingCountry(self, remainingCountries, ownedCountries, allCountries):
        return self._startingCountryAgent.chooseStartingCountry(remainingCountries, ownedCountries.values(), allCountries)

    # Place troops before the games begins. You can place only a portion of the available
    # troops. This method will be called again if you still have troops to be placed
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeStartingTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        #On a besoin de l'etat final pour le QLearning du ChooseStartingCountryAgent
        if(self.saveLastStartCountry):
            oc = map(lambda x : x.getName(), ownedCountries.values())
            self._startingCountryAgent.appendLastIteration(([], oc))
            self.saveLastStartCountry = False

        #on commence par mettre 1 armé sur chaque pays
        placeTroopAction = []
        if all(c.getNbTroops() == 0 for c in ownedCountries.values()):
            placeTroopAction = [PlaceTroopsAction(c.getName(), 1) for c in ownedCountries.values()]
        else:
            placeTroopAction = self._placeStartingTroopsAgent.placeStartingTroopCountry(nbTroopsToPlace, ownedCountries.values(), allCountries)

        return placeTroopAction

    # Declare attacks on the other countries. You need to check if the defending country is
    # not yours, or your attack declaration will be ignored
    #
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of AttackAction.
    def declareAttacks(self, ownedCountries, allCountries):
        return self.attackAgent.declareAttack(ownedCountries.values(), allCountries)

    # Place troops at the start of your turn. You need to place all available troops at one
    #
    # nbTroopsToPlace : the amount of troops you can place
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a list of PlaceTroopsAction
    def placeTroops(self, nbTroopsToPlace, ownedCountries, allCountries):
        #Méthode appelé juste après la phase de départ
        #On va donc passé l'état de départ au PlaceStartingTroopsAgent
        #Pour son QLearning
        if self.saveLastPlaceStartingTroop:
            state = self._placeStartingTroopsAgent.getCurrentState(ownedCountries.values())
            self._placeStartingTroopsAgent.appendLastIteration(state)
            self.saveLastPlaceStartingTroop = False

        placeTroopAction = [self._placeStartingTroopsAgent.placeStartingTroopCountry(1, ownedCountries.values(), allCountries)[0] for x in range(0,nbTroopsToPlace)]
        return placeTroopAction

    # Move troops after attacking. You can only move one per turn
    #
    # turnAttackResults : the result of all the attacks you declared this turn
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a lsingle MoveTroopAction
    def moveTroops(self, turnAttackResults, ownedCountries, allCountries):
        pass


    # Decide the amount of attacking dice while attacking
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 0 and 3, 0 means that you want to cancel the attack
    #
    # default behaviour : always choose 3
    def decideNbAttackingDice(self, attackResult, ownedCountries, allCountries):
        return 3

    # Decide the amount of defending dice while defending
    #
    # attackResult : the result of the pending attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and 2
    #
    # default behaviour : always choose 2
    def decideNbDefendingDice(self, attackResult, ownedCountries, allCountries):
        return 2

    # Decide the amount of troops to be transfered to the new country after winning a battle
    #
    # attackResult : the result of the attack
    # startCountry : the country to move from
    # endCountry : the country to move to
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : a number between 1 and the amount of troops in startCountry
    #
    # default behaviour : move half of the troops to the new country
    def decideNbTransferingTroops(self, attackResult, startCountry, endCountry, ownedCountries, allCountries):
        return startCountry.getNbTroops() / 2

    # Called when your AI wins an attack
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackWon(self, attackResult, ownedCountries, allCountries):
        self.attackAgent.onAttackResult(1, ownedCountries)

    # Called when your AI loses an attack. AKA the attack finished because you only have 1 troop left in
    # the attacking country
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onAttackLost(self, attackResult, ownedCountries, allCountries):
        self.attackAgent.onAttackResult(-1, ownedCountries)

    # Called when your AI succeeds to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendWon(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI fails to defend a territory.
    #
    # attackResult : the result of the attack
    # ownedCountries : the countries that you own
    # allCountries : all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onDefendLost(self, attackResult, ownedCountries, allCountries):
        pass

    # Called when your AI wins the game
    #
    # allCountries : all countries, you own all countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameWon(self, allCountries):
        self._startingCountryAgent.onGameWon()
        self._placeStartingTroopsAgent.onGameWon()

    # Called when your AI lost the game
    #
    # allCountries : all countries, you own no countries
    #
    # return : nothing
    #
    # default behaviour : do nothing
    def onGameLost(self, allCountries):
        self._startingCountryAgent.onGameLost()
        self._placeStartingTroopsAgent.onGameLost()

