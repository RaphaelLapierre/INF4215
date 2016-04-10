import signal
from Controller import *
from RandomAI import *
from CarreRougeAi import CarreRougeAI

finish = False
def signal_handler(signal, frame):
    global finish
    print "Arret demande"
    finish = True

signal.signal(signal.SIGINT, signal_handler)

ai1 = RandomAI() # agent adverse sans apprentissage machine
ai2 = CarreRougeAI() # agent adverse aleatoire

nbWinAI2 = 0
for i in xrange(100):
    if finish:
        break
    controller = Controller("Americas", "Normal", "Random", ai1, ai2)
    winningPlayerIndex = controller.play()
    if winningPlayerIndex == 1:
        nbWinAI2 += 1

ai2.save()

print "Nb win of ai2 : ", nbWinAI2
