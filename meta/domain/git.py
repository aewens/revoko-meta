#from meta.architecture import LogicError
from meta.architecture.entity import Entity
from meta.domain.version import Version

from typing import List
from enum import IntEnum, auto

class GitCommit(Entity):
    sha1: str
    when: float

class GitBranchState(IntEnum):
    FEATURE = auto()
    TESTING = auto()
    STABLE = auto()

class GitBranch(Entity):
    name: str
    version: Version
    commit: GitCommit
    state: GitBranchState

class GitTag(Entity):
    branch: GitBranch
    version: Version

class GitRepo(Entity):
    repo: str
    current_branch: GitBranch
    branches: List[GitBranch]
    tags: List[GitTag]
    commits: List[GitCommit]
