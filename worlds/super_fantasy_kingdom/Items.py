import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification

from .Types import ItemData, ChapterType, SFKItem, chapter_type_to_name
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import SFKWorld

BASE_BUILDING_ID = 1_000_000

def create_itempool(world: "SFKWorld") -> List[Item]:
    itempool: List[Item] = []

    # In this function is where you would remove any starting items that you add in options such as starting chapter
    # This is also the place you would add dynamic amounts of items from options
    # I can point to Sly Cooper and the Thievious Raccoonus since I did that

    # This is a good place to grab anything you need from options
    starting_chapter = chapter_type_to_name[ChapterType(world.options.StartingChapter)]

    # For this example I'll make it so there is a starting chapter
    # We loop through all the chapters in the my_chapter section
    for chapter in sfk_chapters.keys():
        # If the starting chapter equals the chapter we're looking at skip it
        # We skip it since we dont want to add the chapter the player started with to the item pool
        print("-------------------------")
        print(chapter)
        print("-------------------------")
        if starting_chapter == chapter:
            continue
        # Otherwise then we create an item with that name and add it to the item pool
        else:
            itempool.append(create_item(world, chapter))

    for name in item_table:
        if name == "HumanVictory" or name == "UndeadVictory" or name in sfk_precollected_items:
            continue
        itempool.append(create_item(world, name))

    # It's up to you and how you want things organized but I like to deal with victory here
    # This creates your win item and then places it at the "location" where you win
    humanVictory = create_item(world, "HumanVictory")
    undeadVictory = create_item(world, "UndeadVictory")
    world.multiworld.get_location("HumanVictory", world.player).place_locked_item(humanVictory)
    world.multiworld.get_location("UndeadVictory", world.player).place_locked_item(undeadVictory)

    # Then junk items are made
    # Check out the create_junk_items function for more details
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 1)

    return itempool


# This is a generic function to create a singular item
def create_item(world: "SFKWorld", name: str) -> Item:
    data = item_table[name]
    return SFKItem(name, data.classification, data.ap_code, world.player)


# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "SFKWorld", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [SFKItem(name, item_type, data.ap_code, world.player)]

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

sfk_geneal_items = {
    "HumanVictory": ItemData(22050007, ItemClassification.progression),
    "UndeadVictory": ItemData(22050008, ItemClassification.progression),
}

sfk_precollected_items = {
    "Tavern":ItemData(BASE_BUILDING_ID+6, ItemClassification.progression),
}
# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well
sfk_building_items = {
    "Wood":ItemData(BASE_BUILDING_ID+1, ItemClassification.progression),
    "Sawmill":ItemData(BASE_BUILDING_ID+2, ItemClassification.progression),
    "Well":ItemData(BASE_BUILDING_ID+3, ItemClassification.progression),
    "Quarry":ItemData(BASE_BUILDING_ID+4, ItemClassification.progression),
    "Farm":ItemData(BASE_BUILDING_ID+5, ItemClassification.progression),
    "Mine":ItemData(BASE_BUILDING_ID+7, ItemClassification.progression),
    "Smelter":ItemData(BASE_BUILDING_ID+8, ItemClassification.progression),
    "Port":ItemData(BASE_BUILDING_ID+9, ItemClassification.progression),
    "Hunter":ItemData(BASE_BUILDING_ID+10, ItemClassification.progression),
    "Windmill":ItemData(BASE_BUILDING_ID+11, ItemClassification.progression),
    "Brewery":ItemData(BASE_BUILDING_ID+12, ItemClassification.progression),
    "Siege":ItemData(BASE_BUILDING_ID+13, ItemClassification.progression),
    "House":ItemData(BASE_BUILDING_ID+14, ItemClassification.progression),
    "Stables":ItemData(BASE_BUILDING_ID+15, ItemClassification.progression),
    "Graveyard":ItemData(BASE_BUILDING_ID+16, ItemClassification.progression),
    "Portal":ItemData(BASE_BUILDING_ID+17, ItemClassification.progression),
    "Bakery":ItemData(BASE_BUILDING_ID+18, ItemClassification.progression),
    "Elemental":ItemData(BASE_BUILDING_ID+19, ItemClassification.progression),
    "Geologist hunt": ItemData(BASE_BUILDING_ID+27, ItemClassification.progression),
    "Decoration": ItemData(BASE_BUILDING_ID+30, ItemClassification.progression),
    "Coins": ItemData(BASE_BUILDING_ID+32, ItemClassification.progression),
    "Forager": ItemData(BASE_BUILDING_ID+35, ItemClassification.progression),
    "Firsherhut": ItemData(BASE_BUILDING_ID+36, ItemClassification.progression),
    "Monument": ItemData(BASE_BUILDING_ID+100, ItemClassification.progression),

    # Useful items
    # "A good friend": ItemData(20050004, ItemClassification.useful),
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
    **sfk_geneal_items,
    **sfk_precollected_items,
    **sfk_building_items,
    **sfk_chapters,
    **junk_items
}