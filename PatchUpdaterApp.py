import config as cfg
import os, json, shutil, copy
from typing import Self, Optional
from PatchUpdaterConfig import PatchUpdaterConfig


class PatchUpdaterApp:
    _appdata_dir: str
    _temp_dir: str
    _conf_file: str
    _conf: PatchUpdaterConfig


    def __init__(self):
        self._appdata_dir = os.path.expandvars(cfg.APPDATA)
        self._conf_file = os.path.join(self._appdata_dir, cfg.CONFIG)
        self._temp_dir = os.path.join(self._appdata_dir, cfg.TEMP)


    def get_appdata_dir(self) -> str:
        return copy.copy(self._appdata_dir)


    def get_temp_dir(self) -> str:
        return copy.copy(self._temp_dir)


    def prepare_environment(self) -> Self:
        os.makedirs(self._appdata_dir, exist_ok=True)

        if os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
        os.makedirs(self._temp_dir, exist_ok=True)

        if not os.path.exists(self._conf_file):
            with open(self._conf_file, "w", encoding="utf-8") as json_io:
                json.dump(cfg.CONFIG_DEFAULTS, json_io, indent=4)
        return self


    def load_config(self) -> Self:
        assert os.path.exists(self._conf_file), "Config file not found on load"
        with open(self._conf_file, "r", encoding="utf-8") as json_io:
            self._conf = PatchUpdaterConfig(**json.load(json_io))
        return self


    def get_config(self, key: Optional[str] = None):
        if key is None:
            return self._conf
        return getattr(self._conf, key)
