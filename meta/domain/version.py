from enum import Enum, unique
from typing import NamedTuple

@unique
class Phase(Enum):
    UNSTABLE = 0
    ALPHA = 1
    BETA = 2
    RC = 3
    STABLE = 4

class Version(NamedTuple):
    major: int
    minor: int
    patch: int
    phase: Phase
    phase_index: int
    feature: str
