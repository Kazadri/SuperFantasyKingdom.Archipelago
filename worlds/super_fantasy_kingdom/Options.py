from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, OptionSet
from .Heroes import HERO_NAMES

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

class StartingHero(Choice):
    """
    The hero you start with. Must be selected for your starting race.
    Random picks one of the heroes enabled for your starting race.
    """
    display_name = "Starting Hero"
    option_any_selected = 0
    option_alaric = 1
    option_cadus = 2
    option_cole = 3
    option_gideon = 4
    option_grumdil = 5
    option_mort = 6
    option_qhela = 7
    option_rickard = 8
    option_selene = 9
    option_sheva = 10
    option_thea = 11
    default = 0

STARTING_HERO_NAMES = {i + 1: n for i, n in enumerate(HERO_NAMES)}

class HumanHeroes(OptionSet):
    """Heroes to play with when playing the Human race. Ignored if Human is not an enabled race."""
    display_name = "Human Heroes"
    valid_keys = sorted(HERO_NAMES)
    default = sorted(HERO_NAMES)


class UndeadHeroes(OptionSet):
    """Heroes to play with when playing the Undead race. Ignored if Undead is not an enabled race."""
    display_name = "Undead Heroes"
    valid_keys = sorted(HERO_NAMES)
    default = sorted(HERO_NAMES)

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
    StartingHero:               StartingHero
    EnabledChapter:             EnabledChapter
    HumanHeroes:                HumanHeroes
    UndeadHeroes:               UndeadHeroes
    ExtraLocations:             ExtraLocations
    # TrapChance:                 TrapChance
    # ForcefemTrapWeight:         ForcefemTrapWeight
    # SpeedChangeTrapWeight:      SpeedChangeTrapWeight

# This is where you organize your options
# Its entirely up to you how you want to organize it
ap_skeleton_option_groups: Dict[str, List[Any]] = {
    "General Options": [ExtraLocations],
    "Race Options": [StartingChapter, EnabledChapter],
    "Hero Options": [StartingHero, HumanHeroes, UndeadHeroes],
    # "Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
    # "Trap Options": [TrapChance]
}