import cv2
import numpy as np
import pyautogui as pg
import os

#Directory Setup
global installDirectory
installDirectory = os.path.abspath('wizmatic').replace('\wizmatic\\','\\')

def initImageLib():
    global images_cards
    global images_buttons

    images_cards = []
    images_buttons = []

    directory = installDirectory + '\images\cards'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            images_cards.append(directory + '\\' + filename)

    directory = installDirectory + '\images\\buttons'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            images_buttons.append(directory + '\\' + filename)


def viewScreen():
    global screenshot

    screenshot = pg.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot),cv2.COLOR_RGB2BGR)


def findCard(cardName):

    cardPos = [-1,-1]
    cardPath = installDirectory + '\images\cards\\' + cardName + '.png'
    cardCenter = str(pg.locateCenterOnScreen(cardPath, confidence=0.9))

    if(cardCenter != 'None'):
        cardCenter = cardCenter.replace('Point(x=','').replace(',','').replace('y=','').replace(')','')
        cardPos[0] = cardCenter.split(' ')[0]
        cardPos[1] = cardCenter.split(' ')[1]
        print(cardName + ' located at: ' + str(cardPos))
    
    return cardPos

def findButton(buttonName):

    buttonPos = [-1,-1]
    buttonPath = installDirectory + '\images\\buttons\\' + buttonName + '.png'
    buttonCenter = str(pg.locateCenterOnScreen(buttonPath, confidence=0.8))

    if(buttonCenter != 'None'):
        buttonCenter = buttonCenter.replace('Point(x=','').replace(',','').replace('y=','').replace(')','')
        buttonPos[0] = buttonCenter.split(' ')[0]
        buttonPos[1] = buttonCenter.split(' ')[1]

        print(buttonName + ' located at: ' + str(buttonPos))

    return buttonPos

def useCard(cardName):
    i = 0
    loop = 1
    if('_epic' in cardName):
        loop = 5

    while(i < loop):
        viewScreen()
        card1 = [-1,-1]
        
        card1 = findCard(cardName)
        if(card1[0] != -1):
            print('Using card ' + cardName + '...')
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.5)
            pg.click()
            pg.moveRel(0, 200, duration = 0.2)

        i+=1

def buffCard(cardName1, cardName2, availability=1):
    viewScreen()
    card1 = [-1,-1]
    card2 = [-1,-1]
    card1_nopips = [-1,-1]

    card1 = findCard(cardName1)
    card1_nopips = findCard(cardName1 + '_nopips')
    if(card1[0] != -1):
        card2 = findCard(cardName2)
        if(card2[0] != -1):
            pg.moveTo(int(card2[0]), int(card2[1]), duration = 0.5)
            pg.click()
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.5)
            pg.click()
            pg.moveRel(0, 200, duration = 0.2)
            print(cardName1 + ' buffed with ' + cardName2)
        else:
            print('Buff ' + cardName2 + ' unavailable!')
    elif((card1_nopips[0] != -1) and (availability == 0)):
        card2 = findCard(cardName2)
        if(card2[0] != -1):
            pg.moveTo(int(card2[0]), int(card2[1]), duration = 0.5)
            pg.click()
            pg.moveTo(int(card1_nopips[0]), int(card1_nopips[1]), duration = 0.5)
            pg.click()
            pg.moveRel(0, 200, duration = 0.2)
            print(cardName1 + ' buffed with ' + cardName2 + ' (av=0)')
        else:
            print('Buff ' + cardName2 + ' unavailable!')
    else:
        return

def clickButton(buttonName):
    viewScreen()
    button1 = [-1,-1]

    button1 = findButton(buttonName)
    if(button1[0] != -1):
        print('Clicking button ' + buttonName + '...')
        pg.moveTo(int(button1[0]), int(button1[1]), duration = 0.5)
        pg.click()
        pg.moveRel(0, 200, duration = 0.2)

def resetFocus():
    viewScreen()
    reset = [-1,-1]

    reset = findButton('friendslist')
    if(reset[0] != -1):
        print('Resetting window focus...')
        pg.moveTo(int(reset[0]), int(reset[1]), duration = 0.2)
        pg.moveRel(-200, 200, duration = 0.2)
        pg.click()

def inBattle():
    viewScreen()
    battle = [-1,-1]

    battle = findButton('pass')
    if(battle[0] != -1):
        print('inBattle() = True, initiating strategy')
        return True
    else:
        return False

initImageLib()
while(True):
    if(inBattle()):
        resetFocus()
        
        useCard('massdeathprism')

        buffCard('callofkhrulhu','epic')
        buffCard('scarecrow','epic')
        useCard('callofkhrulhu_epic')
        useCard('scarecrow_epic')

        clickButton('pass')
