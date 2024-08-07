import os
import scripts.parseCard as pc
import scripts.resources as rc

#Input card info from wiki HTML
def convertHTMLtoDatabase():
    #Setup directory and html files loop
    dirHTML = str(rc.INSTALLDIR) + '/html'
    for filename in os.listdir(dirHTML):
        if('.html' in filename):
            modName = str(filename).split(' - ')[0].split('Spell_')[1]
            
            #Store card images from wiki
            pc.extractCardImagesFromHtmlDirectory(modName)

            #Store base card details from wiki
            baseCard = pc.decodeSpell(modName)

            #Modify card details concerning variants
            dirIMG = str(rc.INSTALLDIR) + '/images/cards/' + modName
            cardVariants = [] #Store all card variants here after looping through
            for filename in os.listdir(dirIMG):
                modCard = baseCard #Start with the base card
                
                modCard.cardName = filename.split('.')[0] #Update card name to reflect variant
                pc.modifyVariantCardValues(modCard) #Modify values

                if(modCard.cardName == 'Ship of Fools^Strong'): print(modCard.minDamage)

                cardVariants.append(modCard) #Add new variant to list