import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification
from .Buildings import BUILDINGS, BASE_BUILDING_ID, BASE_ROAD_ID

from .Types import ItemData, ChapterType, SFKItem, chapter_type_to_name
from .Heroes import HEROES, get_active_hero_names
from .Regions import get_enabled_chapters
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import SFKWorld

OVERLAND_ROAD_COUNT = 70
CITY_ROAD_COUNT = 21

def create_itempool(world: "SFKWorld") -> List[Item]:
    itempool: List[Item] = []
    starting_chapter = ChapterType(world.options.StartingChapter)

    for chapter in get_enabled_chapters(world):
        if starting_chapter != chapter:
            itempool.append(create_item(world, chapter_type_to_name[chapter]))

    for hero in get_active_hero_names(world):
        if hero != world.starting_hero:
            itempool.append(create_item(world, hero))

    for name in item_table:
        if (name in sfk_precollected_items
                or name in sfk_chapters
                or name in junk_items
                or name in sfk_road_items
                or name in sfk_hero_items):
            continue
        itempool.append(create_item(world, name))

    itempool += create_road_items(world)

    free = len(world.multiworld.get_unfilled_locations(world.player))
    itempool += create_junk_items(world, free - len(itempool))

    return itempool

def create_road_items(world: "SFKWorld") -> List[Item]:
    road_item: List[Item] = []
    road_item += create_multiple_items(world, "Progressive Overland Road", OVERLAND_ROAD_COUNT)
    road_item += create_multiple_items(world, 'Progressive City Road', CITY_ROAD_COUNT)

    return road_item

# This is a generic function to create a singular item
def create_item(world: "SFKWorld", name: str) -> Item:
    data = item_table[name]
    return SFKItem(name, data.classification, data.ap_code, world.player)


# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "SFKWorld", name: str, count: int) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [SFKItem(name, data.classification, data.ap_code, world.player)]

    return itemlist


# Finally, where junk items are created
def create_junk_items(world: "SFKWorld", count: int) -> List[Item]:
    # trap_chance = world.options.TrapChance.value
    trap_chance = 0
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    # This grabs all the junk items and trap items
    for name in item_table.keys():
        # Here we are getting all the junk item names and weights
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        # This is for traps if your randomization includes it
        # It also grabs the trap weights from the options page
        # elif trap_chance > 0 and ic == ItemClassification.trap:
        #     if name == "Forcefem Trap":
        #         trap_list[name] = world.options.ForcefemTrapWeight.value
        #     elif name == "Speed Change Trap":
        #         trap_list[name] = world.options.SpeedChangeTrapWeight.value

    # Where all the magic happens of adding the junk and traps randomly
    # AP does all the weight management so we just need to worry about how many are created
    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

sfk_precollected_items = {
    b.name: ItemData(b.ap_code, b.classification)
    for b in BUILDINGS.values() if b.precollected
}

sfk_building_items = {
    b.name: ItemData(b.ap_code, b.classification)
    for b in BUILDINGS.values() if not b.precollected
}

sfk_outpost_items = {
    "WorldWood": ItemData(BASE_BUILDING_ID + 301, ItemClassification.progression),
    "WorldStone": ItemData(BASE_BUILDING_ID + 302, ItemClassification.progression),
    "WorldWheat": ItemData(BASE_BUILDING_ID + 303, ItemClassification.progression),
    "WorldOre": ItemData(BASE_BUILDING_ID + 304, ItemClassification.progression),
    "WorldHunter": ItemData(BASE_BUILDING_ID + 306, ItemClassification.progression),
    "WorldBanish": ItemData(BASE_BUILDING_ID + 307, ItemClassification.progression),
    "WorldDifficulty": ItemData(BASE_BUILDING_ID + 309, ItemClassification.progression),
    "WorldFaith": ItemData(BASE_BUILDING_ID + 310, ItemClassification.progression),
    "WorldAppeal": ItemData(BASE_BUILDING_ID + 311, ItemClassification.progression),
    "WorldRelic": ItemData(BASE_BUILDING_ID + 312, ItemClassification.progression),
    "WorldUnit": ItemData(BASE_BUILDING_ID + 313, ItemClassification.progression),
    "WorldCoins": ItemData(BASE_BUILDING_ID + 319, ItemClassification.progression),
    "WorldBarracks": ItemData(BASE_BUILDING_ID + 360, ItemClassification.progression),
    "WorldArchery": ItemData(BASE_BUILDING_ID + 361, ItemClassification.progression),
    "WorldMages": ItemData(BASE_BUILDING_ID + 362, ItemClassification.progression),
    "WorldSummoners": ItemData(BASE_BUILDING_ID + 363, ItemClassification.progression),
    "WorldShards": ItemData(BASE_BUILDING_ID + 507, ItemClassification.progression),
}

sfk_upgrade_items = {
    f"{b.name} upgrade": ItemData(b.upgrade_code, ItemClassification.useful)
    for b in BUILDINGS.values() if b.has_upgrade
}

sfk_road_items = {
    "Progressive Overland Road": ItemData(BASE_ROAD_ID+1, ItemClassification.useful),
    "Progressive City Road": ItemData(BASE_ROAD_ID+2, ItemClassification.useful),
}

sfk_hero_items = {
    h.name: ItemData(h.ap_code, ItemClassification.progression)
    for h in HEROES.values()
}

# I like to split up the items so that its easier to look at and since sometimes you only need to look at one specific type of list
# An example of that is in create_itempool where I simulated having a starting chapter
sfk_chapters = {
    "Human": ItemData(20050008, ItemClassification.progression),
    "Undead": ItemData(20050009, ItemClassification.progression),
}

junk_items = {
    # Junk
    "An Old Gamecube": ItemData(20050011, ItemClassification.filler, 0),
    "Coughing Baby": ItemData(20050012, ItemClassification.filler, 0),

    # Traps
    # "Forcefem Trap": ItemData(20050013, ItemClassification.trap, 0),
    # "Speed Change Trap": ItemData(20050014, ItemClassification.trap, 0)
}

# Junk weights is just how often an item will be chosen when junk is being made
# Bigger item = more likely to show up
junk_weights = {
    "An Old Gamecube": 40,
    "Coughing Baby": 20
}

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **sfk_precollected_items,
    **sfk_building_items,
    **sfk_outpost_items,
    **sfk_upgrade_items,
    **sfk_road_items,
    **sfk_hero_items,
    **sfk_chapters,
    **junk_items
}