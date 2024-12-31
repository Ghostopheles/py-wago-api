from typing import Optional
from collections.abc import Iterable
from dataclasses import dataclass, field


class BaseModel:
    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)


@dataclass(repr=False)
class Version:
    major: int
    minor: int
    patch: int
    build: int

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}.{self.build}"

    @classmethod
    def from_str(cls, version: str):
        version_split = version.split(".")
        return cls(*version_split)


@dataclass
class Build(BaseModel):
    product: str
    version: Version
    created_at: str
    build_config: str
    product_config: str
    cdn_config: str
    is_bgdl: bool = field(default=False)

    def __post_init__(self):
        self.version = Version.from_str(self.version)


@dataclass
class FileInfoContentHash(BaseModel):
    version: Version
    product: str
    md5: str
    fdid: int

    def __post_init__(self):
        self.version = Version.from_str(self.version)


class FileInfoContentHashes(Iterable):
    def __init__(self, data: list):
        self.__data = [FileInfoContentHash.from_json(entry) for entry in data]

    def __iter__(self):
        return iter(self.__data)


@dataclass
class FileInfo(BaseModel):
    fdid: int
    latest: dict[str, FileInfoContentHash]
    chashes: FileInfoContentHashes
    filename: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)

    def __post_init__(self):
        self.latest = {
            key: FileInfoContentHash.from_json(value)
            for key, value in self.latest.items()
        }
        self.chashes = FileInfoContentHashes(self.chashes)
