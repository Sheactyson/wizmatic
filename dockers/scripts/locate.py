import scripts.resources as rc
import cv2
import pytesseract
import numpy as np
import pyautogui as pg
import json
import unidecode

#Startup functions
def initLibCards():
    global lib_cards
    filepath = str(rc.INSTALLDIR) + '\\images\\cards\\LibCards.json'

    with open(filepath) as jsonFile:
        lib_cards = json.load(jsonFile)

#View functions
def viewScreen():
    global screenshot
    screenshot = pg.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot),cv2.COLOR_RGB2BGR)

def viewWindow():
    global windowshot
    windowshot = pg.screenshot(region=(zeroPixel_left,zeroPixel_top,1920,1080))
    windowshot = cv2.cvtColor(np.array(windowshot),cv2.COLOR_RGB2BGR)
    #writepath = rc.INSTALLDIR + '\\images\\windowshot.png'
    #cv2.imwrite(writepath, windowshot)

def viewRegion(reg):
    left = reg[0]
    right = reg[0]+reg[2]
    top = reg[1]
    bottom = reg[1]+reg[3]
    regionshot = windowshot[top:bottom, left:right]
    writepath = rc.INSTALLDIR + '\\images\\gamestate\\regionshot.png'
    cv2.imwrite(writepath, regionshot)
    return regionshot

#Utility functions
def resetFocus():
    print('Resetting window focus...')
    pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)
    pg.click()

def findWindowLocation():
    global zeroPixel_left
    global zeroPixel_top
    buttonPath = rc.INSTALLDIR + '\images\\buttons\\shop.png'
    try:
        loc = pg.locateOnScreen(buttonPath, confidence=0.8)
    except:
        loc = 'None'
    if('None' not in str(loc)):
        zeroPixel_left = int(loc[0]-23)
        zeroPixel_top  = int(loc[1]-37)
        print('Window location found at: (' + str(zeroPixel_left) + ',' + str(zeroPixel_top) + ')')
    else:
        print('Window location not found')

def extractText(imageName, reg=(-1,-1,-1,-1), exType='none'):
    pytesseract.pytesseract.tesseract_cmd = rc.TESSPATH
    oimg = cv2.imread(imageName)
    
    if(reg[0]!=-1):
        left = reg[0]
        right = reg[0]+reg[2]
        top = reg[1]
        bottom = reg[1]+reg[3]
        img = oimg[top:bottom, left:right]

    if(exType == 'name'):
        img = cv2.resize(img, ((right-left)*5, (bottom-top)*5), interpolation=cv2.INTER_AREA)
    
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    text = pytesseract.image_to_string(img)
    if(text == ""):
        text = pytesseract.image_to_string(gray)
    
    text = unidecode.unidecode(text)
    text = str(text).strip().replace('‘','').replace(',','').replace('\n','').replace('\'','').replace('-','').replace(':','').rstrip()
    
    return text

#Find functions
def battleInstance():
    battle = [-1,-1]

    battle = findButton('spellBookMenu')
    if(battle[0] == -1):
        return True
    else:
        return False 

def cardSelection():
    battle = [-1,-1]

    battle = findButton('pass')
    if(battle[0] != -1):
        return True
    else:
        return False 
           
def findCard(cardName, buffName=''):
    cardPos = [-1,-1]
    
    if(buffName != ''):
        cardPath = rc.INSTALLDIR + '\\images\\cards\\' + cardName + '\\' + cardName + '^' + buffName + '.png'
    else:
        cardPath = rc.INSTALLDIR + '\\images\\cards\\' + cardName + '\\' + cardName + '.png'

    try:
        cardCenter = str(pg.locateCenterOnScreen(cardPath, confidence=0.8))
    except:
        cardCenter = 'None'

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
    try:
        buttonCenter = str(pg.locateCenterOnScreen(buttonPath, confidence=0.8))
    except:
        buttonCenter = 'None'

    if(buttonCenter != 'None'):
        buttonCenter = buttonCenter.replace('Point(x=','').replace(',','').replace('y=','').replace(')','')
        buttonPos[0] = buttonCenter.split(' ')[0]
        buttonPos[1] = buttonCenter.split(' ')[1]

        #print(buttonName + ' located at: ' + str(buttonPos))

    return buttonPos

def initiative():
    firstPath = rc.INSTALLDIR + '\\images\\gamestate\\opponentFirst.png'
    try:
        firstCenter = str(pg.locateCenterOnScreen(firstPath, confidence=0.8))
    except:
        firstCenter = 'None'

    if(firstCenter != 'None'):
        print('Opponents have initiative')
        first = 'oppo'
    else: 
        print('Allies have initiative')
        first = 'ally'

    return first

def isSlotActive(slot):
    slotPath = rc.INSTALLDIR + '\\images\\gamestate\\slot'+str(slot)+'.png'
    try:
        slotCenter = str(pg.locateCenterOnScreen(slotPath, confidence=0.7))
    except:
        slotCenter = 'None'

    if(slotCenter != 'None'):
        print('Slot'+str(slot)+' is occupied')
        return True
    else: 
        return False

#Interaction functions
def useCard(cardName, buffName='', target=-1):
    cardName = cardName.replace('_',' ')
    buffName = buffName.replace('_',' ')
    i = 0
    loop = 1
    #If it is buffed, might not capture the card correctly first time and need to try multiple times(5)
    if(buffName != ''):
        loop = 5

    while(i < loop):
        card1 = [-1,-1]
        
        card1 = findCard(cardName, buffName)
        if(card1[0] != -1):
            if(buffName != ''):
                print('Using card ' + cardName + '^' + buffName + '...')
            else:
                print('Using card ' + cardName + '...')
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.6)
            pg.click()

            if(target != -1):
                clickDuelSlot(target)
            else:
                pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)

            return False
        else:
            if(buffName != ''):
                print(cardName + '^' + buffName + ' not found')
            else:
                print(cardName + ' not found')

        i+=1
    
    return True

def buffCard(cardName1, cardName2, availability=1):
    cardName1 = cardName1.replace('_',' ')
    cardName2 = cardName2.replace('_',' ')

    card1 = [-1,-1]
    card2 = [-1,-1]

    card1 = findCard(cardName1)
    if(card1[0] != -1):
        card2 = findCard(cardName2)
        if(card2[0] != -1):
            pg.moveTo(int(card2[0]), int(card2[1]), duration = 0.6)
            pg.click()
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.6)
            pg.click()
            pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)
            print(cardName1 + ' buffed with ' + cardName2)
            return False
        else:
            print('Buff ' + cardName2 + ' unavailable!')
            return True
    else:
        print(cardName1 + ' NOT buffed with ' + cardName2)
        return True

def clickButton(buttonName):
    button1 = [-1,-1]

    button1 = findButton(buttonName)
    if(button1[0] != -1):
        print('Clicking button ' + buttonName + '...')
        pg.moveTo(int(button1[0]), int(button1[1]), duration = 0.6)
        pg.click()
        pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)
        return False
    
    return True

def clickDuelSlot(slot):
    slotLoc = pg.center(rc.DUEL_SLOT[slot])
    print('Clicking duel slot ' + str(slot) + '...')
    pg.moveTo(int(slotLoc[0])+zeroPixel_left, int(slotLoc[1])+zeroPixel_top, duration = 0.6)
    pg.click()
    pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)

def discardCard(cardName, buffName=''):
    cardName = cardName.replace('_',' ')
    buffName = buffName.replace('_',' ')
    i = 0
    loop = 1
    #If it is buffed, might not capture the card correctly first time and need to try multiple times(5)
    if(buffName != ''):
        loop = 5

    while(i < loop):
        card1 = [-1,-1]
        
        card1 = findCard(cardName, buffName)
        if(card1[0] != -1):
            if(buffName != ''):
                print('Discarding card ' + cardName + '^' + buffName + '...')
            else:
                print('Discarding card ' + cardName + '...')
            
            pg.moveTo(int(card1[0]), int(card1[1]), duration = 0.6)
            pg.click(button='RIGHT')
            pg.moveTo(zeroPixel_left+960, zeroPixel_top+200, duration = 0.1)

            return False
        else:
            if(buffName != ''):
                print(cardName + '^' + buffName + ' not found')
            else:
                print(cardName + ' not found')

        i+=1
    
    return True

#Gamestate functions
def initGameState():
    GS = rc.GameState() 

    while(cardSelection() == False): #wait until information is available
        continue
    else:
        GS.initiative = initiative()
        for slot in range(8):
            GS.slot[slot].active = isSlotActive(slot)
            if(GS.slot[slot].active == True):
                try:
                    slotInfo = grabSlotInfo(slot)
                    GS.slot[slot].name = slotInfo[0]
                    GS.slot[slot].maxhealth = slotInfo[1].split('/')[0]
                    GS.slot[slot].currenthealth = slotInfo[1].split('/')[0]
                    print(str(GS.slot[slot].name)+': '+str(GS.slot[slot].maxhealth))
                except:
                    continue

    return GS

def updGameState():
    pass

def grabSlotInfo(slot):
    viewWindow()
    viewRegion(rc.DUEL_SLOT[slot])
    regPath = rc.INSTALLDIR + '\\images\\gamestate\\regionshot.png'

    info = []

    #For name
    if(slot <=3):
        reg = rc.DS_NAME[0]
    else:
        reg = rc.DS_NAME[1]
    nameText = str(extractText(regPath, reg, 'name'))
    info.append(nameText)

    #For health
    if(slot <=3):
        reg = rc.DS_HEALTH[0]
    else:
        reg = rc.DS_HEALTH[1]
    healthPoints = str(extractText(regPath, reg))
    info.append(healthPoints)

    return info