import parseCard as pCard
import parseStrategy as pStrat

#Options
loadFromHTML = False
loadStrategy = False
runStrategy = True

#Load from HTML
if(loadFromHTML):
    pCard.populateCardsFromHtml(keep=True)

#Load strategy
if(loadStrategy):
    pStrat.parse('shipoffools')
    import strategy as strat
else:
    import strategy as strat

#Run strategy
if(runStrategy):
    strat.run()