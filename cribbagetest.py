from cribbagegame import CribbageGame
import pygame
import time
def blurSurface(surface, amt):
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf
cribbage_game = CribbageGame()
cribbage_game.deal()
cribbage_game.draw_card()
blurSurface(cribbage_game.screen, 2)
time.sleep(10)