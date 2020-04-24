from meta.creating.version import Version

from typing import NamedTuple

class Branch(NamedTuple):
    name: str
    commit: str
    version: Version
