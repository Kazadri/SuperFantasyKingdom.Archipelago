from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import SFKWorld

BASE_BUILDING_ID = 1_000_000

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
    names = {name: data.ap_code for name, data in location_table.items()}

    return names


# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "SFKWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True


# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
sfk_building_locations = {
    "Wood": LocData(BASE_BUILDING_ID+1, "Human"),
    "Sawmill": LocData(BASE_BUILDING_ID+2, "Human"),
    "Well": LocData(BASE_BUILDING_ID+3, "Human"),
    "Quarry": LocData(BASE_BUILDING_ID+4, "Human"),
    "Farm": LocData(BASE_BUILDING_ID+5, "Human"),
    "Tavern": LocData(BASE_BUILDING_ID+6, "Human"),
    "Mine": LocData(BASE_BUILDING_ID+7, "Human"),
    "Smelter": LocData(BASE_BUILDING_ID+8, "Human"),
    "Port": LocData(BASE_BUILDING_ID+9, "Human"),
    "Hunter": LocData(BASE_BUILDING_ID+10, "Human"),
    "Windmill": LocData(BASE_BUILDING_ID+11, "Human"),
    "Brewery": LocData(BASE_BUILDING_ID+12, "Human"),
    "Siege": LocData(BASE_BUILDING_ID+13, "Human"),
    "House": LocData(BASE_BUILDING_ID+14, "Human"),
    "Stables": LocData(BASE_BUILDING_ID+15, "Human"),
    "Graveyard": LocData(BASE_BUILDING_ID+16, "Human"),
    "Portal": LocData(BASE_BUILDING_ID+17, "Human"),
    "Bakery": LocData(BASE_BUILDING_ID+18, "Human"),
    "Elemental": LocData(BASE_BUILDING_ID+19, "Human"),
}

extra_locations = {
}

event_locations = {
    "HumanVictory": LocData(None, "Human"),
    "UndeadVictory": LocData(None, "Undead")
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **sfk_building_locations,
    **extra_locations,
    **event_locations,
}