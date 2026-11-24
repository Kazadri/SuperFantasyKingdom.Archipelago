from worlds.generic.Rules import add_rule, add_item_rule
from typing import TYPE_CHECKING

from .Relics import RELICS
from .Heroes import get_active_heroes, hero_race_name, victory_name
from .Buildings import BUILDINGS
from .Units import UNITS, unit_location_name

if TYPE_CHECKING:
    from . import SFKWorld

def building_rule(b, player):
    castle = b.castle_level_required()
    req = b.requirements()
    return lambda state: (
        state.has(b.name, player)
        and state.has_all(req, player)
        and (castle == 0 or state.has("Progressive Castle", player, castle))
    )

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
        add_rule(world.multiworld.get_location(b.name, player), building_rule(b, player))

    # Unit requirements
    for u in UNITS.values():
        loc = world.multiworld.get_location(unit_location_name(u.name), player)
        add_rule(loc, lambda state, n=u.name: state.has(n, player))
        add_item_rule(loc, lambda item, n=u.name: not (item.player == player and item.name == n))

    # Relic requirements
    active_races = options.EnabledChapter.value
    buildings_by_name = {b.name: b for b in BUILDINGS.values()}
    for r in RELICS.values():
        if r.race is not None and r.race not in active_races:
            continue  # location not created for this seed
        loc = world.multiworld.get_location(r.location_name, player)
        for bname in r.buildings:
            add_rule(loc, building_rule(buildings_by_name[bname], player))
        if r.units:
            add_rule(loc, lambda state, req=r.units: state.has_all(req, player))