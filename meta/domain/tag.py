from meta.domain.branch import Branch 
from meta.domain.version import Version

from typing import NamedTuple

class Tag(NamedTuple):
    branch: Branch
    version: Version
