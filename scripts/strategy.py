import locate as lc

def run():
    lc.initLibCards()
    while(True):
        battleStarted = False
        stepCount = 2
        step = [True for i in range(stepCount)]
        while(lc.battleInstance()):
            if(battleStarted is False):
                print('battleInstance() = True, initiating battle')
                battleStarted = True

            if(lc.cardSelection()):
                lc.findWindowLocation()
                lc.resetFocus()

                if step[0]:
                    step[0] = lc.buffCard('Ship_of_Fools', 'Epic')
                if step[1]:
                    step[1] = lc.useCard('Ship_of_Fools', buffName='Epic')
                    continue

                lc.clickButton('pass')