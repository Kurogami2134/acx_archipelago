from typing import NamedTuple, Dict, List

from BaseClasses import Item, ItemClassification


class ACXItem(Item):
    game = "Ace Combat X: Skies of Deception"

class ACXItemData(NamedTuple):
    code: int
    item_type: ItemClassification

ascx_base_item_id = 21340000 + 1000

item_list: Dict[str, ItemClassification] = {
    "FENRIR":                           ItemClassification.useful,
    "TYPHOON":                          ItemClassification.useful,
    "F-22":                             ItemClassification.useful,
    "F-14D":                            ItemClassification.useful,
    "RAFALE M":                         ItemClassification.useful,
    "F-16C":                            ItemClassification.useful,
    "F-16XL":                           ItemClassification.useful,
    "F-117A":                           ItemClassification.useful,
    "F-35":                             ItemClassification.useful,
    "F/B-22":                           ItemClassification.useful,
    "JA 37":                            ItemClassification.useful,
    "F-15E":                            ItemClassification.useful,
    "F/A-18E":                          ItemClassification.useful,
    "F-5E":                             ItemClassification.useful,
    "SU-27":                            ItemClassification.useful,
    "SU-37":                            ItemClassification.useful,
    "SU-47":                            ItemClassification.useful,
    "MIG-31":                           ItemClassification.useful,
    "MIG-29A":                          ItemClassification.useful,
    "MIG-21-93":                        ItemClassification.useful,
    "MIG-1.44":                         ItemClassification.useful,
    "F-2A":                             ItemClassification.useful,
    "F-1":                              ItemClassification.useful,
    "APALIS":                           ItemClassification.useful,
    "FREGATA":                          ItemClassification.useful,
    "FORNEUS":                          ItemClassification.useful,
    "CARIBURN":                         ItemClassification.useful,
    "XFA-27":                           ItemClassification.useful,
    "FALKEN":                           ItemClassification.useful,
    "X-02":                             ItemClassification.useful,
    "GRIPEN C":                         ItemClassification.useful,
    "TND-F3":                           ItemClassification.useful,
    "F-15S/MTD":                        ItemClassification.useful,
    "X-29A":                            ItemClassification.useful,
    "YF-23A":                           ItemClassification.useful,
    "A-10A":                            ItemClassification.useful,
    "A-6E":                             ItemClassification.useful,
    "MIR-2000D":                        ItemClassification.useful,
    "S-32":                             ItemClassification.useful,

    "03A - Prelude":                    ItemClassification.progression,
    "03B - Captive City":               ItemClassification.progression,
    "07A - Standoff in the Skies I":    ItemClassification.progression,
    "07B - Standoff in the Skies II":   ItemClassification.progression,
    "07C - Time Limit":                 ItemClassification.progression,
    "12A - Gaiuss Tower":               ItemClassification.progression,
    "12B - Atmos Ring":                 ItemClassification.progression,
    "12C - Wild Card":                  ItemClassification.progression,
    "15A - End of Deception I":         ItemClassification.progression,
    "15B - End of Deception II":        ItemClassification.progression,
    "02 - Out of the Fire":             ItemClassification.progression,
    "04A - Last Line of Defense":       ItemClassification.progression,
    "04B - False Target":               ItemClassification.progression,
    "05A - Rolling Thunder":            ItemClassification.progression,
    "05B - Pinned Down":                ItemClassification.progression,
    "06A - The Midnight Sun":           ItemClassification.progression,
    "06B - Ice Bound":                  ItemClassification.progression,
    "08A - Striking Point":             ItemClassification.progression,
    "08B - The Wasteland":              ItemClassification.progression,
    "09A - Blitz":                      ItemClassification.progression,
    "09B - A Diversion":                ItemClassification.progression,
    "10A - Joint Operation":            ItemClassification.progression,
    "10B - Break In":                   ItemClassification.progression,
    "11A - In Pursuit I":               ItemClassification.progression,
    "11B - In Pursuit II":              ItemClassification.progression,
    "13A - Alect Squadron":             ItemClassification.progression,
    "13B - Armada":                     ItemClassification.progression,
    "14A - Fire Storm":                 ItemClassification.progression,
    "14B - Offline":                    ItemClassification.progression,

    # filler
    "5000 Credits":                     ItemClassification.filler,
    "10000 Credits":                    ItemClassification.filler,
}

item_table: Dict[str, ACXItemData] = {
    name: ACXItemData(ascx_base_item_id + idx, item_type) for idx, (name, item_type) in enumerate(item_list.items())
}

filler_items: List[str] = [
    name for name, data in item_list.items() if data is ItemClassification.filler
]

item_name_to_id: Dict[str, int] = {
    name: data.code for name, data in item_table.items()
}


item_id_to_name: Dict[int, str] = {
    data.code: name for name, data in item_table.items()
}

