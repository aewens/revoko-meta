from meta.domain.version import Version
from meta.domain.dependency import Dependency

from typing import NamedTuple, Dict

class Metadata(NamedTuple):
    name: str
    schema: int
    version: Version
    depends: Dict[str, Dependency]
