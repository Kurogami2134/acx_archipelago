from typing import Dict, List


from BaseClasses import Location

acx_base_loc_id    = 21340000

class ACXLocation(Location):
    game: str = "Ace Combat X: Skies of Deception"

location_clear_quests: List[str] = [
    
]

location_list: List[str] = [
    # purchase every aircraft
    "Bought FENRIR",
    "Bought TYPHOON",
    "Bought F-22",
    "Bought F-14D",
    "Bought RAFALE M",
    "Bought F-16C",
    "Bought F-16XL",
    "Bought F-117A",
    "Bought F-35",
    "Bought F/B-22",
    "Bought JA 37",
    "Bought F-15E",
    "Bought F/A-18E",
    "Bought F-5E",
    "Bought SU-27",
    "Bought SU-37",
    "Bought SU-47",
    "Bought MIG-31",
    "Bought MIG-29A",
    "Bought MIG-21-93",
    "Bought MIG-1.44",
    "Bought F-2A",
    "Bought F-1",
    "Bought APALIS",
    "Bought FREGATA",
    "Bought FORNEUS",
    "Bought CARIBURN",
    "Bought XFA-27",
    "Bought FALKEN",
    "Bought X-02",
    "Bought GRIPEN C",
    "Bought TND-F3",
    "Bought F-15S/MTD",
    "Bought X-29A",
    "Bought YF-23A",
    "Bought A-10A",
    "Bought A-6E",
    "Bought MIR-2000D",
    "Bought S-32",
    
    # complete every mission
    "03A - Prelude",
    "03B - Captive City",
    "07A - Standoff in the Skies I",
    "07B - Standoff in the Skies II",
    "07C - Time Limit",
    "12A - Gaiuss Tower",
    "12B - Atmos Ring",
    "12C - Wild Card",
    "15A - End of Deception I",
    "15B - End of Deception II",
    "01 - Skies of Deception",
    "02 - Out of the Fire",
    "04A - Last Line of Defense",
    "04B - False Target",
    "05A - Rolling Thunder",
    "05B - Pinned Down",
    "06A - The Midnight Sun",
    "06B - Ice Bound",
    "08A - Striking Point",
    "08B - The Wasteland",
    "09A - Blitz",
    "09B - A Diversion",
    "10A - Joint Operation",
    "10B - Break In",
    "11A - In Pursuit I",
    "11B - In Pursuit II",
    "13A - Alect Squadron",
    "13B - Armada",
    "14A - Fire Storm",
    "14B - Offline",
]

location_name_to_id: Dict[str, int] = {
    name: acx_base_loc_id + idx for idx, name in enumerate(location_list)
}

location_id_to_name = {code: name for name, code in location_name_to_id.items()}
