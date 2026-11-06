from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple

from BaseClasses import ItemClassification

BASE_BUILDING_ID = 1_000_000
BASE_UPGRADE_ID = 1_002_000

STARTING_STORAGE = 4
MAX_CASTLE_LEVEL = 3

@dataclass(frozen=True)
class Building:
    name: str
    offset: int
    needs: Tuple[str, ...] = ()
    classification: ItemClassification = ItemClassification.progression
    has_upgrade: bool = False
    precollected: bool = False
    region: str = "Human"
    max_cost: int = 0

    @property
    def ap_code(self) -> int:
        return BASE_BUILDING_ID + self.offset

    @property
    def upgrade_code(self) -> int:
        return BASE_UPGRADE_ID + self.offset

    def _dependencies(self) -> FrozenSet[str]:
        """Explicit needs, plus the buildings required by each castle upgrade this one depends on."""
        deps = set(self.needs)
        for tier in range(1, storage_level(self.max_cost) + 1):
            deps.update(CASTLE_TIER_NEEDS[tier])
        return frozenset(deps)

    def requirements(self, _stack: Tuple[str, ...] = ()) -> FrozenSet[str]:
        if self.name in _stack:
            raise ValueError("Circular building dependency: " + " -> ".join(_stack + (self.name,)))

        result = {self.name}
        for dep in self._dependencies():
            result |= BUILDINGS[dep].requirements(_stack + (self.name,))

        return frozenset(result)

    def castle_level_required(self) -> int:
        level = storage_level(self.max_cost)
        for dep in self._dependencies():
            level = max(level, BUILDINGS[dep].castle_level_required())
        return level


_BUILDING_LIST = [
    Building("Lumberyard", 1, has_upgrade=True),
    Building("Sawmill", 2, needs=("Lumberyard",), max_cost=5),
    Building("Well", 3, needs=("Quarry",), has_upgrade=True, max_cost=4),
    Building("Quarry", 4, needs=("Lumberyard",), has_upgrade=True, max_cost=3),
    Building("Farm", 5, needs=("Lumberyard",), has_upgrade=True, max_cost=5),
    Building("Tavern", 6, has_upgrade=True, precollected=True),
    Building("Goldmine", 7, needs=("Sawmill",), has_upgrade=True, max_cost=5),
    Building("Smelter", 8, needs=("Quarry",), max_cost=9),
    Building("Port", 9, needs=("Sawmill",), has_upgrade=True, max_cost=3),
    Building("Hunter", 10, needs=("Quarry",), has_upgrade=True, max_cost=9),
    Building("Windmill", 11, needs=("Quarry",), max_cost=6),
    Building("Brewery", 12, needs=("Lumberyard", ), max_cost=9),
    Building("Siege camp", 13, needs=("Sawmill",), max_cost=5),
    Building("House", 14, needs=("Lumberyard",), has_upgrade=True, max_cost=4),
    Building("Stables", 15, needs=("Farm",), max_cost=5),
    Building("Graveyard", 16, needs=("Quarry",), max_cost=5),
    Building("Portal", 17, needs=("Goldmine",), max_cost=5),
    Building("Bakery", 18, needs=("Sawmill",), max_cost=6),
    Building("Elemental Tower", 19, needs=("Smelter",), max_cost=5),
    Building("Geologist Tent", 27, needs=("Goldmine",), has_upgrade=True, max_cost=4),
    Building("Decoration", 30, needs=("Farm",), has_upgrade=True, max_cost=4),
    Building("Coin Stamper", 32),
    Building("Forager", 35, needs=("Sawmill",), has_upgrade=True, max_cost=4),
    Building("Fisherhut", 36, needs=("Tavern",), has_upgrade=True), #No max cost since food are not gated by castle level
]

BUILDINGS: Dict[str, Building] = {b.name: b for b in _BUILDING_LIST}

CASTLE_TIER_NEEDS = {
    1: ("Lumberyard",),  # wood
    2: ("Quarry",),      # stone
    3: ("Smelter",),     # gold ingots
}

def storage_level(cost: int) -> int:
    """Castle upgrades needed for one resource's storage (4, 8, 16, 32) to hold `cost`."""
    level = 0
    while STARTING_STORAGE * 2 ** level < cost:
        level += 1
    return level

def _validate() -> None:
    assert len(BUILDINGS) == len(_BUILDING_LIST), "Duplicate building name"
    assert len({b.offset for b in _BUILDING_LIST}) == len(_BUILDING_LIST), "Duplicate building offset"
    for b in _BUILDING_LIST:
        assert storage_level(b.max_cost) <= MAX_CASTLE_LEVEL, f"{b.name}: cost {b.max_cost} exceeds the maximum storage"
        assert b.castle_level_required() <= MAX_CASTLE_LEVEL, f"{b.name} needs a castle level above {MAX_CASTLE_LEVEL}"
        for dep in b.needs:
            assert dep in BUILDINGS, f"{b.name} needs unknown building '{dep}'"
        b.requirements()  # raises on a cycle


_validate()