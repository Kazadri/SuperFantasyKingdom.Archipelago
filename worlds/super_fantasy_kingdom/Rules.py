from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING

from .Heroes import get_active_heroes, hero_race_name, victory_name
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

    victory_items = []
    for race, heroes in get_active_heroes(world).items():
        add_rule(world.multiworld.get_entrance(f"Menu -> {race}", player),
                 lambda state, r=race: state.has(r, player))
        for hero in heroes:
            name = hero_race_name(race, hero)
            add_rule(world.multiworld.get_entrance(f"{race} -> {name}", player),
                     lambda state, h=hero: state.has(h, player))
            victory_items.append(victory_name(race, hero))

    world.multiworld.completion_condition[player] = lambda state: state.has_all(victory_items, player)

    # Building requirements
    for b in BUILDINGS.values():
        castle = b.castle_level_required()
        add_rule(world.multiworld.get_location(b.name, player),
                 lambda state, req=b.requirements(), c=castle:
                     state.has_all(req, player)
                     and (c == 0 or state.has("Progressive Castle", player, c)))
