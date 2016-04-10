import signal
from Controller import *
from RandomAI import *
from CarreRougeAi import CarreRougeAI

import csv

finish = False
def signal_handler(signal, frame):
    global finish
    print "Arret demande"
    finish = True

signal.signal(signal.SIGINT, signal_handler)

ai1 = RandomAI() # agent adverse sans apprentissage machine
ai2 = CarreRougeAI() # agent adverse aleatoire

nbWinAI2 = 0
winRate = []
lastTenWin = 0
for i in xrange(10000):
    if finish:
        break
    controller = Controller("Americas", "Normal", "Random", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWinAI2 += 1
        lastTenWin += 1

    if i%10 == 0:
        winRate.append(lastTenWin/10.0)

ai2.save()
writer = csv.writer(open("data.csv", 'wb'), delimiter=';')
writer.writerow(winRate)

print "Nb win of ai2 : ", nbWinAI2
