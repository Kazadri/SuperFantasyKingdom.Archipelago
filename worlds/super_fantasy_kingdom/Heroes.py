from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import SFKWorld

BASE_HERO_ID = 1_004_000
BASE_HERO_DAY_ID = 1_005_000
DAY_COUNT = 28

RACES = ["Human", "Undead"]
RACE_OPTION_NAME = {"Human": "HumanHeroes", "Undead": "UndeadHeroes"}

@dataclass(frozen=True)
class Hero:
    name: str
    offset: int

    @property
    def ap_code(self) -> int:
        return BASE_HERO_ID + self.offset

_HERO_LIST = [
    Hero("Alaric", 0),
    Hero("Cadus", 1),
    Hero("Cole", 2),
    Hero("Gideon", 3),
    Hero("Grumdil", 4),
    Hero("Mort", 5),
    Hero("Qhe'la", 6),
    Hero("Rickard", 7),
    Hero("Selene", 8),
    Hero("Sheva", 9),
    Hero("Thea", 10),
]


HEROES: Dict[str, Hero] = {h.name: h for h in _HERO_LIST}
HERO_NAMES: List[str] = [h.name for h in _HERO_LIST]

def hero_day_name(race: str, hero: str, day: int) -> str:
    return f"{race} {hero} Day {day}"

def hero_race_name(race: str, hero: str) -> str:
    return f"{race} {hero}"

def victory_name(race: str, hero: str) -> str:
    return f"{race} {hero} Victory"

def hero_day_code(race: str, hero: str, day: int) -> int:
    return BASE_HERO_DAY_ID + RACES.index(race) * 308 + HEROES[hero].offset * 28 + day

def get_active_heroes(world: "SFKWorld") -> Dict[str, List[str]]:
    """{race: [heroes]} for enabled races only. Sorted so generation is deterministic."""
    active: Dict[str, List[str]] = {}
    for race in sorted(world.options.EnabledChapter.value):
        chosen = getattr(world.options, RACE_OPTION_NAME[race]).value
        active[race] = sorted(chosen)
    return active

def get_active_hero_names(world: "SFKWorld") -> List[str]:
    """Distinct heroes needed in the item pool (a hero shared by 2 races = 1 item)."""
    names = set()
    for heroes in get_active_heroes(world).values():
        names.update(heroes)
    return sorted(names)