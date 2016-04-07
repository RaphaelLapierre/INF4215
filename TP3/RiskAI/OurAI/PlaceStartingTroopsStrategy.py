from os import path
import pickle

class PlaceStartingTroopsStrategy:

    def __init__(self):
        self._fileName = "placeStartingTroops"

    def load(self, countries):
        if path.isfile(self._fileName):
            self._countryWeight = pickle.load(open(self._fileName, 'rb'))
        else:
            self._countryWeight = {c : 1 for c in countries}

    def save(self):
        pickle.dump(self._countryWeight, open(self._fileName, 'wb'))

    def placeStartingTroopCountry(self, nbTroopsToPlace, ownedCountries, allCountries):
        if not self._countryWeight:
            self.load(allCountries)
        placeTroopAction = []

    def getDangerIndex(self, ownedCountry, playerName):
        totalFriendlyTroops = 0
        totalTroops = 0
        for country in ownedCountry.getNeighbours():

            if country.getOwner() is playerName:
                totalFriendlyTroops += country.getNbTroops()

            totalTroops += country.getNbTroops();

        totalFriendlyTroops += ownedCountry.getNbTroops()
        totalTroops += ownedCountry.getNbTroops()

        return totalFriendlyTroops / totalTroops


    def onGameWon(self):
        for country in self._chosenCountry:
            self._countryWeight[country] *= 1.10
        self.save()

    def onGameLost(self):
        for country in self._chosenCountry:
            self._countryWeight[country] *= 0.9
        self.save()