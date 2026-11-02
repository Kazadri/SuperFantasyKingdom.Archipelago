from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import SFKWorld

BASE_PEDESTAL_ID = 1_006_000


@dataclass(frozen=True)
class Pedestal:
    name: str
    offset: int
    race: str = "Human"

    @property
    def ap_code(self) -> int:
        return BASE_PEDESTAL_ID + self.offset

_PEDESTAL_LIST = [
    Pedestal("Human Berry1", 0),
    Pedestal("Human Berry2", 1),
    Pedestal("Human Berry3", 2),
    Pedestal("Human Berry4", 3),
    Pedestal("Human Gold1", 4),
    Pedestal("Human Gold2", 5),
    Pedestal("Human Gold3", 6),
    Pedestal("Human Gold4", 7),
    Pedestal("Human Gold5", 8),
    Pedestal("Human Stone1", 9),
    Pedestal("Human Stone2", 10),
    Pedestal("Human Stone3", 11),
    Pedestal("Human Stone4", 12),
    Pedestal("Human Stone5", 13),
    Pedestal("Human Stone6", 14),
    Pedestal("Human Stone7", 15),
    Pedestal("Human Wheat1", 16),
    Pedestal("Human Wheat2", 17),
    Pedestal("Human Wheat3", 18),
    Pedestal("Human Wheat4", 19),
    Pedestal("Human Wheat5", 20),
    Pedestal("Human Wheat6", 21),
    Pedestal("Human Wood1", 22),
    Pedestal("Human Wood2", 23),
    Pedestal("Human Wood3", 24),
    Pedestal("Human Wood4", 25),
    Pedestal("Human Wood5", 26),
    Pedestal("Human Wood6", 27),
    Pedestal("Human Wood7", 28),
]

PEDESTALS: Dict[str, Pedestal] = {p.name: p for p in _PEDESTAL_LIST}

def get_active_pedestals(world: "SFKWorld") -> Dict[str, Pedestal]:
    """{name: Pedestal} for pedestals of enabled races only."""
    enabled = world.options.EnabledChapter.value
    return {name: p for name, p in PEDESTALS.items() if p.race in enabled}


def get_active_pedestals_names(world: "SFKWorld") -> List[str]:
    return sorted(get_active_pedestals(world))