from meta.creating.version import Version

from typing import NamedTuple

class Dependency(NamedTuple):
    name: str
    parent: str
    version: Version

