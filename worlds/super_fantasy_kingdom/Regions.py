from BaseClasses import Region
from .Types import SFKLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SFKWorld

def create_regions(world: "SFKWorld"):
    menu = create_region(world, "Menu")
    create_region_and_connect(world, "Human", "Menu -> Human", menu)
    create_region_and_connect(world, "Undead", "Menu -> Undead", menu)


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


def create_region_and_connect(world: "SFKWorld",name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg