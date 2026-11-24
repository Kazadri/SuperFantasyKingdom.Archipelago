from dataclasses import dataclass, replace
from typing import Dict, Optional, Tuple

from .Units import UNITS
from .Buildings import BUILDINGS
from .Heroes import RACES

BASE_RELIC_ID = 1_011_000  # check it doesn't collide with your other ID ranges

_BUILDING_NAMES = {b.name for b in BUILDINGS.values()}


@dataclass(frozen=True)
class Relic:
    key: str
    offset: int
    title: str
    units: Tuple[str, ...] = ()
    buildings: Tuple[str, ...] = ()
    race: Optional[str] = None
    kingdom_level: int = 0
    amaya: bool = False
    location_name: str = ""

    def __post_init__(self):
        for u in self.units:
            if u not in UNITS:
                raise ValueError(f"Relic {self.key}: unknown unit {u}")
        for b in self.buildings:
            if b not in _BUILDING_NAMES:
                raise ValueError(f"Relic {self.key}: unknown building {b}")
        if self.race is not None and self.race not in RACES:
            raise ValueError(f"Relic {self.key}: unknown race {self.race}")

    @property
    def ap_code(self) -> int:
        return BASE_RELIC_ID + self.offset

_RELIC_LIST = [
    Relic("Acid", 0, "Acid", units=("Ghost",)),
    Relic("AmuletOfTheDead", 1, "Amulet of the Dead", race="Undead"),
    Relic("BlindLove", 2, "Blind Love", units=("Succubus",)),
    Relic("BloodPoisoning", 3, "Blood Poisoning", units=("Leech Mother",)),
    Relic("BloodyKnife", 4, "Bloody Knife", units=("Archer",)),
    Relic("BurningBook", 5, "Burning Book", units=("Jester",)),
    Relic("Charge", 6, "Charge!", units=("Headless",)),
    Relic("Conductor", 7, "Conductor", units=("Runescribe",)),
    Relic("CoverFire", 8, "Cover Fire", units=("Gremlin",)),
    Relic("CrimsonHeart", 9, "Crimson Heart", units=("Devil",)),
    Relic("Destiny", 10, "Destiny", units=("Angel",)),
    Relic("Dice", 11, "Dice", units=("Djinn",)),
    Relic("Disease", 12, "Disease", units=("Abomination",)),
    Relic("Duck", 13, "Duck", units=("Griffin",)),
    Relic("EagleEye", 14, "Eagle Eye", units=("Cyclops",)),
    Relic("Eclipse", 15, "Eclipse", units=("Clown",)),
    Relic("Enlightenment", 16, "Enlightenment", units=("Druid",)),
    Relic("Fangs", 17, "Fangs", units=("Vampire",)),
    Relic("Feasting", 18, "Feasting", units=("Ghoul",)),
    Relic("FireInABottle", 19, "Fire in a Bottle"),
    Relic("FireShield", 20, "Fire Shield"),
    Relic("FlameShock", 21, "Flame Shock", units=("Miner",)),
    Relic("FrostArrows", 22, "Frost Arrows", units=("Halfling",)),
    Relic("GasCloud", 23, "Gas Cloud", units=("Shroom",)),
    Relic("Greatshield", 24, "Greatshield", units=("Swordsman",)),
    Relic("Hellfire", 25, "Hellfire", units=("Jailer",)),
    Relic("HiddenBlade", 26, "Hidden Blade", units=("Rogue",)),
    Relic("HolyWater", 27, "Holy Water", units=("Monk",)),
    Relic("HoneyDipper", 28, "Honey Dipper", units=("Bee",)),
    Relic("Hourglass", 29, "Hourglass", units=("Lich",)),
    Relic("HungryShield", 30, "Hungry Shield", race="Human"),
    Relic("Hurry", 31, "Hurry", units=("Observer",)),
    Relic("HydroPower", 32, "Hydro Power", units=("Magus",)),
    Relic("IceBreaker", 33, "Ice Breaker", units=("Frost Mage",)),
    Relic("KnockKnock", 34, "Knock Knock", units=("Satyr",)),
    Relic("LightningRod", 35, "Lightning Rod", units=("Stormcaller",)),
    Relic("Lute", 36, "Lute", units=("Bard",)),
    Relic("Madness", 37, "Madness", units=("Banshee",)),
    Relic("MagicBeans", 38, "Magic Beans", units=("Dryad",)),
    Relic("MetalArrow", 39, "Metal Arrows", units=("Crossbowman",)),
    Relic("MetalMage", 40, "Metal Mage", race="Human"),
    Relic("MugOfJoy", 41, "Mug of Joy", units=("Marksman",)),
    Relic("Necronomicon", 42, "Necronomicon", units=("Deathpriest",)),
    Relic("Polishing", 43, "Polishing", units=("Flamewalker",)),
    Relic("RagefireGauntlet", 44, "Ragefire Gauntlet", units=("Berserk",)),
    Relic("ScrollOfDarkness", 45, "Scroll of Darkness", buildings=("Elemental Tower",)),
    Relic("ScrollOfEarth", 46, "Scroll of Earth", buildings=("Elemental Tower",)),
    Relic("ScrollOfFire", 47, "Scroll of Fire", buildings=("Elemental Tower",)),
    Relic("ScrollOfIce", 48, "Scroll of Ice", buildings=("Elemental Tower",)),
    Relic("ScrollOfThunder", 49, "Scroll of Thunder", buildings=("Elemental Tower",)),
    Relic("ScrollOfWater", 50, "Scroll of Water", buildings=("Elemental Tower",)),
    Relic("ScrollOfWind", 51, "Scroll of Wind", buildings=("Elemental Tower",)),
    Relic("SkyShield", 52, "Sky Shield", units=("Paladin",)),
    Relic("SleepPowder", 53, "Sleep Powder", units=("Shaman",)),
    Relic("SlipperySlope", 54, "Slippery Slope", units=("Colossus",)),
    Relic("SnowGlobe", 55, "Snow Globe", units=("Yeti",)),
    Relic("StaffOfLife", 56, "Staff of Life", units=("Pixie",)),
    Relic("SwiftSpear", 57, "Swift Spear", units=("Spearman",)),
    Relic("ThickSkin", 58, "Thick Skin", units=("Troll",)),
    Relic("ThornyWhip", 59, "Thorny Whip", units=("Treant",)),
    Relic("UnholyAura", 60, "Unholy Aura"),
    Relic("UniqueHorn", 61, "Unique Horn", units=("Jouster",)),
    Relic("VipersKiss", 62, "Viper's Kiss", units=("Dinosaur",)),
    Relic("Vision", 63, "Glasses"),
    Relic("Vision2", 64, "Glasses"),
    Relic("Vision3", 65, "Glasses"),
    Relic("Vision4", 66, "Glasses"),
    Relic("WeakSpot", 67, "Weak Spot", units=("Dancer",)),
    Relic("WildFire", 68, "Wildfire", units=("Efreet",)),
    Relic("Wolfsbane", 69, "Wolfsbane", units=("Werewolf",)),
    Relic("Wrench", 70, "Wrench", units=("Mechanic",)),
    Relic("Archaeologist", 71, "Archaeology", race="Undead", kingdom_level=18, amaya=True),
    Relic("Bait", 72, "Bait", race="Human", kingdom_level=10, amaya=True),
    Relic("Bait2", 73, "Bait", race="Human", kingdom_level=10, amaya=True),
    Relic("BanishedKing", 74, "Banished King", kingdom_level=2, amaya=True),
    Relic("BetterBerries", 75, "Better Berries", race="Human", kingdom_level=18, amaya=True),
    Relic("BigDaddy", 76, "Big Daddy", race="Undead", kingdom_level=14, amaya=True),
    Relic("BoneGrowth", 77, "Bone Growth", race="Undead", kingdom_level=12, amaya=True),
    Relic("BushFinder", 78, "Bush of Life", race="Human", kingdom_level=6, amaya=True),
    Relic("CarrotOnAStick", 79, "Carrot on a Stick", race="Human", kingdom_level=24, amaya=True),
    Relic("Cookies", 80, "Cookies", kingdom_level=4, amaya=True),
    Relic("Cookies2", 81, "Cookies with Milk", kingdom_level=4),
    Relic("Deforestation", 82, "Deforestation", race="Human", kingdom_level=16, amaya=True),
    Relic("Dessert", 83, "Dessert", race="Human", kingdom_level=14, amaya=True),
    Relic("FieldsOfGlory", 84, "Fields of Glory", buildings=("Farm",), race="Human", kingdom_level=44, amaya=True),
    Relic("FishFilet", 85, "Fish Fillet", race="Human", kingdom_level=30, amaya=True),
    Relic("FishingNet", 86, "Fishing Net", race="Human", kingdom_level=20, amaya=True),
    Relic("FishingRod", 87, "Fishing Rod", race="Human", kingdom_level=36, amaya=True),
    Relic("Fruitarian", 88, "Forbidden Fruit", race="Human", kingdom_level=12, amaya=True),
    Relic("GoldDigger", 89, "Gold Digger", buildings=("Goldmine",), race="Human", kingdom_level=42, amaya=True),
    Relic("GreenHouse", 90, "Greenhouse", buildings=("Farm",), race="Human", kingdom_level=34, amaya=True),
    Relic("Inheritance", 91, "Inheritance", race="Undead", kingdom_level=8, amaya=True),
    Relic("Motivation", 92, "Motivation", buildings=("Graveyard",), race="Undead", kingdom_level=28, amaya=True),
    Relic("Mutilation", 93, "Mutilation", race="Undead", kingdom_level=36, amaya=True),
    Relic("Petrification", 94, "Petrification", race="Undead", kingdom_level=32, amaya=True),
    Relic("Plague", 95, "Plague", buildings=("Farm",), race="Undead", kingdom_level=30, amaya=True),
    Relic("Pumpking", 96, "Pumpking", race="Undead", kingdom_level=22, amaya=True),
    Relic("Purge", 97, "Purge", race="Undead", kingdom_level=6, amaya=True),
    Relic("Recycling", 98, "Recycling", race="Undead", kingdom_level=20, amaya=True),
    Relic("RisingTides", 99, "Rising Tides", race="Human", kingdom_level=22, amaya=True),
    Relic("SacrificialTablet", 100, "Sacrificial Tablet", buildings=("Elemental Tower",), kingdom_level=40, amaya=True),
    Relic("Salvage", 101, "Salvage", race="Undead", kingdom_level=16, amaya=True),
    Relic("Scissors", 102, "Scissors", race="Human", kingdom_level=8, amaya=True),
    Relic("Soup", 103, "Soup", buildings=("Brewery",), race="Human", kingdom_level=28, amaya=True),
    Relic("SpawnBloats", 104, "Bloat", race="Undead", amaya=True),
    Relic("SpawnBones", 105, "Bone", race="Undead", amaya=True),
    Relic("SpawnBushes", 106, "Bush", race="Human", amaya=True),
    Relic("SpawnGraves", 107, "Grave", race="Undead", amaya=True),
    Relic("SpawnOozePit", 108, "Ooze pool", race="Undead", kingdom_level=26, amaya=True),
    Relic("SpawnOres", 109, "Ore", race="Human", amaya=True),
    Relic("SpawnPumpkins", 110, "Pumpkin", race="Undead", amaya=True),
    Relic("SpawnRocks", 111, "Rock", amaya=True),
    Relic("SpawnTrees", 112, "Tree", race="Human", amaya=True),
    Relic("SugarTax", 113, "Sugar Tax", race="Undead", kingdom_level=24, amaya=True),
    Relic("SweetTooth", 114, "Sweet Tooth", buildings=("Bakery",), race="Undead", kingdom_level=34, amaya=True),
    Relic("VelvetGloves", 115, "Velvet Gloves", kingdom_level=38, amaya=True),
    Relic("WateringCan", 116, "Watering Can", race="Human", kingdom_level=32, amaya=True),
    Relic("Wilderness", 117, "Wilderness", buildings=("Farm",), race="Human", kingdom_level=26, amaya=True),
    Relic("Zombie", 118, "Zombie", race="Undead", kingdom_level=10, amaya=True),
]


def _build() -> Dict[str, Relic]:
    counts: Dict[str, int] = {}
    for r in _RELIC_LIST:
        counts[r.title] = counts.get(r.title, 0) + 1

    out: Dict[str, Relic] = {}
    for r in _RELIC_LIST:
        name = f"Relic: {r.title}" if counts[r.title] == 1 else f"Relic: {r.title} ({r.key})"
        assert r.key not in out and r.offset == len(out), f"bad offset/duplicate for {r.key}"
        out[r.key] = replace(r, location_name=name)
    return out


RELICS: Dict[str, Relic] = _build()