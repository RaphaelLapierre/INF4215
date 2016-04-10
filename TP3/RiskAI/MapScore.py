
# Retourne un score normalisé entre 0 et 1
# 0 signifie la defaite total du playerName
# 1 signifie la victoire
def getScore(map, playerName):
    score = 0
    total = 0
    for continent in map.getContinents():
        weight = continent[0] / len(continent[2])
        for country in continent[2]:
            score += weight * country.getNbTroops() * (1 if country.getOwner() == playerName else -1)
            total += weight * country.getNbTroops()
    return (score/total + 1) / 2


def getCountryScore(map, country):
    for continent in map.getContinents():
        if country in continent[2]:
            return continent[0] / len(continent[2])
    return -1


def getDangerIndex(ownedCountry, playerName):
    totalFriendlyTroops = 0
    totalTroops = 0
    for country in ownedCountry.getNeighbours():

        if country.getOwner() is playerName:
            totalFriendlyTroops += country.getNbTroops()

        totalTroops += country.getNbTroops();

    totalFriendlyTroops += ownedCountry.getNbTroops()
    totalTroops += ownedCountry.getNbTroops()

    return totalFriendlyTroops / totalTroops