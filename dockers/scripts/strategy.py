import scripts.locate as lc

def run():
    #lc.initLibCards()
    while(True):
        battleStarted = False
        stepCount = 3
        step = [True for i in range(stepCount)]
        while(lc.battleInstance()):
            if(battleStarted is False):
                print('battleInstance() = True, initiating battle')
                lc.findWindowLocation()
                GS = lc.initGameState()
                battleStarted = True

            if(lc.cardSelection()):
                print('cardSelection() = True, initiating strategy')
                lc.findWindowLocation()
                lc.resetFocus()

                if step[0]:
                    step[0] = lc.buffCard('Vampire', 'Epic')
                if step[1]:
                    step[1] = lc.useCard('Deathblade', target=7)
                    continue
                if step[2]:
                    step[2] = lc.useCard('Vampire', buffName='Epic', target=0)
                    continue

                lc.clickButton('pass')