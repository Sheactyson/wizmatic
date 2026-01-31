import os

#Formatting constants
TAB1 = '    '
TAB2 = '        '
TAB3 = '            '
TAB4 = '                '
TAB5 = '                    '

#Class used for parsing cards from wiki
class LibCard:
    def __init__(self):
        self.spellURL: str = "None"
        self.imgPath: str = "None"
        self.name: str = "None"
        self.desc: str = "None"
        self.type: list = []
        self.school: str = "None"
        self.regularPipCost: int = 0
        self.schoolPipCost: int = 0
        self.shadowPipCost: int = 0
        self.accuracy: int = 0
        self.pierce: int = 0
        self.damage: int = 0 
        self.minDamage: int = -1
        self.perPip: int = 0
        self.heal: int = 0
        self.lifesteal: float = 0
        self.rounds: int = 0
        self.DOT: int = 0
        self.HOT: int = 0
        self.targetPercent: int = 0
        self.selfPercent: int = 0
        
        self.damageSchools: list = []
        self.augmentType: list = []
        self.protect: bool = False
        self.delay: bool = False
        self.addPips: int = 0

#Class used for holding game state
class GameState:
    def __init__(self):
        self.initiative: str = "Unknown"
        self.slot: list = [GameSlot(),GameSlot(),GameSlot(),GameSlot(),GameSlot(),GameSlot(),GameSlot(),GameSlot()]

#Class used for holding game slots
class GameSlot:
    def __init__(self):
        self.active: bool = False
        self.name: str
        self.maxhealth: int
        self.currenthealth: int

#Important links/paths
INSTALLDIR = '/app'
WIKIURL = 'https://wizard101central.com'
TESSPATH = INSTALLDIR + '\\tesseract\\tesseract.exe'


#Categories of in-game content
SCHOOLS = ['Fire','Ice','Storm','Balance','Myth','Death','Life','Star','Sun','Moon','Shadow']
SPELL_TYPE_ICONS = ['Damage Spell','Healing Spell','Charm Spell','Aura Spell','Enchantment Spell','Polymorph Spell','Shadow Self Spell','Shadow Creature Spell','All Enemies Spell','Steal Spell','Ward Spell','Global Spell','Manipulation Spell','Mutate Spell']
BUFFS_ALL = ['Strong','Giant','Monstrous','Gargantuan','Colossal','Epic','Keen Eyes','Accurate','Sniper','Unstoppable','Extraordinary','Primordial','Radical','Sharpened Blade','Potent Trap','Aegis','Indemnity','Daybreaker','Nightbringer']
BUFFS_DAMAGE = ['Strong','Giant','Monstrous','Gargantuan','Colossal','Epic']
BUFFS_ACCURACY = ['Keen Eyes','Accurate','Sniper','Unstoppable','Extraordinary']
BUFFS_HEALING = ['Primordial','Radical']
BUFFS_PERCENT = ['Sharpened Blade','Potent Trap']
BUFFS_PROTECT = ['Aegis','Indemnity']
BUFFS_DELAY = ['Daybreaker','Nightbringer']
CHARMS = ['Healing','Accuracy']

#Locations of regions on 1920x1080 screen
DUEL_SLOT = [(94,1,232,116),(519,1,232,116),(945,1,232,116),(1370,1,232,116), #Located on screen in this
             (211,906,232,165),(627,906,232,165),(1043,906,232,165),(1459,906,232,165)] #orientation
DS_HEALTH = [(64,49,161,32),(66,104,154,32)] #0:slots 0-3, 1:slots 4-7
DS_NAME   = [(67,25,163,27),(70,82,152,27)]  #0:slots 0-3, 1:slots 4-7
HEALTH_REG = (21,935,127,33)
MANA_REG   = (118,979,89,33)
ENERGY_REG = (62,1001,61,28)