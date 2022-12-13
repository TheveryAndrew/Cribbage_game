import random
from netrc import __all__
import pyttsx3
from tkinter import Variable
import pygame
from xmlrpc.client import Boolean
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
class CribbageGame():
    def __init__(self):
        self.computerschoice=None
        self.currentdrawing='drawcomputercards'
        self.theturncard=None
        self.points=0
        self.computerspoints=0
        self.currentcrib=1#random.randint(0, 1)
        self.whosturn=self.currentcrib^1
        self.currentmode=CHOOSING
        self.selectedcards=[]
        self.pegginglist=[]
        self.message=[]
        self.countingpileforperson=[]
        self.rollingballs=['dumaque', 'babies', 'bellies']
        self.criblist=[]
        self.countingpileforcomputer=[]
        self.personprofile=0
        self.computerprofile=0
        self.personname=0
        self.computername=random.choices(['James','Robert','John','Michael','David','William','Richard','Joseph','Thomas','Charles', 'Christopher', 'Daniel', 'Mattew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua'])[0]
        self.screen = pygame.display.set_mode((800,800))
    def draw_card(self):
        global cards
        self.screen.fill(pygame.Color(0, 0, 255))
        smallfont = pygame.font.SysFont('dejavuserif', 15)
        text = smallfont.render(f'{self.personname} | {self.points} \n {self.computername} | {self.computerspoints}' , True , pygame.Color(0, 0, 0))
        self.screen.blit(text , (600, 550))
        smallfon = pygame.font.SysFont('dejavuserif', 15)
        tex = smallfon.render(f'{self.personname} | {self.points} \n {self.computername} | {self.computerspoints}' , True , pygame.Color(0, 0, 0))
        self.screen.blit(tex , (600, 550))
        if self.computerschoice:
            for cardnumber, cardsuit, _ in self.countingpileforperson:
                draw_cards(cardnumber, cardsuit, 400, 275, self.screen, False)
            if self.computerschoice=='10h' or self.computerschoice=='10d' or self.computerschoice=='10s' or self.computerschoice=='10c':
                draw_cards(self.computerschoice[0]+self.computerschoice[1], self.computerschoice[2], 400, 275, self.screen, False)
            else:
                draw_cards(self.computerschoice[0][0], self.computerschoice[0][1], 400, 250, self.screen, False)
        if self.currentmode==CHECK_POINTS:
            calculate_the_score=pygame.Rect(350, 525, 100, 50)          
            pygame.draw.rect(self.screen, pygame.Color(25, 60, 25), calculate_the_score)
            pygame.Rect(400+50, 800-275, 100, 50)
            #posy>400-50 and posy<400+50:
            #if posx<800-275 and posx>800-275-50:
            calculate_text_preview=pygame.font.SysFont('dejavuserif', 20)
            calculate_text=calculate_text_preview.render('Calculate score', True, pygame.Color(0, 0, 0))
            self.screen.blit(calculate_text, (400, 550))
        if self.theturncard:
            (theturncard_card, theturncard_suit, _) = self.theturncard
            draw_cards(theturncard_card, theturncard_suit, 0, 313.5, self.screen, False) 
        for index, (card, cardsuit, _) in enumerate(cards):
            if self.currentdrawing=='drawcomputercards':
                draw_facedown_cards(facedowncard, 100+50*index, 50, self.screen)
            elif self.currentdrawing=='drawdeck':
                for i in range(0, 52-12):
                    #52 is the number of cards and 12 is the number of cards that the computer has already dealt.
                    draw_facedown_cards(facedowncard, 200+(i*10), 400, self.screen) 
                    draw_facedown_cards(facedowncard, 100+50*index, 50, self.screen)
            draw_cards(card, cardsuit, 100+50*index, 575, self.screen, index in self.selectedcards)
            if len(self.selectedcards)==2:
                    smallfont = pygame.font.SysFont('dejavuserif',15)
                    text = smallfont.render('Send to crib' , True , pygame.Color(0, 0, 0))
                    self.screen.blit(text , (700, 700))
        rectu=pygame.Rect(800/2, 800/2, 100, 100)
        pygame.draw.rect(self.screen, pygame.Color(0, 255, 0), rectu)
        pygame.display.update()
    def godeclaration(self):
        self.pegginglist=[]
        self.countingpileforcomputer=[]
        self.countingpileforperson=[]
    def event_loop(self):
        while True:
            event=pygame.event.get()
            if len(event)>0:
                for events in event:
                    if events.type==pygame.MOUSEBUTTONUP:
                        posx, posy = pygame.mouse.get_pos()
                        if cribbage_game.currentmode==CHOOSING:
                            message=f"Pick 2 cards to throw away and make the crib. {self.computername} is also going to pick 2 cards"
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
                                        self.computerpegging(self.pegginglist)
                        elif self.currentmode==PICK_TURN_CARD:
                            if posy>=400 and posy<=575 and posx>=200 and posx<=690:
                                self.currentdrawing='drawcomputercards'
                                self.theturncard=random.sample(cardlist, 1)[0]
                                cardlist.remove(self.theturncard)
                                self.currentmode=PEGGING
                            else:
                                message="Pick a card"
                        elif self.currentmode==PEGGING:
                            if self.whosturn==YOU:
                                self.personpegging(posx, posy, self.pegginglist)
                        elif self.currentmode==CHECK_POINTS:
                            mostpoints=check_points(cards)
                            self.points+=mostpoints
                            print(f"We are checking points! Now person has {self.points}")
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
                    print(f"Total: {thethetotal}")
                    engine.runAndWait()

                print(f"{card} is person's pick")
                print(f"Your points: {self.points}, Computer's points: {self.computerspoints}")
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
            somepoints=peggingpoints(self.pegginglist)
            self.computerspoints+=somepoints
            print(f"{computerspick} is computer's pick")
            print(f"Your points: {self.points}, Computer's points: {self.computerspoints}")
            del hand[hand.index(computerspick)]
            self.countingpileforcomputer.append(computerspick)
            self.whosturn=YOU
        else:
            if len(validcomputer)>0:
                self.message="your opponent can't play so it is your turn"
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
facedowncard=pygame.image.load("playing-card-back.jpg")
facescards={(cardnumber,suit): pygame.image.load(f"pixil-frame-0({cardnumber}{suit}).png") for cardnumber,suit,_ in cardlist if cardnumber>10}
def check_points(hand):
    for index1, (card1, _, _)in enumerate(hand):
        for index2, (card2, _, _)in enumerate(hand):
            if card1==card2:
                if index2>index1:
                    points=points+2
    def add(total, remainingcards):
        if total==15:
            return 2
        elif total>15:
            return 0
        point=0
        for index,(_, _, card)in enumerate(remainingcards):
            point+=add(total+card,remainingcards[index+1:])
            return point
        for index3, (_, card3, _) in enumerate(hand):
            if hand[0][1]!=card3:
                if index3==len(hand)-1:
                    points+=4
                break
        else:
            points=points+5
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
    points+=ad
    points+=ru
    points+=no
    return points
def shuffle(deck):
    for i, card in enumerate(deck):
        random_position=random.randint(0, len(deck))
        cardposition=deck[card]
        deck[card]=deck[random_position]
        deck[random_position]=cardposition
def draw_cards(cardnumber : str, cardsuit : str, positionx : float, positiony : float, surface : Variable, highliting : Boolean):
    global selectedcards
    if cribbage_game.currentmode!=CHOOSING:
        if cribbage_game.currentcrib==YOU:
            draw_facedown_cards(pygame.image.load("/home/absmall/Downloads/playing-card-back.jpg"), 100, 400, cribbage_game.screen)
        else:
            draw_facedown_cards(pygame.image.load("/home/absmall/Downloads/playing-card-back.jpg"), 100, 250, cribbage_game.screen)
    drawrectangle=pygame.Rect(positionx, positiony, 100, 175)
    if highliting==True:
        redrect=pygame.Rect(positionx-2, positiony-2, 104, 179)
        pygame.draw.rect(surface, pygame.Color(255, 0, 0), redrect)
    pygame.draw.rect(surface, pygame.Color(0, 255, 0), drawrectangle)
    font = pygame.font.SysFont('dejavuserif', 18)
    if cardnumber > 10:
        surface.blit(facescards[cardnumber, cardsuit], pygame.Rect(positionx, positiony, 100, 175))
    else:
        for position in positions[cardnumber]:
            img = font.render(suit[cardsuit], True, pygame.Color(0, 0, 255))
            surface.blit(img, pygame.Rect(positionx+position[0], positiony+position[1], img.get_width(), img.get_height()))
def draw_facedown_cards(card, positionx, positiony, surface):
    surface.blit(card, pygame.Rect(positionx, positiony, 100, 175))
def deal(deck : list):
    global cards
    cards=random.sample(deck, 6)
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
            if posy<800-275 and posy>800-275-50:
                return True
        return False
def peggingpoints(listofpeggingcards):
    # Find points for pairs
    lastcard=listofpeggingcards[-1][0]
    returnation=0
    for i in range(0, len(listofpeggingcards)-1):
        if listofpeggingcards[-2-i][0] != lastcard:
            returnation = i*(i+1)
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
if __name__ == '__main__':
    cribbage_game = CribbageGame()
    print("Let's play cribbage")
    time.sleep(2)
    suit={'c':'♣','h':'♥','d':'♦','s':'♠'}
    positions={8:[(32,26),(69,26),(20,49),(62,48),(24,88),(62,88),(23,132),(64,133)],1:[(39,68)],2:[(39,16),(39,127)],3:[(29,6),(32,127),(29,65)],4:[(15,19),(63,18),(15,115),(71,118)],5:[(15,19),(63,18),(15,115),(71,118),(42,69)],6:[(15,19),(63,18),(15,115),(71,118),(18,69),(64,69)],7:[(15,19),(63,18),(15,115),(71,118),(18,69),(64,69),(39,46)],9:[(32,26),(69,26),(20,49),(62,48),(24,88),(62,88),(23,132),(64,133),(42,67)],10:[(15,19),(63,18),(18,47),(67,47),(17,68),(68,69),(17,97),(67,93),(16,122),(68,123)]}
    removedumaque(True)
    deal(cardlist)
    cribbage_game.event_loop()
