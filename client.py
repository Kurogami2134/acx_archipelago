from json import dumps as json_dump, loads as json_load
from CommonClient import CommonContext, ClientCommandProcessor, gui_enabled, get_base_parser, server_loop, ClientStatus


from .acx_if import ACX_Interface, AIRCRAFT_NAME_LIST, MISSION_NAME_LIST
from .locations import location_name_to_id, location_id_to_name
from .items import item_id_to_name, ACXItem

import asyncio


from websockets import Subprotocol
from websockets.legacy import client


class ACXCommandProcessor(ClientCommandProcessor):
    def _cmd_psp(self) -> None:
        """
        Trigger a connection/re-connection to PPSSPP.
        """
        asyncio.create_task(connect_psp(self.ctx))

class ACXContext(CommonContext):
    game = "Ace Combat X: Skies of Deception"
    tags = {"AP"}
    items_handling = 0b111
    game_interface: ACX_Interface | None = None
    command_processor = ACXCommandProcessor
    watcher_task: asyncio.Task | None = None
    #event_receiver_task: asyncio.Task | None = None
    #update_task: asyncio.Task | None = None

    already_dead = False
    dying = False
    just_got_dld = False
    locations_checked: set[int] = set()
    slot_data = None
    want_slot_data: bool = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ACXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game="Ace Combat X: Skies of Deception")

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)
    
    async def send_location_by_name(self, name) -> None:
        if name in location_name_to_id:
            lid = location_name_to_id[name]
            self.locations_checked.add(lid)
            await self.send_msgs([{"cmd": "LocationChecks", "locations": self.locations_checked}])
        else:
            print(f'Invalid Location: {name}.')

    def give_item(self, item: ACXItem) -> None:
        print(item)
        if self.game_interface is None:
            return
        if (" - " in item_id_to_name[item.item]): #  Missions
            print("Sending")
            self.game_interface.unlock_mission_by_name(item_id_to_name[item.item])
        elif "Credits" in item_id_to_name[item.item]: #  Credits
            self.game_interface.give_credits(int(item_id_to_name[item.item].split(" ")[0]))
        else: #  Aircraft
            self.game_interface.unlock_aircraft_by_name(item_id_to_name[item.item])
    
    def on_package(self, cmd: str, args: dict):
        match cmd:
            case "Connected":
                self.slot_data = args["slot_data"]
                if self.game_interface is not None and self.game_interface.get_credits() == 0:
                    self.game_interface.give_credits(self.slot_data["starting_credits"])
            case "ReceivedItems":
                print(args)
                for item in args['items']:
                    print(f'{item_id_to_name[item.item]} from {location_id_to_name[item.location] if item.location in location_id_to_name else "idk"}')
                    self.give_item(item)
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and not self.already_dead:
            self.dying = True

async def game_watcher(ctx: ACXContext):
    while not ctx.exit_event.is_set():

        print("GAME")

        if not (ctx.game_interface is None or ctx.game_interface.ram is None):

            if not (ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.slot is None or ctx.game_interface is None):
                try:
                    if "DeathLink" not in ctx.tags and ctx.slot_data["death_link"]:
                        await ctx.update_death_link(True)

                    is_in_mission: bool = ctx.game_interface.in_mission()

                    should_send_dl: bool = ctx.game_interface.check_dead()
                    if should_send_dl and ctx.just_got_dld:
                        ctx.just_got_dld = False
                    elif should_send_dl:
                        ctx.send_death()
                    
                    if is_in_mission:
                        if ctx.dying:
                            ctx.game_interface.kill()
                            ctx.dying = False
                            print("DEATHLINKINGPUM")
                        print("IN")
                    else:
                        local_checks: set[int] = set()

                        mission_status: list[bool] = ctx.game_interface.check_missions()
                        aircraft_status: list[bool] = ctx.game_interface.check_purchased_aircraft()
                        for idx, done in enumerate(mission_status):
                            if done:
                                # print(f'{idx}, {MISSION_NAME_LIST[idx]}, {location_name_to_id[MISSION_NAME_LIST[idx]]}')
                                local_checks.add(location_name_to_id[MISSION_NAME_LIST[idx]])
                        for idx, bought in enumerate(aircraft_status):
                            if idx == 11:  # Skip F-4E
                                continue
                            if bought:
                                local_checks.add(location_name_to_id[f'Bought {AIRCRAFT_NAME_LIST[idx]}'])
                        if ctx.locations_checked != local_checks:
                            ctx.locations_checked = local_checks
                            if local_checks is not None:
                                await ctx.send_msgs([{
                                    "cmd": "LocationChecks",
                                    "locations": local_checks
                                }])
                        victory = False

                        match ctx.slot_data["objective"]:
                            case 0: #  Mission sanity
                                victory = len([x for x in mission_status if x]) >= 10
                            case 1: #  15A
                                victory = mission_status[8]
                            case 2: #  15B
                                victory = mission_status[9]
                            case 3: #  15 either
                                victory = mission_status[8] or mission_status[9]

                        if (not ctx.finished_game) and victory:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                except:
                    ...
        await asyncio.sleep(0.1)

async def connect_psp(ctx: ACXContext) -> None:
    ctx.game_interface = ACX_Interface()
    while not ctx.game_interface.connect():
        if ctx.game_interface.connect():
            break
    ctx.game_interface.setup()
        

async def main(args) -> None:
    ctx = ACXContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Connect
    await connect_psp(ctx)
    print("Base Setup Done")

    ctx.watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")
    #if ctx.watcher_task:
    #    await ctx.watcher_task
    
    await ctx.exit_event.wait()
    await ctx.shutdown()



def launch(*launch_args: str) -> None:
    import colorama
    import urllib.parse
    colorama.init()
    parser = get_base_parser()
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(launch_args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            if url.password:
                args.password = urllib.parse.unquote(url.password)
            if url.username:
                args.connect = f'{urllib.parse.unquote(url.username)}:None@{url.hostname}:{url.port}'
            else:
                args.connect = f'{url.hostname}:{url.port}'

        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    launch()
