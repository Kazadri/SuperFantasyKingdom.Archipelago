from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

GAME_NAME = "Super Fantasy Kingdom"

class SFKLocation(Location):
    game = GAME_NAME

class SFKItem(Item):
    game = GAME_NAME

# I use these next 2 to convert the number you get from the options into a name
# Mainly used in Items.py for starting chapter
# Not important for a lot of games
class ChapterType(IntEnum):
    Human = 1
    Undead = 2

chapter_type_to_name = {
    ChapterType.Human: "Human",
    ChapterType.Undead: "Undead",
}

# Here is where all the stuff from the Items.py comes from
# You can add or take away anything you want but ap_code and classification are pretty important
class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1

# Again where all the Location.py things come from
# You can add whatever you want here as well but ap_code and region are pretty important
class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]