import pygame
import os
class starter_pickings():
    def __init__(self):
        self.personname=""
        self.personprofile=0
        self.clock = pygame.time.Clock()
        self.base_font = pygame.font.Font(None, 32)
        self.input_rect = pygame.Rect(300, 450, 200, 50)
        self.color_active = pygame.Color(pygame.Color(0, 0, 255))
        self.color = pygame.Color(pygame.Color(0, 255 ,0))
        self.active = False
        self.running=True
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
    def button(self, screen, positionx, positiony, height, width, color):
        thebutton=pygame.Rect(positionx-width/2, positiony-height/2, width, height)
        pygame.draw.rect(screen, color, thebutton)
        pygame.Rect(thebutton)
    def name(self, screen):
        smallfont=pygame.font.SysFont('dejavuserif',20)
        text = smallfont.render('Type in your name', True, pygame.Color(0, 0, 0))
        screen.blit(text , (300-20, 400))
        thebutton=pygame.Rect(350-100/2, 550-50/2, 100, 50)
        pygame.draw.rect(screen, color, thebutton)
        pygame.Rect(thebutton)
        smallfont=pygame.font.SysFont('dejavuserif',30)
        text = smallfont.render('Enter', True, pygame.Color(255, 255, 0))
        screen.blit(text , (310, 530))
        event = pygame.event.get()
        for events in event:
            if events.type==pygame.quit:
                running=False
            if events.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                if posx>325 and posx<375:
                    if posy>525 and posy<575:
                        return user_text
                if self.input_rect.collidepoint(events.pos):
                    active = True
                else:
                    active = False
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += events.unicode
        if active:
            color = self.color_active
        else:
            color = color
        pygame.draw.rect(screen, color, self.input_rect)
        text_surface = self.base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))
        self.input_rect.w = max(100, text_surface.get_width()+10)
        pygame.display.flip()
        self.clock.tick(60)
    def profile(self, screen):
        computerprofile=pygame.image.load(os.path.join(self.current_directory, "man-in-questioning-thoughts-clipart.jpg"))
        font=pygame.font.SysFont('dejavuserif',20)
        atext = font.render('Choose a profile:', True, pygame.Color(0, 0, 0))
        screen.blit(atext , (400, 20))
        return computerprofile