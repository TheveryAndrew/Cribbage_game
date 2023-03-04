import pygame
import os
pygame.init()
current_directory = os.path.dirname(os.path.realpath(__file__))
screen = pygame.display.set_mode((800, 800))
computerprofile=pygame.image.load(os.path.join(current_directory, "man-in-questioning-thoughts-clipart.jpg"))
font=pygame.font.SysFont('dejavuserif',20)
atext = font.render('Choose a profile:', True, pygame.Color(0, 0, 0))
screen.blit(atext , (400, 20))
while True:
    event = pygame.event.get()
    screen.fill(pygame.Color(25, 60, 25))
    pygame.display.update()
    screen.blit(screen, (50, 50), computerprofile)
    for events in event:
        if events.type==pygame.quit:
            pygame.QUIT()