from dataclasses import dataclass
from enum import IntEnum

from Options import Choice, PerGameCommonOptions, Toggle, DefaultOnToggle, Range

class DeathLink(DefaultOnToggle):
    """DeathLink:
    """
    auto_display_name = True
    display_name = "DeathLink"

class GameObjective(Choice):
    """Win Condition:
    - Hunt Alatreon
    - Hunt Amatsu
    - Hunt Jhen Mohran
    - Clear Alatreon Quest
    - Clear Amatsu Urgent
    - Clear Jhen Mohran Urgent
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



@dataclass
class ACXOptions(PerGameCommonOptions):
    # death link
    death_link: DeathLink
    
    # randomization options
    required_missions: RequiredMissions

    # starting credits
    starting_credits: StartingCredits
    
    # goal
    objective_to_win: GameObjective

