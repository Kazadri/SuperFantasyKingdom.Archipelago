from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING
from .Locations import sfk_building_locations
from .Regions import get_enabled_chapters
from .Types import chapter_type_to_name

if TYPE_CHECKING:
    from . import SFKWorld


# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amoount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "SFKWorld"):
    player = world.player
    options = world.options
    #
    # # Chapter Access
    add_rule(world.multiworld.get_entrance("Menu -> Human", player),
             lambda state: state.has("Human", player))
    add_rule(world.multiworld.get_entrance("Menu -> Undead", player),
             lambda state: state.has("Undead", player))

    for loc_name in sfk_building_locations:
        add_rule(world.multiworld.get_location(loc_name, player),
                 lambda state, n=loc_name: state.has(n, player))

    # Victory condition rule!
    victory_items = [
        chapter_type_to_name[chapter] + "Victory"
        for chapter in get_enabled_chapters(world)
    ]
    world.multiworld.completion_condition[player] = lambda state: state.has_all(victory_items, player)