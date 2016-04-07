import pickle
from os import path

class LearningStartingCountryStrategy:

    def __init__(self):
        self._fileName = "learningStartingCountry"
        self._chosenCountry = []

    def load(self, countries):
        if path.isfile(self._fileName):
            self._countryWeight = pickle.load(open(self._fileName, 'rb'))
        else:
            self._countryWeight = {c : 1 for c in countries}

    def save(self):
        pickle.dump(self._countryWeight, open(self._fileName, 'wb'))

    def chooseStartingCountry(self, remainingCountry, allCountries):
        if not self._countryWeight:
            self.load(allCountries)

        country = max(remainingCountry, key=lambda x : self._countryWeight[x])
        self._chosenCountry.append(country)
        return country

    def onGameWon(self):
        for country in self._chosenCountry:
            self._countryWeight[country] *= 1.10
        self.save()

    def onGameLost(self):
        for country in self._chosenCountry:
            self._countryWeight[country] *= 0.9
        self.save()
