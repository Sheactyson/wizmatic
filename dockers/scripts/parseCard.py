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
    res = rc.LibCard()

    #Get card name
    res.cardName = inputName

    #Get page HTML
    res.spellURL = rc.WIKIURL + '/wiki/Spell:' + str(res.cardName).replace(' ','_')
    #cardHTML = importPage(res.spellURL)
    cardHTML = importLocal('Spell_' + res.cardName)

    #iterate through images
    iPath_found = False
    school_found = False
    shadowPip_found = False
    allImages = cardHTML.find_all('a', class_='image')
    for ele in allImages:
        #Get path of image in files
        if(iPath_found is False and res.cardName in str(ele)):
            res.imgPath = '/images/cards/' + res.cardName + '/' + res.cardName + '.png'
            iPath_found  = True
        #Get school of card
        elif(school_found is False and any(sch in str(ele) for sch in rc.SCHOOLS)):
            res.school = str(ele).split('(Icon) ')[1].split('.')[0]
            school_found = True
        #Get pip cost
        elif('Pip' in str(ele)):
            modEle = str(ele)
            if('src' in str(ele)): #Accounts for locally stored html issue
                modEle = str(ele).split('src')[0]

            if('Shadow' in modEle):
                res.shadowPipCost = int(str(ele.parent.text).strip())
                shadowPip_found = True
            elif(shadowPip_found is False and any(sch in modEle for sch in rc.SCHOOLS)):
                res.schoolPipCost = int(str(ele.parent.text).strip())
            else:
                regularPipCost = str(ele.parent.text).strip()
            
            if(regularPipCost == "X"): #Accounts for all pips spells
                res.regularPipCost = -1
            else:
                res.regularPipCost = int(regularPipCost)
        #Get type
        elif(any(icn in str(ele) for icn in rc.SPELL_TYPE_ICONS)):
            res.type.append(str(ele).split('title=\"')[1].split('\"')[0])

    #Get base accuracy
    accuracy_found = False
    containers = cardHTML.find_all('td')
    for cont in containers:
        if(accuracy_found is False and '%' in str(cont.string)):
            res.baseAccuracy = int(str(cont.string).replace('%',''))
            accuracy_found = True

    #Grab description
    desc_found = False
    containers = cardHTML.find_all('td', {'colspan': '2'})
    for ele in containers:
        if('Description' in str(ele)):
            desc_found = True
            continue
        elif(desc_found):         
            res.desc = str(ele).split('>')[1].split('<')[0].rstrip()
            break

    #Populate card values based on type
    populateValues(res)

    return res

def populateValues(card: rc.LibCard):
    dList = str(card.desc).split(' ')
    for tp in card.type: #Iterate through each type assigned to the card
        if(tp == 'Damage Spell'): #Damage Spell
            for word in dList:
                if(word == 'Deals'):
                    value = dList[dList.index('Deals')+1]
                    if('-' in value):
                        card.minDamage = int(str(value).split('-')[0].replace(',',''))
                        card.maxDamage = int(str(value).split('-')[1].replace(',',''))
                    else:
                        card.minDamage = int(value.replace(',',''))
                        card.maxDamage = int(value.replace(',',''))
                if(word == 'and' and 'Rounds' in dList): #DOT Spells
                    value = int(dList[dList.index('and')+1])
                    card.rounds = int(dList[dList.index('Rounds')-1])
                    card.totalDOT = value
                    card.roundDOT = math.floor(card.totalDOT/card.rounds)
        elif(tp == "Steal Spell"): #Steal Spell
            for word in dList:
                if(word == 'Deals'):
                    value = dList[dList.index('Deals')+1]
                    if('-' in value):
                        card.minDamage = int(str(value).split('-')[0].replace(',',''))
                        card.maxDamage = int(str(value).split('-')[1].replace(',',''))
                    else:
                        card.minDamage = int(value.replace(',',''))
                        card.maxDamage = int(value.replace(',',''))
                if(word == 'for'): #Sets the lifesteal amount
                    next = dList[dList.index('for')+1]
                    if(next == 'half'):
                        multiplier = 0.5
                    else:
                        multiplier = int(str(next).replace('%',''))/100
                    card.baseHeal = math.ceil(card.minDamage*multiplier)
        elif(tp == 'Enchantment Spell'): #Enchantment Spell
            if(card.school == "Sun"):
                if(card.cardName in rc.BUFFS_DAMAGE):
                    value = str(card.desc).split('Damage')[0].replace('+','')
                    card.buffDamage = int(value)
                if(card.cardName in rc.BUFFS_ACCURACY):
                    value = str(card.desc).split('%')[0].replace('+','')
                    card.buffAccuracy = int(value)
                    if('Piercing' in card.desc):
                        value = str(card.desc).split('%')[1].split('+')[1]
                        card.buffPierce = int(value)
                if(card.cardName in rc.BUFFS_HEALING):
                    value = str(card.desc).split('Healing')[0].replace('+','').replace(' ','')
                    card.buffHeal = int(value)
                if(card.cardName in rc.BUFFS_PERCENT):
                    value = str(card.desc).split('%')[0].replace('+','')
                    card.buffPercent = int(value)
                if(card.cardName in rc.BUFFS_PROTECT):
                    card.buffProtect = True
                if(card.cardName in rc.BUFFS_DELAY):
                    card.buffDelay = True
                    card.addPips = 4
                if(card.cardName == "Cloak"):
                    card.buffCloak = True

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

def printCardStatus(cardName):
    card = decodeSpell(cardName)
    card_vars = vars(card)
    pprint(card_vars, sort_dicts=False)
    print('\n')

def populateCardsFromHtml(keep=False):
    #Setup cards based on html directory
    directory = str(rc.INSTALLDIR) + '/html'
    fileLocation = str(rc.INSTALLDIR) + '/images/cards/LibCards.json'
    jsonFile = open(fileLocation, 'w')
    data_final = []

    for filename in os.listdir(directory):
        if('.html' in filename):
            modName = str(filename).split(' - ')[0].split('Spell_')[1]
            extractCardImagesFromHtmlDirectory(modName)
            card = decodeSpell(modName)
            jsonObj = json.dumps(card.__dict__)
            jsonDict = json.loads(jsonObj)
            data_final.append({modName: jsonDict})

    json.dump(data_final, jsonFile, ensure_ascii=False, indent=2)
    jsonFile.close()

def modifyVariantCardValues(modCard):
    #Extract the type of variant
    if('^' in modCard.cardName):
        variant = modCard.cardName.split('^')[1]
    else:
        return

    #Proceed based on variant type
    if(variant in rc.BUFFS_DAMAGE):
        if(modCard.rounds == 0): #Not DOT
            if(variant == 'Strong'):
                modCard.minDamage = modCard.minDamage + 100
                modCard.maxDamage = modCard.maxDamage + 100
        else: #Is DOT
            pass

    elif(variant in rc.BUFFS_PERCENT):
        pass

    elif(variant in rc.BUFFS_PROTECT):
        pass

    elif(variant in rc.BUFFS_ACCURACY):
        pass

    elif(variant in rc.BUFFS_HEALING):
        pass

    elif(variant in rc.BUFFS_DELAY):
        pass

    else:
        return