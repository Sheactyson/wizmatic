import resources as rc
import cv2
import numpy as np
import pyautogui as pg
import os
import json
import time

def initLibCards():
    global lib_cards
    filepath = str(rc.INSTALLDIR) + '\\images\\cards\\LibCards.json'

    with open(filepath) as jsonFile:
        lib_cards = json.load(jsonFile)

def findCard(cardName, buffName=''):
    cardPos = [-1,-1]
    
    if(buffName != ''):
        cardPath = rc.INSTALLDIR + '\\images\\cards\\' + cardName + '\\' + cardName + '^' + buffName + '.png'
    else:
        cardPath = rc.INSTALLDIR + '\\images\\cards\\' + cardName + '\\' + cardName + '.png'

    cardCenter = str(pg.locateCenterOnScreen(cardPath, confidence=0.8))

    if(cardCenter != 'None'):
        cardCenter = cardCenter.replace('Point(x=','').replace(',','').replace('y=','').replace(')','')
        cardPos[0] = cardCenter.split(' ')[0]
        cardPos[1] = cardCenter.split(' ')[1]

        if(buffName != ''):
            print(cardName + '^' + buffName + ' located at: ' + str(cardPos))
        else:
            print(cardName + ' located at: ' + str(cardPos))
    
    return cardPos

def findButton(buttonName):

    buttonPos = [-1,-1]
    buttonPath = rc.INSTALLDIR + '\images\\buttons\\' + buttonName + '.png'
    buttonCenter = str(pg.locateCenterOnScreen(buttonPath, confidence=0.8))

    if(buttonCenter != 'None'):
        buttonCenter = buttonCenter.replace('Point(x=','').replace(',','').replace('y=','').replace(')','')
        buttonPos[0] = buttonCenter.split(' ')[0]
        buttonPos[1] = buttonCenter.split(' ')[1]

        print(buttonName + ' located at: ' + str(buttonPos))

    return buttonPos

def useCard(cardName, buffName=''):
    i = 0
    loop = 1
    #If it is buffed, might not capture the card correctly first time and need to try multiple times(5)
    if(buffName != ''):
        loop = 5
        cardUsed = False

    while(i < loop and cardUsed is False):
        card1 = [-1,-1]
        
        card1 = findCard(cardName, buffName)
        if(card1[0] != -1):
            if(buffName != ''):
                print('Using card ' + cardName + '^' + buffName + '...')
            else:
                print('Using card ' + cardName + '...')
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.5)
            pg.click()
            pg.moveRel(0, 200, duration = 0.2)
            cardUsed = True
        else:
            if(buffName != ''):
                print(cardName + '^' + buffName + ' not found')
            else:
                print(cardName + ' not found')

        i+=1

def buffCard(cardName1, cardName2, availability=1):
    card1 = [-1,-1]
    card2 = [-1,-1]

    card1 = findCard(cardName1)
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
    else:
        print(cardName1 + ' NOT buffed with ' + cardName2)
    '''elif(availability == 0):
        card2 = findCard(cardName2)
        if(card2[0] != -1):
            pg.moveTo(int(card2[0]), int(card2[1]), duration = 0.5)
            pg.click()
            pg.moveTo(int(card1_nopips[0]), int(card1_nopips[1]), duration = 0.5)
            pg.click()
            pg.moveRel(0, 200, duration = 0.2)
            print(cardName1 + ' buffed with ' + cardName2 + ' (av=0)')
        else:
            print('Buff ' + cardName2 + ' unavailable!')'''

def clickButton(buttonName):
    button1 = [-1,-1]

    button1 = findButton(buttonName)
    if(button1[0] != -1):
        print('Clicking button ' + buttonName + '...')
        pg.moveTo(int(button1[0]), int(button1[1]), duration = 0.5)
        pg.click()
        pg.moveRel(0, 200, duration = 0.2)

def resetFocus():
    reset = [-1,-1]

    reset = findButton('friendslist')
    if(reset[0] != -1):
        print('Resetting window focus...')
        pg.moveTo(int(reset[0]), int(reset[1]), duration = 0.2)
        pg.moveRel(-200, 200, duration = 0.2)
        pg.click()

def inBattle():
    battle = [-1,-1]

    battle = findButton('pass')
    if(battle[0] != -1):
        print('inBattle() = True, initiating strategy')
        return True
    else:
        return False

initLibCards()
while(True):
    if(inBattle()):
        resetFocus()
        
        buffCard('Ship of Fools','Epic')
        useCard('Ship of Fools','Epic')

        clickButton('pass')
