from struct import pack, unpack
from ModIO import PspRamIO

CHECK_HOOK          = 0x08820E90
DL_HOOK             = 0x088707FC
CREDITS             = 0x08A80E38
MISSION_UNLOCK      = 0x08A80F10
AIR_CRAFT_STATUS    = 0x08A80E46
MISSION_RANKINGS    = 0x08A812F0
TIMER               = 0x08AA4968
HEALTH_PTR          = 0x08A82ED8 # +0xB0
IN_MISSION          = 0x08AA4964
MISSION_NAMES       = 0x08F6A324
AIRCRAFT_NAMES      = 0x08F67424

PATCH_1 = b'\x00\x0A\x01\x3C\x10\xE4\x21\x24\x02\x00\x29\x14\x00\x00\x00\x00\x04\x00\x03\x34\xA6\x83\x20\x0A\x24\x10\x43\x00'
PATCH_2 = b'\x80\x08\x01\x3C\x60\x00\x21\x24\x01\x00\x0F\x34\x00\x00\x2F\xA0\x1C\x02\x42\x8C\x01\xC2\x21\x0A\x80\x00\x42\x30'

AIRCRAFT_NAME_LIST: list[str] = [
    "FENRIR",
    "TYPHOON",
    "F-22",
    "F-14D",
    "RAFALE M",
    "F-16C",
    "F-16XL",
    "F-117A",
    "F-35",
    "F/B-22",
    "JA 37",
    "F-4E",
    "F-15E",
    "F/A-18E",
    "F-5E",
    "SU-27",
    "SU-37",
    "SU-47",
    "MIG-31",
    "MIG-29A",
    "MIG-21-93",
    "MIG-1.44",
    "F-2A",
    "F-1",
    "APALIS",
    "FREGATA",
    "FORNEUS",
    "CARIBURN",
    "XFA-27",
    "FALKEN",
    "X-02",
    "GRIPEN C",
    "TND-F3",
    "F-15S/MTD",
    "X-29A",
    "YF-23A",
    "A-10A",
    "A-6E",
    "MIR-2000D",
    "S-32",
]

MISSION_NAME_LIST: list[str] = [
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

ACE_NAMES: list[str] = [
    "NULL",
    'ZEPHYR',
    'PAIN',
    'SAVANNA',
    'TYRANT',
    'ICE',
    'BIEL',
    'INFERNO',
    'BECRUX',
    'ORCA',
    'SABER',
    'MANTA',
    'RAGE',
    'STORM',
    'GHOST',
    'ACRUX',
    'SORROW',
    'DUSK',
    'PALADIN',
    'FROST',
    'ROSE',
    'LANCER',
    'FURY',
    'SHIVA',
    "NULL",
    "NULL",
    "NULL",
    "NULL",
    "NULL",
    "NULL",
    "NULL",
    'RIOT',
    'GACRUX',
    'COMET',
    'VIPER',
    'SPIDER',
    'FIRESTORM',
    'ARI',
    'GARUDA',
    'ELIZA',
]


def unlock_purchases(ram) -> None:
    ram.seek(AIR_CRAFT_STATUS)
    for x in range(0x28):
        buf = unpack("h", ram.read(2))[0]
        ram.seek(-2, 1)
        ram.write(pack("h", buf | 1))

def apply_patch(ram, add, patch: bytes = b'') -> None:
    ram.seek(add)
    ram.write(patch)

def create_jump(ram, add: int, target: int, nop: int = 0) -> None:
    ram.seek(add)
    ram.write(pack("I", 0x08000000 | (target // 4)))
    ram.write(bytes(nop * 4))

def get_mission_name(ram, idx: int = 0) -> str:
    ram.seek(MISSION_NAMES + idx * 0x20)
    return ram.read(0x20).split(b'\x00')[0].decode("utf-8")

def get_aircraft_name(ram, idx: int = 0) -> str:
    ram.seek(AIRCRAFT_NAMES + idx * 0x20)
    return ram.read(0x20).split(b'\x00')[0].decode("utf-8")

class ACX_Interface:
    def __init__(self) -> None:
        self.ram: PspRamIO | None = None

    def setup(self) -> None:
        unlock_purchases(self.ram)
        apply_patch(self.ram, 0x8800000, PATCH_1)
        create_jump(self.ram, CHECK_HOOK, 0x8800000)
        apply_patch(self.ram, 0x8800030, PATCH_2)
        create_jump(self.ram, DL_HOOK, 0x8800030, 1)

    def give_credits(self, amount: int = 0) -> None:
        if self.ram is None:
            return
        self.ram.seek(CREDITS)
        current: int = unpack("i", self.ram.read(4))[0]
        self.ram.seek(CREDITS)
        self.ram.write(pack("i", current + amount))
    
    def get_credits(self) -> int:
        if self.ram is None:
            return 0
        self.ram.seek(CREDITS)
        return unpack("i", self.ram.read(4))[0]

    def unlock_aircraft(self, idx: int) -> None:
        if self.ram is None:
            return
        self.ram.seek(AIR_CRAFT_STATUS + 2 * idx)
        buf = unpack("h", self.ram.read(2))[0]
        self.ram.seek(-2, 1)
        self.ram.write(pack("h", buf | 4))

    def unlock_aircraft_by_name(self, name: str) -> None:
        self.unlock_aircraft(AIRCRAFT_NAME_LIST.index(name))

    def unlock_mission(self, idx: int) -> None:
        if self.ram is None:
            return
        self.ram.seek(MISSION_UNLOCK + idx * 0x20)
        self.ram.write(b'\x03')

    def unlock_mission_by_name(self, name: str) -> None:
        self.unlock_mission(MISSION_NAME_LIST.index(name))

    def check_missions(self, min_rank: int = 3) -> list[bool]:
        if self.ram is None:
            return [False] * 0x20
        self.ram.seek(MISSION_RANKINGS)
        return [unpack("<B31x", self.ram.read(0x20))[0] <= min_rank for _ in range(30)]

    def check_purchased_aircraft(self) -> list[bool]:
        if self.ram is None:
            return [False] * 0x28
        self.ram.seek(AIR_CRAFT_STATUS)
        return [(unpack("H", self.ram.read(0x2))[0] & 2) > 0 for _ in range(0x28)]

    def check_aces(self) -> list[bool]:
        if self.ram is None:
            return [False] * 0x28
        self.ram.seek(AIR_CRAFT_STATUS)
        return [(unpack("H", self.ram.read(0x2))[0] & 0x20) > 0 for _ in range(0x28)]

    def check_leseath_colors(self) -> list[bool]:
        if self.ram is None:
            return [False] * 0x28
        self.ram.seek(AIR_CRAFT_STATUS)
        return [(unpack("H", self.ram.read(0x2))[0] & 0x10) > 0 for _ in range(0x28)]

    def in_mission(self) -> bool:
        if self.ram is None:
            return False
        self.ram.seek(IN_MISSION)
        buf: bytes = self.ram.read(2)
        return buf == b'\x02\x80'

    def check_dead(self) -> bool:
        if self.ram is None:
            return False
        self.ram.seek(0x08800060)
        buf = self.ram.read(1)
        self.ram.seek(-1, 1)
        self.ram.write(b'\x00')
        return buf != b'\x00'

    def kill(self) -> None:
        if self.ram is None:
            return
        self.ram.seek(HEALTH_PTR)
        self.ram.seek(unpack("<I", self.ram.read(4))[0] + 0xB0)
        self.ram.write(b'\x00\x00')

    def connect(self) -> bool:
        try:
            self.ram = PspRamIO()
            return True
        except:
            return False
