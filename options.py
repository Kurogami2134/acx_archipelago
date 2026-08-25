from dataclasses import dataclass
from enum import IntEnum

from Options import Choice, PerGameCommonOptions, Toggle, DefaultOnToggle, Range

class DeathLink(DefaultOnToggle):
    """DeathLink:
    """
    auto_display_name = True
    display_name = "DeathLink"

class RandomAces(DefaultOnToggle):
    """Randomize ACES:
    """
    auto_display_name = True
    display_name = "Randomize Aces"

class GameObjective(Choice):
    """Win Condition:
    - Missionsanity: clear a number of missions
    - story1: Clear 15A
    - story2: Clear 15B
    - Story Either: Clear either 15A or 15B
    """
    auto_display_name = True
    display_name = "Win Condition"
    option_missionsanity = 0
    option_story1 = 1
    option_story2 = 2
    option_story_either = 3
    default = 0

class RequiredMissions(Range):
    """"""
    display_name = "Required Missions (Missionsanity)"
    range_start = 1
    range_end = 30
    default = 16

class StartingCredits(Range):
    """"""
    display_name = "Starting Credits"
    range_start = 0
    range_end = 30000
    default = 2500

class MinimumClearRank(Choice):
    """Sets the minimum rank you need to check a mission location"""
    display_name = "Min. Mission Rank"
    option_C = 3
    option_B = 2
    option_A = 1
    option_S = 0
    default = 3


@dataclass
class ACXOptions(PerGameCommonOptions):
    # death link
    death_link: DeathLink
    
    # randomization options
    randomize_aces: RandomAces
    required_missions: RequiredMissions

    # starting credits
    starting_credits: StartingCredits
    
    # progression
    min_rank: MinimumClearRank
    objective_to_win: GameObjective

