from enum import StrEnum
from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json


class WagoAddonStability(StrEnum):
    STABLE = "stable"
    ALPHA = "alpha"
    BETA = "beta"


@dataclass_json
@dataclass
class WagoAddonMetadata:
    label: str  # Release name
    stability: WagoAddonStability  # Release stability
    changelog: str  # Release changelog as a markdown string

    # must have at least one of the following populated
    # each element is a list of supported patch versions for the given flavor
    supported_retail_patches: Optional[list[str]] = None
    supported_cata_patches: Optional[list[str]] = None
    supported_wotlk_patches: Optional[list[str]] = None
    supported_bc_patches: Optional[list[str]] = None
    supported_classic_patches: Optional[list[str]] = None


@dataclass_json
@dataclass
class WagoAddonsGameVersions:
    retail: list[str]
    cata: list[str]
    wotlk: list[str]
    bc: list[str]
    classic: list[str]


@dataclass_json
@dataclass
class WagoAddonsAddonCategory:
    id: int
    display_name: str
