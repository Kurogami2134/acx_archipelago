from BaseClasses import Item, ItemClassification, Location, Region
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import launch_subprocess, components, Component, Type

from typing import List

from .rules import get_rule
from .items import ACXItem, item_list, item_id_to_name, item_name_to_id, filler_items, item_table
from .locations import ACXLocation, normal_locations, aces_locations, location_list, location_id_to_name, location_name_to_id
from .options import ACXOptions


def launch_client(*args: str) -> None:
    from .client import launch
    launch_subprocess(launch, name="ACXClient", args=args)


components.append(Component(
    "ACX Client",
    "ACXClient",
    func=launch_client,
    supports_uri=True,
    game_name="Ace Combat X: Skies of Deception",
    component_type=Type.CLIENT)
)


# add web world
class ACXWebWorld(WebWorld):
    ...

class ACXWorld(World):
    """ INFO """

    game = "Ace Combat X: Skies of Deception"
    web = ACXWebWorld()
    item_id_to_name = item_id_to_name
    item_name_to_id = item_name_to_id

    location_id_to_name = location_id_to_name
    location_name_to_id = location_name_to_id

    options_dataclass = ACXOptions
    options: ACXOptions
    item_pool: List[ACXItem]

    def create_item(self, name: str, classification: ItemClassification = ItemClassification.filler) -> Item:
        return ACXItem(name, classification, self.item_name_to_id[name], self.player)
    
    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_items)
    
    def create_items(self) -> None:
        for item_name in item_list:
            self.multiworld.itempool.append(self.create_item(item_name, item_table[item_name].item_type))
        
        pre_filled = len(self.multiworld.itempool)
        to_fill = len(self.get_region("Game").locations)
        if (to_fill - pre_filled) > 0:
            print(f"Adding Filler {to_fill - pre_filled}")
            for _ in range(to_fill - pre_filled):
                self.multiworld.itempool.append(self.create_filler())

    def fill_slot_data(self) -> dict:
        return {
            "death_link": self.options.death_link.value,
            "required_missions": self.options.required_missions.value,
            "starting_credits": self.options.starting_credits.value,
            "min_rank":self.options.min_rank.value,
            "objective": self.options.objective_to_win.value
        }

    def place_item(self, location_name: str, item_name: str) -> None:
        ...
    
    def create_regions(self) -> None:
        def create_location(name: str) -> ACXLocation:
            return ACXLocation(
                self.player,
                name,
                location_name_to_id[name],
                game_region,
            )

        menu_region = Region(
            "Menu",
            self.player,
            self.multiworld,
        )
        game_region = Region(
            "Game",
            self.player,
            self.multiworld,
        )
        menu_region.connect(game_region)
        self.multiworld.regions.append(menu_region)
        self.multiworld.regions.append(game_region)
        
        locations: List[str] = []
        
        locations.extend(normal_locations) 
        if self.options.randomize_aces:
            locations.extend(aces_locations)

        for loc in locations:
            location: ACXLocation = create_location(loc)
            self.set_rule(location, get_rule(loc))
            game_region.locations.append(location)
        """
        match self.options.objective_to_win:
            case WinCondition.hunt_ala:
                if not self.options.hunted_monsters_in_pool:
                    loc = "Hunt Alatreon"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            case WinCondition.hunt_ama:
                if not self.options.hunted_monsters_in_pool:
                    loc = "Hunt Amatsu Magatsuchi"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            case WinCondition.hunt_jhen:
                if not self.options.hunted_monsters_in_pool:
                    loc = "Hunt Jhen Mohran"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            case WinCondition.ala_quest:
                if not self.options.gh_quests_in_pool or not self.options.normal_quests_in_pool:
                    loc = "Guild 8* Quest 38"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            case WinCondition.ama_quest:
                if not self.options.gh_quests_in_pool or not self.options.urgent_quests_in_pool:
                    loc = "Guild 8* Quest 40"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            case WinCondition.jhen_quest:
                if not self.options.gh_quests_in_pool or not self.options.urgent_quests_in_pool:
                    loc = "Guild 8* Quest 39"
                    location: P3rdLocation = create_location(loc)
                    self.set_rule(location, get_rule(loc))
                    game_region.locations.append(location)
            """

    
    def generate_basic(self) -> None:
        #  Add win condition
        # game_clear: ACXItem = ACXItem("Game Clear", ItemClassification.progression_skip_balancing, 213412, self.player)
        # location: Location
        # match self.options.objective_to_win:
        #     case WinCondition.hunt_ala:
        #         location = self.multiworld.get_location("Hunt Alatreon", self.player)
        #     case WinCondition.hunt_ama:
        #         location = self.multiworld.get_location("Hunt Amatsu Magatsuchi", self.player)
        #     case WinCondition.hunt_jhen:
        #         location = self.multiworld.get_location("Hunt Jhen Mohran", self.player)
        #     case WinCondition.ala_quest:
        #         location = self.multiworld.get_location("Guild 8* Quest 38", self.player)
        #     case WinCondition.ama_quest:
        #         location = self.multiworld.get_location("Guild 8* Quest 40", self.player)
        #     case WinCondition.jhen_quest:
        #         location = self.multiworld.get_location("Guild 8* Quest 39", self.player)
        # location.place_locked_item(game_clear)
        ...
