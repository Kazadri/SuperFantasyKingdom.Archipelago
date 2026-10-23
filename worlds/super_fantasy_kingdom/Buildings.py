from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple

from BaseClasses import ItemClassification

BASE_BUILDING_ID = 1_000_000
BASE_UPGRADE_ID = 1_002_000

@dataclass(frozen=True)
class Building:
    name: str
    offset: int
    needs: Tuple[str, ...] = ()
    classification: ItemClassification = ItemClassification.progression
    has_upgrade: bool = False
    precollected: bool = False
    region: str = "Human"

    @property
    def ap_code(self) -> int:
        return BASE_BUILDING_ID + self.offset

    @property
    def upgrade_code(self) -> int:
        return BASE_UPGRADE_ID + self.offset

    def requirements(self, _stack: Tuple[str, ...] = ()) -> FrozenSet[str]:
        if self.name in _stack:
            raise ValueError("Circular building dependency: " + " -> ".join(_stack + (self.name,)))

        result = {self.name}
        for dep in self.needs:
            result |= BUILDINGS[dep].requirements(_stack + (self.name,))

        return frozenset(result)


_BUILDING_LIST = [
    Building("Lumberyard", 1, has_upgrade=True),
    Building("Sawmill", 2, needs=("Lumberyard",)),
    Building("Well", 3, needs=("Quarry",), has_upgrade=True),
    Building("Quarry", 4, needs=("Lumberyard",), has_upgrade=True),
    Building("Farm", 5, needs=("Lumberyard",), has_upgrade=True),
    Building("Tavern", 6, has_upgrade=True, precollected=True),
    Building("Goldmine", 7, needs=("Sawmill",), has_upgrade=True),
    Building("Smelter", 8, needs=("Quarry",)),
    Building("Port", 9, needs=("Sawmill",), has_upgrade=True),
    Building("Hunter", 10, needs=("Quarry",), has_upgrade=True),
    Building("Windmill", 11, needs=("Quarry",)),
    Building("Brewery", 12, needs=("Lumberyard", )),
    Building("Siege camp", 13, needs=("Sawmill",)),
    Building("House", 14, needs=("Lumberyard",), has_upgrade=True),
    Building("Stables", 15, needs=("Farm",)),
    Building("Graveyard", 16, needs=("Quarry",)),
    Building("Portal", 17, needs=("Goldmine",)),
    Building("Bakery", 18, needs=("Sawmill",)),
    Building("Elemental Tower", 19, needs=("Smelter",)),
    Building("Geologist Tent", 27, needs=("Goldmine",), has_upgrade=True),
    Building("Decoration", 30, needs=("Farm",), has_upgrade=True),
    Building("Coin Stamper", 32),
    Building("Forager", 35, needs=("Sawmill",), has_upgrade=True),
    Building("Fisherhut", 36, needs=("Tavern",), has_upgrade=True),
]

BUILDINGS: Dict[str, Building] = {b.name: b for b in _BUILDING_LIST}

def _validate() -> None:
    assert len(BUILDINGS) == len(_BUILDING_LIST), "Duplicate building name"
    assert len({b.offset for b in _BUILDING_LIST}) == len(_BUILDING_LIST), "Duplicate building offset"
    for b in _BUILDING_LIST:
        for dep in b.needs:
            assert dep in BUILDINGS, f"{b.name} needs unknown building '{dep}'"
        b.requirements()  # raises on a cycle


_validate()