from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING

BASE_RESOURCE_ID = 2_000_000

if TYPE_CHECKING:
    from . import SFKWorld

@dataclass(frozen=True)
class Resource:
    name: str
    offset: int
    weight: int = 50
    race: str = "Human"

    @property
    def ap_code(self) -> int:
        return BASE_RESOURCE_ID + self.offset

_RESOURCE_LIST = [
    Resource("Faith", 0, 100),
    Resource("Coins", 1, 100),
    Resource("Wood", 2),
    Resource("Board", 3, 20),
    Resource("Stone", 4),
    Resource("Gold", 5),
    Resource("Ingot", 6, 20),
    Resource("Wheat", 7),
]

RESOURCES: Dict[str, Resource] = {r.name: r for r in _RESOURCE_LIST}

def get_active_resources(world: "SFKWorld") -> Dict[str, Resource]:
    """{name: Resource} for resources of enabled races only."""
    enabled = world.options.EnabledChapter.value
    return {name: p for name, p in RESOURCES.items() if p.race in enabled}


def get_active_resources_names(world: "SFKWorld") -> List[str]:
    return sorted(get_active_resources(world))