import os

class LibCard:
    def __init__(self):
        self.cardName: str = "None"
        self.type: list = []
        self.desc: str = "None"
        self.spellURL: str = "None"
        self.imgPath: str = "None"
        self.school: str = "None"
        self.regularPipCost: int
        self.schoolPipCost: int
        self.shadowPipCost: int
        self.baseAccuracy: int

        self.minDamage: int
        self.maxDamage: int
        self.baseHeal: int
        self.baseTake: int
        
        self.totalDOT: int
        self.totalHOT: int
        self.roundDOT: int
        self.roundHOT: int
        self.rounds: int
        
        self.basePercent: int
        self.baseSelfPercent: int
        self.augmentSchools: list

        self.buffAccuracy: int
        self.buffPierce: int
        self.buffDamage: int
        self.buffHeal: int
        self.buffRoundDOT: int
        self.buffRoundHOT: int
        self.buffPercent: int
        self.buffProtect: bool
        self.buffCloak: bool
        self.buffDelay: bool
        self.addPips: int


INSTALLDIR = os.path.abspath('wizmatic').replace('\wizmatic\\','\\')
WIKIURL = 'https://wizard101central.com'

SCHOOLS = ['Fire','Ice','Storm','Balance','Myth','Death','Life','Star','Sun','Moon','Shadow']
SPELL_TYPE_ICONS = ['Damage Spell','Healing Spell','Charm Spell','Aura Spell','Enchantment Spell','Polymorph Spell','Shadow Self Spell','Shadow Creature Spell','All Enemies Spell','Steal Spell','Ward Spell','Global Spell','Manipulation Spell','Mutate Spell']
BUFFS_ALL = ['Strong','Giant','Monstrous','Gargantuan','Colossal','Epic','Keen Eyes','Accurate','Sniper','Unstoppable','Extraordinary','Primordial','Radical','Sharpened Blade','Potent Trap','Aegis','Indemnity','Daybreaker','Nightbringer']
BUFFS_DAMAGE = ['Strong','Giant','Monstrous','Gargantuan','Colossal','Epic']
BUFFS_ACCURACY = ['Keen Eyes','Accurate','Sniper','Unstoppable','Extraordinary']
BUFFS_HEALING = ['Primordial','Radical']
BUFFS_PERCENT = ['Sharpened Blade','Potent Trap']
BUFFS_PROTECT = ['Aegis','Indemnity']
BUFFS_DELAY = ['Daybreaker','Nightbringer']