import config as cfg
import os, zlib, requests, re, copy
from typing import Self
from util import prompt
from PatchUpdaterApp import PatchUpdaterApp
from PatchUpdaterDownloader import PatchUpdaterDownloader
from PatchUpdaterResponseDTO import PatchUpdaterResponseDTO


class PatchUpdaterRunner:
    _app: PatchUpdaterApp
    _hashes: dict[str, str]
    _inversed_hashes: dict[str, str]
    _awaiting_updates: dict[str, PatchUpdaterResponseDTO]
    _fetched_files: dict[str, str]
    _downloader: PatchUpdaterDownloader
    _result: dict[str, int]


    def __init__(self, app: PatchUpdaterApp):
        self._app = app
        self._downloader = PatchUpdaterDownloader()
        self._result = {"success": 0, "fail": 0}


    def scan_files(self) -> Self:
        self._hashes = {}
        for dir in self._app.get_config("scan_folders"):
            if not os.path.exists(os.path.expandvars(dir)):
                continue
            for file in os.listdir(os.path.expandvars(dir)):
                abs_file = os.path.join(os.path.expandvars(dir), file)
                if os.path.isdir(abs_file):
                    continue
                with open(abs_file, "rb") as file_b:
                    checksum = hex(zlib.crc32(file_b.read()))
                    self._hashes[abs_file] = f"0x{checksum[2:].upper().zfill(8)}"

        self._inversed_hashes = {self._hashes[a]: a for a in self._hashes}

        return self


    def get_update_queue(self) -> dict[str, PatchUpdaterResponseDTO]:
        return copy.deepcopy(self._awaiting_updates)


    def get_update_info(self) -> Self:
        response = requests.post(
            f"{cfg.B2WEB}{cfg.UPDATE_ENDPOINT}",
            None,
            {
                "version": cfg.VERSION,
                "check": list(self._hashes.values())
            },
            headers={
                "User-Agent": cfg.USER_AGENT,
                "Content-Type": "application/json",
            },
            timeout=5
        )

        if response.status_code != 200:
            print(response.text)
            raise Exception("Failed to fetch data from B2")

        self._awaiting_updates = {}
        for object in response.json():
            dto: PatchUpdaterResponseDTO = PatchUpdaterResponseDTO(**object)
            if dto.status == cfg.STATUS_NO_UPDATE:
                print(f"Detected file '{self._inversed_hashes[dto.checksum]}' as {dto.old_file.get("name")} version {dto.old_file.get("version")}, no updates available")
            elif dto.status == cfg.STATUS_UPDATE_AVAILABLE and dto.new_file.get("download"):
                print(f"Detected file '{self._inversed_hashes[dto.checksum]}' as {dto.old_file.get("name")} version {dto.old_file.get("version")}, update to version {dto.new_file.get("version")} is available")
                self._awaiting_updates[dto.checksum] = dto

        return self


    def set_downloader_attributes(self) -> Self:
        self._downloader.set_attributes(
            _tempdir=self._app.get_temp_dir(),
            _queue={checksum: self._awaiting_updates[checksum].new_file.get("download") for checksum in self._awaiting_updates}
        )
        return self


    def get_downloader(self) -> PatchUpdaterDownloader:
        return self._downloader


    def get_success(self) -> int:
        return self._result.get("success", 0)


    def get_fail(self) -> int:
        return self._result.get("fail", 0)


    def manage_downloaded(self) -> Self:
        successfull = {}
        for fname in os.listdir(self._app.get_temp_dir()):
            if not fname.endswith(".b2"):
                continue
            hash = fname.replace(".b2", "")
            file_to_replace = self._inversed_hashes.get(hash)
            if file_to_replace is None:
                continue

            temp = os.path.join(self._app.get_temp_dir(), fname)
            new_file = copy.copy(file_to_replace)
            for replace_pattern, replace_target in cfg.PATH_UPGRADES.items():
                search = re.search(replace_pattern, file_to_replace)
                if search is not None:
                    new_file = new_file.replace(search.group(1), replace_target)
                    break

            new_file = os.path.join(
                os.path.dirname(new_file),
                re.sub(
                    r"[\s]", 
                    " ", 
                    re.sub(
                        r"[^\w\s-]", 
                        "_", 
                        f"{self._awaiting_updates[hash].new_file.get("name")} {self._awaiting_updates[hash].new_file.get("version")}"
                    ) + os.path.splitext(new_file)[1]
                ).strip().replace("  ", " ")
            )

            if self._app.get_config("confirm_update") and not prompt(f"Update '{file_to_replace}'?"):
                continue
            os.replace(temp, new_file)
            if new_file != file_to_replace:
                os.remove(file_to_replace)

            successfull[hash] = new_file

        for checksum, dto in self._awaiting_updates.items():
            old_file, new_file = self._inversed_hashes[checksum], successfull.get(checksum)
            if new_file is None:
                print(f"Failed to update file '{old_file}' ({dto.old_file.get("name")} {dto.old_file.get("version")})")
                self._result["fail"] += 1
            else:
                print(f"'{old_file}' => '{new_file}' ({dto.old_file.get("name")} {dto.old_file.get("version")} => {dto.new_file.get("name")} {dto.new_file.get("version")})")
                self._result["success"] += 1

        return self
