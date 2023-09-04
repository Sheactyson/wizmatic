import parseCard as pCard
import parseStrategy as pStrat

#Load from HTML
#pCard.populateCardsFromHtml(keep=True)

#Load strategy
pStrat.parse('shipoffools')
import strategy as strat

#Run strategy
strat.run()