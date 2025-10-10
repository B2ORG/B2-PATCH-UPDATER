import dataclasses

@dataclasses.dataclass(frozen=True)
class PatchUpdaterConfig:
    scan_folders: list[str]
    confirm_update: bool

