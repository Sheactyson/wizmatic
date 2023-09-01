import os

class LibCard:
    def __init__(self):
        self.cardName: str = "Unspecified"
        self.type: list = []
        self.desc: str = ""
        self.originalName: str = ""
        self.buffName: str = ""
        self.spellURL: str = "None"
        self.imgURL: str = "None"
        self.school: str = "None"
        self.regularPipCost: int = 0
        self.schoolPipCost: int = 0
        self.shadowPipCost: int = 0

        self.baseAccuracy: int = 0
        self.minDamage: int = 0
        self.maxDamage: int = 0
        self.baseHeal: int = 0
        self.baseTake: int = 0
        self.baseDOT: int = 0
        self.baseHOT: int = 0
        self.rounds: int = 0
        
        self.basePercent: int = 0
        self.baseSelfPercent: int = 0
        self.augmentSchools: list = []

        self.buffAccuracy: int = 0
        self.buffPierce: int = 0
        self.buffDamage: int = 0
        self.buffHeal: int = 0
        self.buffPercent: int = 0
        self.buffProtect: bool = False
        self.buffCloak: bool = False
        self.buffDelay: bool = False
        self.addPips: int = 0


INSTALLDIR = os.path.abspath('wizmatic').replace('\wizmatic\\','\\')
WIKIURL = 'https://wizard101central.com'

SCHOOLS = ['Fire','Ice','Storm','Balance','Myth','Death','Life','Star','Sun','Moon','Shadow']
SPELL_TYPE_ICONS = ['Damage Spell','Healing Spell','Charm Spell','Aura Spell','Enchantment Spell','Polymorph Spell','Shadow Self Spell','Shadow Creature Spell','All Enemies Spell','Steal Spell','Ward Spell','Global Spell','Manipulation Spell','Mutate Spell']
BUFFS_DAMAGE = ['Strong','Giant','Monstrous','Gargantuan','Colossal','Epic']
BUFFS_ACCURACY = ['Keen Eyes','Accurate','Sniper','Unstoppable','Extraordinary']
BUFFS_HEALING = ['Primordial','Radical']
BUFFS_PERCENT = ['Sharpened Blade','Potent Trap']
BUFFS_PROTECT = ['Aegis','Indemnity']
BUFFS_DELAY = ['Daybreaker','Nightbringer']