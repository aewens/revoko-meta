from meta.creating.version import Version
from meta.creating.dependency import Dependency

from typing import NamedTuple, Dict

class Metadata(NamedTuple):
    name: str
    schema: int
    version: Version
    depends: Dict[str, Dependency]
