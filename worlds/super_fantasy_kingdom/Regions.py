from BaseClasses import Region, ItemClassification
from typing import TYPE_CHECKING
from collections.abc import Iterator
from .Types import SFKLocation, SFKItem
from .Locations import location_table, is_valid_location
from .Types import ChapterType
from .Heroes import (get_active_heroes, hero_day_name, hero_day_code, hero_race_name,
                     victory_name, DAY_COUNT)

if TYPE_CHECKING:
    from . import SFKWorld

def create_regions(world: "SFKWorld"):
    menu = create_region(world, "Menu")
    for race, heroes in get_active_heroes(world).items():
        race_region = create_region_and_connect(world, race, f"Menu -> {race}", menu)
        for hero in heroes:
            name = hero_race_name(race, hero)
            region = create_region_and_connect(world, name, f"{race} -> {name}", race_region)

            for day in range(1, DAY_COUNT + 1):
                loc_name = hero_day_name(race, hero, day)
                region.locations.append(
                    SFKLocation(world.player, loc_name, hero_day_code(race, hero, day), region)
                )

            v_name = victory_name(race, hero)
            event_loc = SFKLocation(world.player, v_name, None, region)
            event_loc.place_locked_item(SFKItem(v_name, ItemClassification.progression, None, world.player))
            region.locations.append(event_loc)

def create_region(world: "SFKWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = SFKLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)

    world.multiworld.regions.append(reg)
    return reg


def create_region_and_connect(world: "SFKWorld",name: str, entrancename: str, connected_region: Region, rule=None) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename, rule)
    return reg

def get_enabled_chapters(world: "SFKWorld") -> Iterator[ChapterType]:
    for name in world.options.EnabledChapter.value:
        yield ChapterType[name]