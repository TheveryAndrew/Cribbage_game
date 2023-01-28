from cribbagegame import CribbageGame
import time
from xmlrpc.client import Boolean
if __name__=='__main__':
    rollingballs=['dumaque', 'babies', 'bellies']
    def removedumaque(is_there_a_dumaque : Boolean):
        if is_there_a_dumaque==False:
            pass
        else:
            rollingballs.remove('dumaque')
    cribbage_game=CribbageGame()
    print("Let's play cribbage")
    time.sleep(2)
    removedumaque(True)
    cribbage_game.deal()
    cribbage_game.event_loop()