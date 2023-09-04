import resources as rc

def loadStrategyTxt(stratName):
    stratPath = str(rc.INSTALLDIR) + '\\strategy\\' + stratName + '.txt'
    with open(stratPath) as stratFile:
        data = stratFile.read().replace('\n','').split(',')
    return data

def writeBuff(i, step):
    data = step.split(' ')
    str = '\n'+rc.TAB4+'if step['+i+']:\n'
    str += rc.TAB5+'step['+i+'] = lc.buffCard(\''+data[1]+'\', \''+data[3]+'\')'
    return str

def writeUse(i, step):
    data = step.split(' ')
    str = '\n'+rc.TAB4+'if step['+i+']:\n'
    
    if('^' in step):
        str += rc.TAB5+'step['+i+'] = lc.useCard(\''+data[1].split('^')[0]+'\', buffName=\''+data[1].split('^')[1]+'\''
    else:
        str += rc.TAB5+'step['+i+'] = lc.useCard(\''+data[1]+'\''
    
    if('on' in step):
        str += ', target='+data[3]+')'
    else:
        str += ')'

    str += '\n'+rc.TAB5+'continue'
    return str

def writePass(i):
    str = '\n'+rc.TAB4+'if step['+i+']:\n'
    str += rc.TAB5+'lc.clickButton(\'pass\')'
    return str

def parse(stratName):
    #Get strat data
    stratData = loadStrategyTxt(stratName)
    stepCount = len(stratData)

    #write header code
    outStr =       'import locate as lc\n\n'

    outStr +=      'def run():\n'
    outStr += rc.TAB1+'lc.initLibCards()\n'
    outStr += rc.TAB1+'while(True):\n'
    outStr += rc.TAB2+   'battleStarted = False\n'
    outStr += rc.TAB2+   'stepCount = ' + str(stepCount) + '\n'
    outStr += rc.TAB2+   'step = [True for i in range(stepCount)]\n'
    outStr += rc.TAB2+   'while(lc.battleInstance()):\n'
    outStr += rc.TAB3+      'if(battleStarted is False):\n'
    outStr += rc.TAB4+         'print(\'battleInstance() = True, initiating battle\')\n'
    outStr += rc.TAB4+         'battleStarted = True\n\n'

    outStr += rc.TAB3+      'if(lc.cardSelection()):\n'
    outStr += rc.TAB4+         'lc.findWindowLocation()\n'
    outStr += rc.TAB4+         'lc.resetFocus()\n'

    #write each step
    for step in stratData:
        i = str(stratData.index(step))
        if(step.split(' ')[0] == 'Buff'):
            outStr += writeBuff(i, step)
        elif(step.split(' ')[0] == 'Use'):
            outStr += writeUse(i, step)
        elif(step.split(' ')[0] == 'Pass'):
            outStr += writePass(i)

    #write final pass
    outStr += '\n\n'+rc.TAB4+'lc.clickButton(\'pass\')'

    #output into strategy.py
    path = rc.INSTALLDIR + '\\scripts\\strategy.py'
    with open(path, 'w') as stratFile:
        stratFile.write(outStr)