from meta.creating.branch import Branch 
from meta.creating.version import Version

from typing import NamedTuple

class Tag(NamedTuple):
    branch: Branch
    version: Version
