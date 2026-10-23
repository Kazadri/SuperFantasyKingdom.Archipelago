from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING

from .Regions import get_enabled_chapters
from .Types import chapter_type_to_name
from .Buildings import BUILDINGS

if TYPE_CHECKING:
    from . import SFKWorld


# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "SFKWorld"):
    player = world.player
    options = world.options

    # Chapter + victory rules
    victory_items = []
    for chapter in get_enabled_chapters(world):
        name = chapter_type_to_name[chapter]
        add_rule(world.multiworld.get_entrance(f"Menu -> {name}", player),
                 lambda state, n=name: state.has(n, player))
        victory_items.append(f"{name}Victory")

    world.multiworld.completion_condition[player] = lambda state: state.has_all(victory_items, player)

    # Building requirements
    for b in BUILDINGS.values():
        add_rule(world.multiworld.get_location(b.name, player),
                 lambda state, req=b.requirements(): state.has_all(req, player))
