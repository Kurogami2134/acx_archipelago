from rule_builder.rules import True_, Rule, Has


RULES = {
    "03A - Prelude": Has("03A - Prelude"),
    "03B - Captive City": Has("03B - Captive City"),
    "07A - Standoff in the Skies I": Has("07A - Standoff in the Skies I"),
    "07B - Standoff in the Skies II": Has("07B - Standoff in the Skies II"),
    "07C - Time Limit": Has("07C - Time Limit"),
    "12A - Gaiuss Tower": Has("12A - Gaiuss Tower"),
    "12B - Atmos Ring": Has("12B - Atmos Ring"),
    "12C - Wild Card": Has("12C - Wild Card"),
    "15A - End of Deception I": Has("15A - End of Deception I"),
    "15B - End of Deception II": Has("15B - End of Deception II"),
    "02 - Out of the Fire": Has("02 - Out of the Fire"),
    "04A - Last Line of Defense": Has("04A - Last Line of Defense"),
    "04B - False Target": Has("04B - False Target"),
    "05A - Rolling Thunder": Has("05A - Rolling Thunder"),
    "05B - Pinned Down": Has("05B - Pinned Down"),
    "06A - The Midnight Sun": Has("06A - The Midnight Sun"),
    "06B - Ice Bound": Has("06B - Ice Bound"),
    "08A - Striking Point": Has("08A - Striking Point"),
    "08B - The Wasteland": Has("08B - The Wasteland"),
    "09A - Blitz": Has("09A - Blitz"),
    "09B - A Diversion": Has("09B - A Diversion"),
    "10A - Joint Operation": Has("10A - Joint Operation"),
    "10B - Break In": Has("10B - Break In"),
    "11A - In Pursuit I": Has("11A - In Pursuit I"),
    "11B - In Pursuit II": Has("11B - In Pursuit II"),
    "13A - Alect Squadron": Has("13A - Alect Squadron"),
    "13B - Armada": Has("13B - Armada"),
    "14A - Fire Storm": Has("14A - Fire Storm"),
    "14B - Offline": Has("14B - Offline"),
}

def get_rule(loc: str) -> Rule:
    if loc in RULES:
        return RULES[loc]
    
    return True_()
