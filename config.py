VERSION = "0.9"
USER_AGENT = "B2-PATCH-UPDATER/" + VERSION
APPDATA = r"%localappdata%\B2PatchUpdater"
CONFIG = "b2_patch_updater.json"
TEMP = "temp"
B2WEB = "https://b2.wtf/"
UPDATE_ENDPOINT = "api/gsc/v1/check-for-updates/"
STATUS_UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
STATUS_NO_UPDATE = "NO_UPDATES"

CONFIG_DEFAULTS = {
    "scan_folders": [
        "%localappdata%\\Plutonium\\plugins",
        "%localappdata%\\Plutonium\\storage\\t4\\scripts\\sp",
        "%localappdata%\\Plutonium\\storage\\t4\\raw\\scripts\\sp",
        "%localappdata%\\Plutonium\\storage\\t6\\scripts\\zm",
        "%localappdata%\\Plutonium\\storage\\t6\\raw\\scripts\\zm",
    ],
    "confirm_update": False,
}
PATH_UPGRADES = {
    ".*(\\\\storage\\\\t4\\\\scripts\\\\sp)": "\\storage\\t4\\raw\\scripts\\sp",
    ".*(\\\\storage\\\\t6\\\\scripts\\\\zm)": "\\storage\\t6\\raw\\scripts\\zm"
}