import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class PatchUpdaterResponseDTO:
    checksum: str
    status: str
    old_file: Optional[dict[str, int|str|None]]
    new_file: Optional[dict[str, int|str|None]]
