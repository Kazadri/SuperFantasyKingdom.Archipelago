from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData
from .Buildings import BUILDINGS

if TYPE_CHECKING:
    from . import SFKWorld

BASE_DAY_ID = 1_001_000
DAY_COUNT = 28

def did_include_extra_locations(world: "SFKWorld") -> bool:
    return bool(world.options.ExtraLocations)


def get_total_locations(world: "SFKWorld") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        if not did_include_extra_locations(world) and name in extra_locations:
            continue

        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total


def get_location_names() -> Dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items() if data.ap_code is not None}

    return names


# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "SFKWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True

sfk_building_locations = {
    b.name: LocData(b.ap_code, b.region) for b in BUILDINGS.values()
}

sfk_day_complete_locations = {
    f"Human Day {d}": LocData(BASE_DAY_ID + d, f"Human Day {d}")
    for d in range(1, DAY_COUNT + 1)
}

extra_locations = {
}

event_locations = {
    "HumanVictory": LocData(None, f"Human Day {DAY_COUNT}"),
    "UndeadVictory": LocData(None, "Undead"),
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **sfk_building_locations,
    **sfk_day_complete_locations,
    **extra_locations,
    **event_locations,
}