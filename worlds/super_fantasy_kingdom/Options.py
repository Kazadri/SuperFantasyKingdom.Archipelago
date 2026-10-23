from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range, OptionSet

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in ap_skeleton_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class StartingChapter(Choice):
    """
    Determines which race you'll start with.
    """
    display_name = "Starting Race"
    option_human = 1
    option_undead = 2
    default = 1

class ExtraLocations(Toggle):
    """
    This will enable the extra locations option. Toggle is just true or false.
    """
    display_name = "Add Extra Locations"

class EnabledChapter(OptionSet):
    """Enter the list of chapters to play.  Valid chapters are:
        'Human'
        'Undead'"""
    display_name = "Races"
    default = ["Human"]
    valid_keys_casefold = False

# class TrapChance(Range):
#     """
#     Determines the chance for any junk item to become a trap.
#     Set it to 0 for no traps.
#     Range is in fact a range. You can set the limits and its default.
#     """
#     display_name = "Trap Chance"
#     range_start = 0
#     range_end = 100
#     default = 0

# class ForcefemTrapWeight(Range):
#     """
#     The weight of forcefem traps in the trap pool.
#     Does really cool stuff to your body.
#     """
#     display_name = "Forcefem Trap Weight"
#     range_start = 0
#     range_end = 100
#     default = 100
#
# class SpeedChangeTrapWeight(Range):
#     """
#     The weight of speed change traps in the trap pool.
#     Speed change traps change the game speed for x seconds.
#     """
#     display_name = "Speed Change Trap Weight"
#     range_start = 0
#     range_end = 100
#     default = 25

@dataclass
class SFKOptions(PerGameCommonOptions):
    StartingChapter:            StartingChapter
    EnabledChapter:             EnabledChapter
    ExtraLocations:             ExtraLocations
    # TrapChance:                 TrapChance
    # ForcefemTrapWeight:         ForcefemTrapWeight
    # SpeedChangeTrapWeight:      SpeedChangeTrapWeight

# This is where you organize your options
# Its entirely up to you how you want to organize it
ap_skeleton_option_groups: Dict[str, List[Any]] = {
    "General Options": [ExtraLocations],
    "Race Options": [StartingChapter, EnabledChapter],
    # "Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
    # "Trap Options": [TrapChance]
}