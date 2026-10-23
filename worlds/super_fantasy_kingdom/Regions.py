from BaseClasses import Region
from .Types import SFKLocation, ChapterType, chapter_type_to_name
from .Locations import location_table, is_valid_location, DAY_COUNT
from typing import TYPE_CHECKING
from collections.abc import Iterator

if TYPE_CHECKING:
    from . import SFKWorld


def create_regions(world: "SFKWorld"):
    menu = create_region(world, "Menu")
    for chapter in get_enabled_chapters(world):
        name = chapter_type_to_name[chapter]
        previous = create_region_and_connect(world, name, f"Menu -> {name}", menu)
        for day in range(1, DAY_COUNT + 1):
            day_name = f"{name} Day {day}"
            previous = create_region_and_connect(world, day_name, f"{previous.name} -> {day_name}", previous)


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