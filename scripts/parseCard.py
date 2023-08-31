import requests
import resources as rc
from bs4 import BeautifulSoup
from pprint import pprint

def importPage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def decodePage(inputName):
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
    #for()

    return res

def printCardStatus(cardName):
    card = decodePage(cardName)
    card_vars = vars(card)
    pprint(card_vars, sort_dicts=False)
    print('\n')

printCardStatus('Ship_of_Fools^Epic')
printCardStatus('Call_of_Khrulhu')
printCardStatus('Ship_of_Fools')