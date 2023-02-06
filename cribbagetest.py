from cribbagegame import CribbageGame
import pygame
import time
import unittest
class Blurtest(unittest.TestCase):
    def test_blursurface(self):
        cribbage_game = CribbageGame()
        cribbage_game.deal()
        cribbage_game.draw_cards()
        timevar=10
        for i in range(0, 10):
            time.sleep(1)
        timevar=timevar-1
        while timevar<10:
            blurSurface(cribbage_game.screen, 2)
def blurSurface(surface, amt):
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf
if __name__ =="__main__":
    unittest.main()