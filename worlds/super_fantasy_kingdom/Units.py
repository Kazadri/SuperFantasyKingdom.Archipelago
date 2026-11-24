from dataclasses import dataclass
from typing import Dict

BASE_UNIT_ID = 1_009_000
STARTING_UNIT_COUNT = 3

@dataclass(frozen=True)
class Unit:
    name: str
    offset: int
    race: str

    @property
    def ap_code(self) -> int:
        return BASE_UNIT_ID + self.offset

# APPEND ONLY: the offset is part of the Archipelago ID.
# Elementals and constructs (no upgrade tiers in the game) are ignored for now.
_UNIT_LIST = [
    Unit("Abomination", 0, "Undead"),
    Unit("Angel", 1, "Human"),
    Unit("Archer", 2, "Elven"),
    Unit("Banshee", 3, "Undead"),
    Unit("Bard", 4, "Human"),
    Unit("Bee", 5, "Swamp"),
    Unit("Berserk", 6, "Dwarven"),
    Unit("Clown", 7, "Undead"),
    Unit("Colossus", 8, "Desert"),
    Unit("Crossbowman", 9, "Human"),
    Unit("Cyclops", 10, "Barbarian"),
    Unit("Dancer", 11, "Elven"),
    Unit("Deathpriest", 12, "Undead"),
    Unit("Devil", 13, "Demon"),
    Unit("Dinosaur", 14, "Swamp"),
    Unit("Djinn", 15, "Desert"),
    Unit("Druid", 16, "Elven"),
    Unit("Dryad", 17, "Nature"),
    Unit("Flamewalker", 18, "Dwarven"),
    Unit("Frost Mage", 19, "Elven"),
    Unit("Ghost", 20, "Undead"),
    Unit("Ghoul", 21, "Undead"),
    Unit("Gremlin", 22, "Desert"),
    Unit("Griffin", 23, "Human"),
    Unit("Halfling", 24, "Elven"),
    Unit("Headless", 25, "Undead"),
    Unit("Jailer", 26, "Demon"),
    Unit("Jester", 27, "Demon"),
    Unit("Jouster", 28, "Human"),
    Unit("Leech Mother", 29, "Swamp"),
    Unit("Lich", 30, "Undead"),
    Unit("Magus", 31, "Desert"),
    Unit("Marksman", 32, "Dwarven"),
    Unit("Mechanic", 33, "Dwarven"),
    Unit("Miner", 34, "Dwarven"),
    Unit("Monk", 35, "Human"),
    Unit("Observer", 36, "Desert"),
    Unit("Paladin", 37, "Human"),
    Unit("Pixie", 38, "Nature"),
    Unit("Psion", 39, "Swamp"),
    Unit("Rogue", 40, "Elven"),
    Unit("Runescribe", 41, "Dwarven"),
    Unit("Satyr", 42, "Nature"),
    Unit("Shaman", 43, "Barbarian"),
    Unit("Shroom", 44, "Swamp"),
    Unit("Stormcaller", 45, "Barbarian"),
    Unit("Succubus", 46, "Demon"),
    Unit("Swordsman", 47, "Human"),
    Unit("Treant", 48, "Nature"),
    Unit("Troll", 49, "Barbarian"),
    Unit("Vampire", 50, "Undead"),
    Unit("Werewolf", 51, "Nature"),
    Unit("Yeti", 52, "Elven"),
    Unit("Efreet", 53, "Demon"),
    Unit("Minotaur", 54, "Barbarian"),
    Unit("Spearman", 55, "Human"),
]

UNITS: Dict[str, Unit] = {u.name: u for u in _UNIT_LIST}

def pick_starting_units(world) -> list[str]:
    if world.options.StartingUnitsMode.current_key == "randomized":
        return world.random.sample(sorted(UNITS), STARTING_UNIT_COUNT)

    return sorted(world.options.StartingUnits.value)

def unit_location_name(unit_name: str) -> str:
    return f"Play {unit_name}"