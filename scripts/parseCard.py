import requests
import resources as rc
from bs4 import BeautifulSoup

def importPage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def decodePage(inputName):
    #Determine buffs or not
    if '^' in inputName:
        originalName = inputName.split('^')[0]
        buffName = inputName.split('^')[1]
    else:
        originalName = inputName
        buffName = ''

    #Get page HTML
    spellURL = rc.WIKIURL + '/wiki/Spell:' + originalName
    cardHTML = importPage(spellURL)

    #Get card name
    lib_cardName = str(cardHTML.find(id='firstHeading')).split('Spell:')[1].split('<')[0]

    if '^' in inputName:
        lib_cardName = lib_cardName + '^' + buffName

    #iterate through images
    iURL_found = False
    school_found = False
    allImages = cardHTML.find_all('a', class_='image')
    for ele in allImages:
        print(ele)
        #Get url of image on wiki
        if(iURL_found is False and originalName in str(ele) and buffName in str(ele)):
            lib_imgUrl = rc.WIKIURL + str(ele).split('src=\"')[1].split('\"')[0]
            iURL_found  = True
        #Get school of card
        if(school_found is False and any(sch in str(ele) for sch in rc.SCHOOLS)):
            lib_school = str(ele).split('(Icon) ')[1].split('.')[0]
            school_found = True
        #Get pip cost
        if('Pip' in str(ele)):
            if any(sch in str(ele) for sch in rc.SCHOOLS):
                lib_schoolPipCost = str(ele.parent.text).strip()
            else:
                lib_regularPipCost = str(ele.parent.text).strip()
                lib_schoolPipCost = 0

    results = lib_cardName+'\n'+lib_imgUrl+'\n'+lib_school+'\n'+lib_regularPipCost+'+'+lib_schoolPipCost
    print(results)

cardName = 'Ship_of_Fools'
decodePage(cardName)