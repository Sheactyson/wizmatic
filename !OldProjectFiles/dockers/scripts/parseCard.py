import requests
import scripts.resources as rc
from bs4 import BeautifulSoup
from pprint import pprint
import math
import json
import os
import cv2

Session_Active = False

def startSession():
    global ses
    global Session_Active
    ses = requests.Session()
    ses.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    Session_Active = True
    print('Web Session Started')

def importPage(url):
    global ses
    global Session_Active
    if(Session_Active is False):
        startSession()
    res = ses.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup

def importLocal(inputName):
    filepath = rc.INSTALLDIR + '/html/' + inputName + ' - Wizard101 Wiki.html'
    with open(filepath, encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'html5lib')
    return soup

def decodeSpell(inputName): #Modified for local, since pulling from web scraper is not working
    card = rc.LibCard()

    #Get card name
    card.name = inputName

    #Get page HTML
    card.spellURL = rc.WIKIURL + '/wiki/Spell:' + str(card.name).replace(' ','_')
    #cardHTML = importPage(card.spellURL)
    cardHTML = importLocal('Spell_' + card.name)

    #Output soup
    outPath = rc.INSTALLDIR + '/html/soup/' + card.name + '.html'
    file = open(outPath, 'w')
    file.write(str(cardHTML))

    #iterate through images
    iPath_found = False
    school_found = False
    shadowPip_found = False
    accuracy_found = False
    allImages = cardHTML.find_all('img')
    for ele in allImages:
        #Get path of image in files
        if(iPath_found is False and card.name in str(ele)):
            card.imgPath = '/images/cards/' + card.name + '/' + card.name + '.png'
            iPath_found  = True
        #Get school of card
        elif(school_found is False and any(sch in str(ele) for sch in rc.SCHOOLS)):
            card.school = str(ele).split('alt=\"')[1].split('\"')[0]
            school_found = True
        #Get pip cost
        elif('Pip' in str(ele)):
            modEle = str(ele)
            if('src' in str(ele)): #Accounts for locally stored html issue
                modEle = str(ele).split('src')[0]

            if('Shadow' in modEle):
                card.shadowPipCost = int(str(ele.parent.text).strip())
                shadowPip_found = True
            elif(shadowPip_found is False and any(sch in modEle for sch in rc.SCHOOLS)):
                card.schoolPipCost = int(str(ele.parent.text).strip())
            else:
                regularPipCost = str(ele.parent.text).strip()
            
            if(regularPipCost == 'X'): #Accounts for all pips spells
                card.regularPipCost = -1
            else:
                card.regularPipCost = int(regularPipCost)
        #Get accuracy
        elif(accuracy_found == False and 'Accuracy' in str(ele)):
            modEle = str(ele)
            if('src' in str(ele)): #Accounts for locally stored html issue
                modEle = str(ele).split('src')[0]

            card.accuracy = int(str(ele.parent.text).strip().replace('%',''))
            accuracy_found = True

        #Get type
        elif(any(icn in str(ele) for icn in rc.SPELL_TYPE_ICONS)):
            card.type.append(str(ele).split('title=\"')[1].split('\"')[0])

    #Grab description
    desc_found = False
    containers = cardHTML.find_all('td', {'colspan': '2'})
    for ele in containers:
        if('Description' in str(ele)):
            desc_found = True
            continue
        elif(desc_found):         
            card.desc = str(ele).split('>')[1].split('<')[0].rstrip()
            break

    #Populate card values based on type
    populateValues(card)

    return card

def populateValues(card: rc.LibCard):
    dList = str(card.desc).split(' ')
    for tp in card.type: #Iterate through each type assigned to the card
        if(tp == 'Damage Spell'): #Damage Spell
            for word in dList:
                if(word == 'Deals'):
                    if(dList[dList.index('Deals')+2] in rc.SCHOOLS):
                        card.damageSchools.append(dList[dList.index('Deals')+2])
                    value = dList[dList.index('Deals')+1]    
                    if('-' in value):
                        card.minDamage = int(str(value).split('-')[0].replace(',',''))
                        card.damage = int(str(value).split('-')[1].replace(',',''))
                    else:
                        card.minDamage = -1
                        card.damage = int(value.replace(',',''))

                if(word == 'per' and 'Rounds' in dList and card.regularPipCost == -1): #Per Pip Spells (DOT)
                    card.rounds = int(dList[dList.index('Rounds')-1])
                    card.perPip = card.damage
                    card.minDamage = -1
                    card.damage = 0
                elif(word == 'per' and card.regularPipCost == -1): #Per Pip Spells (No DOT)
                    card.perPip = card.damage
                    card.minDamage = -1
                    card.damage = 0

                if(word == 'and' and 'Rounds' in dList and card.regularPipCost != -1): #DOT Spells (Initial Hit)
                    value = int(dList[dList.index('and')+1])
                    card.rounds = int(dList[dList.index('Rounds')-1])
                    card.DOT = math.floor(value/card.rounds)
                elif(word == 'Rounds' and 'and' not in dList and card.regularPipCost != -1): #DOT Spells (No Initial Hit)
                    card.rounds = int(dList[dList.index('Rounds')-1])
                    card.DOT = math.floor(card.damage/card.rounds)
                    card.minDamage = -1
                    card.damage = 0

        elif(tp == 'Steal Spell'): #Steal Spell
            card.damageSchools.append('Steal')
            for word in dList:
                if(word == 'Deals'):
                    value = dList[dList.index('Deals')+1]
                    if('-' in value):
                        card.minDamage = int(str(value).split('-')[0].replace(',',''))
                        card.damage = int(str(value).split('-')[1].replace(',',''))
                    else:
                        card.minDamage = -1
                        card.damage = int(value.replace(',',''))
                if(word == 'for'): #Sets the lifesteal amount
                    next = dList[dList.index('for')+1]
                    if(next == 'half'):
                        multiplier = 0.5
                    else:
                        multiplier = int(str(next).replace('%',''))/100
                    card.lifesteal = multiplier
        elif(tp == 'Enchantment Spell'): #Enchantment Spell
            if(card.school == 'Sun'):
                if(card.name in rc.BUFFS_DAMAGE):
                    value = str(card.desc).split('Damage')[0].replace('+','')
                    card.minDamage = -1
                    card.damage = int(value)
                if(card.name in rc.BUFFS_ACCURACY):
                    value = str(card.desc).split('%')[0].replace('+','')
                    card.accuracy = int(value)
                    if('Piercing' in card.desc):
                        value = str(card.desc).split('%')[1].split('+')[1]
                        card.pierce = int(value)
                if(card.name in rc.BUFFS_HEALING):
                    value = str(card.desc).split('Healing')[0].replace('+','').replace(' ','')
                    card.heal = int(value)
                if(card.name in rc.BUFFS_PERCENT):
                    value = str(card.desc).split('%')[0].replace('+','')
                    card.targetPercent = int(value)
                if(card.name in rc.BUFFS_PROTECT):
                    card.protect = True
                if(card.name in rc.BUFFS_DELAY):
                    card.delay = True
                    card.addPips = 4
        elif(tp == 'Charm Spell'): #Charm Spell
            for word in dList:
                dList[dList.index(word)] = word.replace(',','')
                word = word.replace(',','')
                if('-' in word): #Negative charms
                    if('on' in dList and dList[dList.index('on')+1] == 'caster'):
                        card.selfPercent = int(word.replace('%',''))
                    else:
                        card.targetPercent = int(word.replace('%',''))
                if('+' in word): #Positive charms
                    if('on' in dList and dList[dList.index('on')+1] == 'caster'):
                        card.selfPercent = int(word.replace('%',''))
                    else:
                        card.targetPercent = int(word.replace('%',''))
                if('%' in word and dList[dList.index(word)+1] == 'Damage'): #Non-School
                    card.augmentType.append('Balance')
                if(word in rc.SCHOOLS and ('%' in dList[dList.index(word)-1] or dList[dList.index(word)-1] in rc.SCHOOLS or dList[dList.index(word)-2] in rc.SCHOOLS)): #Adds the correct school types to the list only if they are charm school types
                    if(word != 'Moon' and word != 'Sun' and word != 'Star' and word not in card.augmentType):
                        card.augmentType.append(word)
                if(word in rc.CHARMS and dList[dList.index(word)+1] == 'Charm'):
                    card.augmentType.append(word)


def extractCardImagesFromHtmlDirectory(cardName):
    saveLocation = str(rc.INSTALLDIR) + '/images/cards/' + cardName
    directory = str(rc.INSTALLDIR) + '/html/Spell_' + cardName + ' - Wizard101 Wiki_files'

    #Setup new directory
    os.chdir(str(rc.INSTALLDIR) + '/images/cards')
    try:
        os.mkdir(saveLocation)
        os.chdir(saveLocation)
    except:
        os.chdir(saveLocation)
    
    #Find and save necessary files
    for filename in os.listdir(directory):
        modName = str(filename) #Create modifiable filename
        if('(Spell)_'+str(cardName).replace(' ','_') in filename and '117px' not in filename and 'Tier' not in filename):
            #Remove pixel description
            if('px' in modName):
                modName = modName.split('px-')[1]
            #Reformat original name
            fromRep = '(Spell)_'+str(cardName).replace(' ','_')
            toRep = cardName
            modName = modName.replace(fromRep, toRep)
            #Reformat buff name
            if('(' in modName):
                modName = modName.replace('_(','^').replace('_',' ').replace(')','')
            #Save image
            imgPath = str(directory + '/' + filename)
            img = cv2.imread(imgPath)
            dim = (83, 127)
            scaledImg = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            cv2.imwrite(modName, scaledImg)

def printCardStatus(card):
    card_vars = vars(card)
    pprint(card_vars, sort_dicts=False)
    print('\n')

def modifyVariantCardValues(modCard):
    #Extract the type of variant
    if('^' in modCard.name):
        variant = modCard.name.split('^')[1]
        modCard.imgPath = '/images/cards/' + modCard.name.split('^')[0] + '/' + modCard.name + '.png'
    else:
        return

    #Proceed based on variant type
    if(variant in rc.BUFFS_DAMAGE):
        if(modCard.rounds == 0): #Not DOT
            damageRange = False #Boolean to check if the card has a range for damage
            if(modCard.minDamage != -1): damageRange = True
            if(variant == 'Strong'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 100
                modCard.damage = modCard.damage + 100
            elif(variant == 'Giant'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 125
                modCard.damage = modCard.damage + 125
            elif(variant == 'Monstrous'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 175
                modCard.damage = modCard.damage + 175
            elif(variant == 'Gargantuan'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 225
                modCard.damage = modCard.damage + 225
            elif(variant == 'Colossal'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 275
                modCard.damage = modCard.damage + 275
            elif(variant == 'Epic'):
                if(damageRange): modCard.minDamage = modCard.minDamage + 300
                modCard.damage = modCard.damage + 300
            else:
                print(modCard.name + ' is not a supported single damage buff')
            
            if('Steal Spell' in modCard.type): #Account for lifesteal spells
                modCard.heal = math.floor(modCard.damage/2)
        elif(modCard.rounds != 0): #Is DOT
            DOTinitial = True #Boolean for finding DOT type (has initial hit or not)
            if(modCard.damage == 0): DOTinitial = False
            if(variant == 'Strong'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 50
                    modCard.damage = modCard.damage + 50
                    modCard.DOT = modCard.DOT + math.floor(50/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(100/modCard.rounds)
            elif(variant == 'Giant'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 62
                    modCard.damage = modCard.damage + 62
                    modCard.DOT = modCard.DOT + math.floor(62/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(125/modCard.rounds)
            elif(variant == 'Monstrous'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 87
                    modCard.damage = modCard.damage + 87
                    modCard.DOT = modCard.DOT + math.floor(87/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(175/modCard.rounds)
            elif(variant == 'Gargantuan'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 112
                    modCard.damage = modCard.damage + 112
                    modCard.DOT = modCard.DOT + math.floor(112/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(225/modCard.rounds)
            elif(variant == 'Colossal'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 137
                    modCard.damage = modCard.damage + 137
                    modCard.DOT = modCard.DOT + math.floor(137/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(275/modCard.rounds)
            elif(variant == 'Epic'):
                if(DOTinitial):
                    modCard.minDamage = modCard.minDamage + 150
                    modCard.damage = modCard.damage + 150
                    modCard.DOT = modCard.DOT + math.floor(150/modCard.rounds)
                else:
                    modCard.DOT = modCard.DOT + math.floor(300/modCard.rounds)
            else:
                print(modCard.name + ' is not a supported DOT damage buff')
        else:
            print(modCard.name + ' is not a supported damage buff')

    elif(variant in rc.BUFFS_PERCENT):
        if(modCard.targetPercent != 0):
            modCard.targetPercent = modCard.targetPercent + 10
        if(modCard.selfPercent != 0):
            modCard.selfPercent = modCard.selfPercent + 10

    elif(variant in rc.BUFFS_PROTECT):
        modCard.protect = True

    elif(variant in rc.BUFFS_ACCURACY):
        if(variant == 'Keen Eyes'):
            modCard.accuracy = modCard.accuracy + 10
        elif(variant == 'Accurate'):
            modCard.accuracy = modCard.accuracy + 15
        elif(variant == 'Sniper'):
            modCard.accuracy = modCard.accuracy + 20
        elif(variant == 'Unstoppable'):
            modCard.accuracy = modCard.accuracy + 25
            modCard.pierce = modCard.pierce + 10
        elif(variant == 'Extraordinary'):
            modCard.accuracy = modCard.accuracy + 25
            modCard.pierce = modCard.pierce + 15
        else:
            print(modCard.name + ' is not a supported accuracy buff')

    elif(variant in rc.BUFFS_HEALING):
        if(variant == 'Primordial'):
            modCard.heal = modCard.heal + 100
        elif(variant == 'Radical'):
            modCard.heal = modCard.heal + 150
        else:
            print(modCard.name + ' is not a supported healing buff')

    elif(variant in rc.BUFFS_DELAY):
        pass

    else:
        return