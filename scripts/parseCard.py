import requests
import resources as rc
from bs4 import BeautifulSoup
from pprint import pprint
import fnmatch
import math

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
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def decodeSpell(inputName):
    res = rc.LibCard()

    #Determine buffs or not
    if '^' in inputName:
        res.originalName = inputName.split('^')[0]
        res.buffName = inputName.split('^')[1]
    else:
        res.originalName = inputName
        res.buffName = ''

    #Get page HTML
    res.spellURL = rc.WIKIURL + '/wiki/Spell:' + res.originalName
    cardHTML = importPage(res.spellURL)

    #Get card name
    res.cardName = str(cardHTML.find(id='firstHeading')).split('Spell:')[1].split('<')[0]

    if '^' in inputName:
        res.cardName = res.cardName + '^' + res.buffName

    #iterate through images
    iURL_found = False
    school_found = False
    shadowPip_found = False
    allImages = cardHTML.find_all('a', class_='image')
    for ele in allImages:
        #Get url of image on wiki
        if(iURL_found is False and res.originalName in str(ele) and res.buffName in str(ele)):
            res.imgURL = rc.WIKIURL + str(ele).split('src=\"')[1].split('\"')[0]
            iURL_found  = True
        #Get school of card
        elif(school_found is False and any(sch in str(ele) for sch in rc.SCHOOLS)):
            res.school = str(ele).split('(Icon) ')[1].split('.')[0]
            school_found = True
        #Get pip cost
        elif('Pip' in str(ele)):
            if('Shadow' in str(ele)):
                res.shadowPipCost = str(ele.parent.text).strip()
                shadowPip_found = True
            elif(shadowPip_found is False and any(sch in str(ele) for sch in rc.SCHOOLS)):
                res.schoolPipCost = str(ele.parent.text).strip()
            else:
                regularPipCost = str(ele.parent.text).strip()
            
            if(regularPipCost == "X"): #Account for all pips spells
                res.regularPipCost = -1
            else:
                res.regularPipCost = regularPipCost
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
            res.desc = str(ele).split('>')[1].split('<')[0]
            break

    #Populate card values based on type
    populateValues(res)

    return res

def populateValues(card: rc.LibCard):
    dList = str(card.desc).split(' ')
    print(dList)
    if(card.buffName != ""): #Apply buff values to card
        buffCard = decodeSpell(card.buffName)
        card.buffDamage   = buffCard.buffDamage
        card.buffAccuracy = buffCard.buffAccuracy
        card.buffPierce   = buffCard.buffPierce
        card.buffHeal     = buffCard.buffHeal
        card.buffPercent  = buffCard.buffPercent
        card.buffProtect  = buffCard.buffProtect
        card.buffDelay    = buffCard.buffDelay
        card.addPips      = buffCard.addPips
        card.buffCloak    = buffCard.buffCloak
    for tp in card.type: #Iterate through each type assigned to the card
        print(tp)
        if(tp == 'Damage Spell'): #Damage Spell
            for word in dList:
                if(word == 'Deals'):
                    value = dList[dList.index('Deals')+1]
                    print(value)
                    if('-' in value):
                        card.minDamage = int(str(value).split('-')[0].replace(',',''))
                        card.maxDamage = int(str(value).split('-')[1].replace(',',''))
                    else:
                        card.minDamage = int(value.replace(',',''))
                        card.maxDamage = int(value.replace(',',''))
                if(word == 'and' and 'Rounds' in dList): #DOT Spells
                    value = int(dList[dList.index('and')+1])
                    card.rounds = int(dList[dList.index('Rounds')-1])
                    card.totalDOT = value + card.buffDamage
                    card.roundDOT = math.floor(card.totalDOT/card.rounds)
        elif(tp == "Steal Spell"): #Steal Spell
            for word in dList:
                if(word == 'Deals'):
                    value = dList[dList.index('Deals')+1]
                    print(value)
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
                    card.buffHeal = math.ceil(card.buffDamage*multiplier)
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


def printCardStatus(cardName):
    card = decodeSpell(cardName)
    card_vars = vars(card)
    pprint(card_vars, sort_dicts=False)
    print('\n')

printCardStatus('Fire_Elf^Epic')