import random
from netrc import __all__
import pyttsx3
import os
from tkinter import Variable
import pygame
from xmlrpc.client import Boolean
from fontTools.ttLib import TTFont
import time
import functools
CHOOSING=1
PICK_TURN_CARD=2
PEGGING=3
CHECK_POINTS=4
YOU=0
COMPUTER=1
turnevent=pygame.event.custom_type()
timerevent = pygame.event.custom_type()
pygame.init()
engine=pyttsx3.init()
current_directory = os.path.dirname(os.path.realpath(__file__))
class CribbageGame():
    def __init__(self):
        self.computerschoice=None
        self.currentdrawing='drawcomputercards'
        self.theturncard=None
        self.points=0
        self.computerspoints=0
        self.currentcrib=random.randint(0, 1)
        self.whosturn=self.currentcrib^1
        self.currentmode=CHOOSING
        self.selectedcards=[]
        self.pegginglist=[]
        self.message=""
        self.countingpileforperson=[]
        self.rollingballs=['dumaque', 'babies', 'bellies']
        self.criblist=[]
        self.countingpileforcomputer=[]
        self.personprofile=0
        self.computerprofile=0
        self.personname=0
        self.computername=random.choices(['James','Robert','John','Michael','David','William','Richard','Joseph','Thomas','Charles', 'Christopher', 'Daniel', 'Mattew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua'])[0]
        self.screen = pygame.display.set_mode((800,800))

        fonts = map(lambda x: (x, pygame.font.match_font(x)), pygame.font.get_fonts())

        def char_in_font(unicode_char, font):
            for cmap in font['cmap'].tables:
                if cmap.isUnicode():
                    if ord(unicode_char) in cmap.cmap:
                        return True
            return False

        def find_font_for_char(char):
            for font, fontpath in fonts:
                ttf = TTFont(fontpath, fontNumber=0)   # specify the path to the font in question
                if char_in_font(char, ttf):
                    return font

        self.cardfont = find_font_for_char("♣")

    def draw_cards(self, cardnumber:str,cardsuit:str,positionx:float,positiony:float,surface:Variable,highliting:Boolean):
        global selectedcards
        if cribbage_game.currentmode!=CHOOSING:
            if cribbage_game.currentcrib==YOU:
                draw_facedown_cards(facedowncard,100,400,cribbage_game.screen)
            else:
                draw_facedown_cards(facedowncard,100,250,cribbage_game.screen)
        drawrectangle=pygame.Rect(positionx,positiony,100,175)
        redrect=pygame.Rect(positionx-2,positiony-2,104,179)
        if highliting==True:
            pygame.draw.rect(surface, pygame.Color(255,0,0),redrect)
        else:
            pygame.draw.rect(surface,pygame.Color(0,0,0),redrect)
        pygame.draw.rect(surface,pygame.Color(190,190,190),drawrectangle)
        font=pygame.font.SysFont(self.cardfont,18)
        if cardnumber>10:
            surface.blit(facescards[cardnumber,cardsuit],pygame.Rect(positionx,positiony,100,175))
        else:
            for position in positions[cardnumber]:
                img = font.render(suit[cardsuit],True,pygame.Color(0, 0, 255))
                surface.blit(img, pygame.Rect(positionx+position[0], positiony+position[1], img.get_width(), img.get_height()))
    def draw_card(self):
        global cards
        self.screen.fill(pygame.Color(0, 0, 255))
        smallfont = pygame.font.SysFont('dejavuserif', 15)
        text = smallfont.render(f'{self.personname} | {self.points} \n {self.computername} | {self.computerspoints}' , True , pygame.Color(0, 0, 0))
        self.screen.blit(text , (600, 550))
        smallfon = pygame.font.SysFont('dejavuserif', 15)
        tex = smallfon.render(f'{self.personname} | {self.points} \n {self.computername} | {self.computerspoints}' , True , pygame.Color(0, 0, 0))
        self.screen.blit(tex , (600, 550))
        for i, card in enumerate(self.countingpileforperson):
            self.draw_cards(card[0], card[1], 470+i*5, 400, self.screen, False)
        for i, card in enumerate(self.countingpileforcomputer):
            self.draw_cards(card[0], card[1], 470+i*5, 400-50, self.screen, False)
        if self.computerschoice:
            for cardnumber, cardsuit, _ in self.countingpileforperson:
                self.draw_cards(cardnumber, cardsuit, 400, 275, self.screen, False)
            if self.computerschoice=='10h' or self.computerschoice=='10d' or self.computerschoice=='10s' or self.computerschoice=='10c':
                self.draw_cards(self.computerschoice[0]+self.computerschoice[1], self.computerschoice[2], 400, 275, self.screen, False)
            else:
                self.draw_cards(self.computerschoice[0][0], self.computerschoice[0][1], 400, 250, self.screen, False)
        if self.currentmode==CHECK_POINTS:
            calculate_the_score=pygame.Rect(350, 525, 100, 50)
            pygame.draw.rect(self.screen, pygame.Color(25, 60, 25), calculate_the_score)
            pygame.Rect(400+50, 800-275, 100, 50)
            calculatepreview=pygame.font.SysFont('dejavuserif', 20)
            calculate_text=calculatepreview.render('Calculate', True, pygame.Color(0, 0, 0))
            self.screen.blit(calculate_text, (350, 535))
            textpreview=pygame.font.SysFont('dejavuserif', 20)
            text_text=textpreview.render('score', True, pygame.Color(0, 0, 0))
            self.screen.blit(text_text, (350, 550))
        if self.theturncard:
            (theturncard_card, theturncard_suit, _) = self.theturncard
            self.draw_cards(theturncard_card, theturncard_suit, 0, 313.5, self.screen, False) 
        for index, (card, cardsuit, _) in enumerate(cards):
            if self.currentdrawing=='drawcomputercards':
                draw_facedown_cards(facedowncard, 100+50*index, 50, self.screen)
            elif self.currentdrawing=='drawdeck':
                for i in range(0,52-12):
                    #52 is the number of cards and 12 is the number of cards that the computer has already dealt.
                    draw_facedown_cards(facedowncard, 200+(i*10), 400, self.screen) 
                    draw_facedown_cards(facedowncard, 100+50*index, 50, self.screen)
            self.draw_cards(card, cardsuit, 100+50*index, 575, self.screen, index in self.selectedcards)
            if len(self.selectedcards)==2:
                    smallfont=pygame.font.SysFont('dejavuserif',15)
                    text = smallfont.render('Send to crib',True,pygame.Color(0, 0, 0))
                    self.screen.blit(text , (700, 700))    
        rectu=pygame.Rect(800/2, 800/2, 100, 100)
        pygame.draw.rect(self.screen, pygame.Color(0, 255, 0), rectu)
        messagepreview=pygame.font.SysFont('dejavuserif', 14)
        if self.message=="Pick a card":
            calculate_message=messagepreview.render(self.message, True, pygame.Color(0, 0, 0))
            self.screen.blit(calculate_message, (400, 400))
        elif self.message=="your opponent can't play so it is your turn":
            for index, words in enumerate(["your opponent", "can't play so", "it's your turn"]):
                calculate_message=messagepreview.render(words, True, pygame.Color(0, 0, 0))
                self.screen.blit(calculate_message, (400, 400 + index*14))
        elif self.message=="you cannot play that card, play a different card":
            for index, words in enumerate(["you cannot", "play tht card", "play a", "different card"]):
                calculate_message=messagepreview.render(words, True, pygame.Color(0, 0, 0))
                self.screen.blit(calculate_message, (400, 400 + index*14))
        elif self.message==f"Pick 2 cards to throw away and make the crib. {self.computername} is also going to pick 2 cards":
            for index, words in enumerate(["Pick 2 cards", "to throw away", "and make the", f"crib {self.computername}", "is also going to", "pick 2 cards"]):
                calculate_message=messagepreview.render(words, True, pygame.Color(0, 0, 0))
                self.screen.blit(calculate_message, (400, 400 + index*14))
        pygame.display.update()
    def godeclaration(self):
        self.pegginglist=[]
        self.countingpileforcomputer=[]
        self.countingpileforperson=[]
        personvalid=self.validcards(cards)
        cardscomputervalid=self.validcards(hand)
        if len(personvalid)==0 and len(cardscomputervalid)==0:
            self.currentmode=CHECK_POINTS
        else:
            pygame.event.post(pygame.event.Event(turnevent))
    def event_loop(self):
        while True:
            event=pygame.event.get()
            if len(event)>0:
                for events in event:
                    if events.type==pygame.MOUSEBUTTONUP:
                        posx, posy = pygame.mouse.get_pos()
                        if cribbage_game.currentmode==CHOOSING:
                            self.message=f"Pick 2 cards to throw away and make the crib. {self.computername} is also going to pick 2 cards"
                            if (selectedcard := clickcard(posx, posy, 6))!=None:
                                card=cards[selectedcard]
                                if selectedcard in self.selectedcards:
                                    self.selectedcards.remove(selectedcard)
                                elif len(self.selectedcards)<2:
                                    self.selectedcards.append(selectedcard)
                            elif clickbutton(posx, posy, "sendtocrib"):
                                if len(self.selectedcards)==2:
                                    self.currentmode=PICK_TURN_CARD
                                    self.criblist.append(self.selectedcards)
                                    self.selectedcards.sort()
                                    del cards[self.selectedcards[1]]
                                    del cards[self.selectedcards[0]]
                                    self.currentdrawing='drawdeck'
                                    self.selectedcards=[]
                                    if self.whosturn==YOU:
                                        continue
                                    else:
                                        self.currentdrawing='drawcomputercards'
                                        self.theturncard=random.sample(cardlist, 1)[0]
                                        cardlist.remove(self.theturncard)
                                        self.currentmode=PEGGING
                                        pygame.event.post(pygame.event.Event(turnevent))
                        elif self.currentmode==PICK_TURN_CARD:
                            if posy>=400 and posy<=575 and posx>=200 and posx<=690:
                                self.currentdrawing='drawcomputercards'
                                self.theturncard=random.sample(cardlist, 1)[0]
                                cardlist.remove(self.theturncard)
                                self.currentmode=PEGGING
                            else:
                                self.message="Pick a card"
                        elif self.currentmode==PEGGING:
                            if self.whosturn==YOU:
                                self.personpegging(posx, posy, self.pegginglist)                                
                        elif self.currentmode==CHECK_POINTS:
                            # Two error to fix:
                            # - Button "Calculate the score" does not disappear when job is done
                            # - There is only one round, go up until someone hits 120 points
                            yesorno=clickbutton(posx, posy, "calculate score")
                            if yesorno==True:
                                mostpoints=check_points(self.countingpileforperson)
                                self.points+=mostpoints
                                mostcomputerpoints=check_points(self.countingpileforcomputer)
                                self.computerspoints+=mostcomputerpoints
                    elif events.type == turnevent:
                        self.computerpegging(self.pegginglist)
                    elif events.type == timerevent:
                        removedumaque(False)
            self.draw_card()
    def validcards(self, cards):
        global thecardsthatarevalid
        total=self.peggingTotal(self.pegginglist)
        thecardsthatarevalid = [card for card in cards if card[-1] + total <=31]
        return thecardsthatarevalid
    def personpegging(self, posx : float, posy : float, listofpeggingcards : list):
        peggingcard=clickcard(posx, posy, len(cards))       
        total= self.peggingTotal(self.pegginglist)
        cardsthatarevalid = [index for index, card in enumerate(cards) if card[-1] + total <=31]
        computeruvalid=self.validcards(hand)
        if len(cardsthatarevalid)>0:
            if peggingcard in cardsthatarevalid:
                card = cards[peggingcard]
                self.countingpileforperson.append(card)
                self.pegginglist.append(card)
                del cards[peggingcard]
                somepoints=peggingpoints(self.pegginglist)
                self.points+=somepoints
                if somepoints > 0:
                    thethetotal=self.peggingTotal(self.pegginglist)
                    engine.say(thethetotal)
                    engine.runAndWait()
                self.whosturn=COMPUTER
                pygame.event.post(pygame.event.Event(turnevent))
            else:
                self.message="you cannot play that card, play a different card"
        else:
            if len(computeruvalid)>0:
                pygame.event.post(pygame.event.Event(turnevent))
            else:
                self.computerspoints+=1
                self.godeclaration()
    def peggingTotal(self, listofpeggingcards):
        return functools.reduce(lambda x,y: x+y, [x[2] for x in listofpeggingcards], 0)
    def computerpegging(self, listofpeggingcards):
        total=self.peggingTotal(listofpeggingcards)
        validcomputer=self.validcards(cards)
        computercardsthatarevalid = [card for card in hand if card[-1] + total <=31]
        if len(computercardsthatarevalid)>0:
            computerspick=(random.sample(computercardsthatarevalid, 1)[0])
            self.pegginglist.append(computerspick)
            self.countingpileforcomputer.append(computerspick)
            somepoints=peggingpoints(self.pegginglist)
            self.computerspoints+=somepoints
            del hand[hand.index(computerspick)]
            self.countingpileforcomputer.append(computerspick)
            self.whosturn=YOU
        else:
            if len(validcomputer)>0:
                self.message="your opponent can't play so it is your turn"
                self.whosturn=YOU
            else:
                self.points+=1
                self.godeclaration()            
def intstr(card):
    if card=="10s"or card=="10c"or card=="10h"or card=="10d":
        cardnumber=10
    else:
        cardnumber=card[0]
    cardsuit=card[-1]
    if cardnumber=="q":
        cardnumber=12
    if cardnumber=="j":
        cardnumber=11
    if cardnumber=="k":
        cardnumber=13
    if cardnumber=="a":
        cardnumber=1
    cardnumber=int(cardnumber)
    value=10 if cardnumber>=10 else cardnumber
    return cardnumber, cardsuit, value
cardlist=[intstr(card)for card in["as","ah","ad","ac","2d","2h","2s","2c","3h","3d","3s","3c","4h","4c","4s","4d","5h","5d","5s","5c","6h","6d","6s","6c","7h","7d","7s","7c","8h","8d","8s","8c","9h","9d","9s","9c","10h","10d","10s","10c","jh","js","jd","jc","qh","qd","qs","qc","kh","kd","ks","kc"]]
hand=random.sample(cardlist, 4)
print(hand)
facedowncard=pygame.image.load(os.path.join(current_directory, "playing-card-back.jpg"))
facescards={(cardnumber,suit): pygame.image.load(os.path.join(current_directory, f"pixil-frame-0({cardnumber}{suit}).png")) for cardnumber,suit,_ in cardlist if cardnumber>10}
def check_points(hand):
    pairs = 0
    for index1, (card1, _, _)in enumerate(hand):
        for index2, (card2, _, _)in enumerate(hand):
            if card1==card2:
                if index2>index1:
                    pairs+=2
    def add(total, remainingcards):
        if total==15:
            return 2
        elif total>15:
            return 0
        point=0
        for index,(_, _, card)in enumerate(remainingcards):
            point+=add(total+card,remainingcards[index+1:])
        for index3, (_, card3, _) in enumerate(hand):
            if hand[0][1]!=card3:
                if index3==len(hand)-1:
                    point+=4
                break
        else:
            point=point+5
        return point
    def run(lastcardseen, remainingcards, thecardsthatwevefound):
        point=0
        for index, (card, _, _) in enumerate(remainingcards):
            if lastcardseen==card-1 or lastcardseen==0:
                longer_points=run(card, remainingcards[0:index]+remainingcards[index+1:], thecardsthatwevefound+1)
                point += longer_points
                if thecardsthatwevefound>=3 and longer_points==0:
                    point += thecardsthatwevefound
        return point
    def nob():
        for card, suit, _ in hand[0:-1]:
            if card==11 and suit==hand[-1][1]:
                return 1
        return 0
    no=nob()
    ru=run(0, hand, 1)
    ad=add(0, hand)
    point=pairs+no+ru+ad
    return point
def shuffle(deck):
    for i, card in enumerate(deck):
        random_position=random.randint(0, len(deck))
        cardposition=deck[card]
        deck[card]=deck[random_position]
        deck[random_position]=cardposition
def draw_facedown_cards(card, positionx, positiony, surface):
    surface.blit(card, pygame.Rect(positionx, positiony, 100, 175))
def deal(deck : list):
    global cards
    cards=random.sample(deck, 6)
    print(cards)
    for card in cards:
        deck.remove(card)
def removedumaque(is_there_a_dumaque : Boolean):
    if is_there_a_dumaque==False:
        pass
    else:
        cribbage_game.rollingballs.remove('dumaque')
def clickcard(posx : Variable or int, posy : Variable or int, cardsinhand : int):
    posx=(posx-100)/50
    if posx > cardsinhand-1 and posx<cardsinhand+1: posx=cardsinhand-1
    if posx>=0 and posx<cardsinhand+1:
        if posy>575 and posy<750:
            posx=int(posx)
            return posx
    return None
def clickbutton(posx : Variable or int, posy : Variable or int, sendtocrib_or_calculate_score: str):
    if sendtocrib_or_calculate_score=="sendtocrib":
        if posx>700 and posx<785:
            if posy>700 and posy<785:
                return True
        return False
    elif sendtocrib_or_calculate_score=="calculate score":
        if posx>400-50 and posx<400+50:
            if posy<611 and posy>527:
                return True
        return False
def peggingpoints(listofpeggingcards):
    # Find points for pairs
    lastcard=listofpeggingcards[-1][0]
    returnation=0
    for i in range(0, len(listofpeggingcards)-1):
        if listofpeggingcards[-2-i][0]!=lastcard:
            returnation=i*(i+1)
            break
    else:
        returnation=(len(listofpeggingcards)-1)*(len(listofpeggingcards))
    # Find points for 15's
    total = functools.reduce(lambda x,y: x+y,[x[2] for x in listofpeggingcards])
    if total == 15: 
        returnation+=2
    elif total == 31:
        returnation+=2
        cribbage_game.godeclaration()
    # Find points for runs
    for i in range(0, len(listofpeggingcards)):
        sorted_cards = sorted([x[0] for x in listofpeggingcards[i:]])
        last = sorted_cards[0]
        for i in sorted_cards[1:]:
            if i == last+1:
                last = i
            else:
                break
        else:
            break
    if len(listofpeggingcards)-i >= 3:
        returnation += len(listofpeggingcards)-i
    return returnation
if __name__=='__main__':
    cribbage_game=CribbageGame()
    print("Let's play cribbage")
    time.sleep(2)
    suit={'c':'♣','h':'♥','d':'♦','s':'♠'}
    positions={8:[(32,26),(69,26),(20,49),(62,48),(24,88),(62,88),(23,132),(64,133)],1:[(39,68)],2:[(39,16),(39,127)],3:[(29,6),(32,127),(29,65)],4:[(15,19),(63,18),(15,115),(71,118)],5:[(15,19),(63,18),(15,115),(71,118),(42,69)],6:[(15,19),(63,18),(15,115),(71,118),(18,69),(64,69)],7:[(15,19),(63,18),(15,115),(71,118),(18,69),(64,69),(39,46)],9:[(32,26),(69,26),(20,49),(62,48),(24,88),(62,88),(23,132),(64,133),(42,67)],10:[(15,19),(63,18),(18,47),(67,47),(17,68),(68,69),(17,97),(67,93),(16,122),(68,123)]}
    removedumaque(True)
    deal(cardlist)
    cribbage_game.event_loop()
