from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData
from .Buildings import BUILDINGS
from .Heroes import RACES, HERO_NAMES, hero_day_name, hero_day_code, get_active_heroes, DAY_COUNT
if TYPE_CHECKING:
    from . import SFKWorld

def did_include_extra_locations(world: "SFKWorld") -> bool:
    return bool(world.options.ExtraLocations)


def get_total_locations(world: "SFKWorld") -> int:
    total = sum(1 for n in location_table if is_valid_location(world, n))
    total += sum(len(h) for h in get_active_heroes(world).values()) * DAY_COUNT
    return total


def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items() if data.ap_code is not None}
    names.update(all_hero_day_locations())
    return names


def is_valid_location(world: "SFKWorld", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True

def all_hero_day_locations() -> Dict[str, int]:
    """Every possible (race, hero, day) location, for location_name_to_id."""
    return {
        hero_day_name(race, hero, d): hero_day_code(race, hero, d)
        for race in RACES
        for hero in HERO_NAMES
        for d in range(1, DAY_COUNT + 1)
    }

sfk_building_locations = {
    b.name: LocData(b.ap_code, b.region) for b in BUILDINGS.values()
}

extra_locations = {
}

location_table = {
    **sfk_building_locations,
    **extra_locations,
}