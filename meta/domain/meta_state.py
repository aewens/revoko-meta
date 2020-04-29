#from meta.architecture import LogicError
#from meta.architecture.entity import Entity
from meta.domain.git import GitBranchState, GitCommit
from meta.domain.git import GitBranch, GitTag, GitRepo
from meta.domain.version import Version, VersionPhase
from meta.domain.dependency import Dependency
from meta.domain.metadata import Metadata

#from enum import IntEnum, auto
from typing import Dict, Any

class MetaState(object):
    def __init__(self, metadata, git_repo):
        self._metadata = metadata
        self._git_repo = git_repo
        self._version = self._metdata.version
        self._branch = self._git_repo.current_branch 

    @property
    def metadata(self):
        return self._metadata

    @property
    def git_repo(self):
        return self._git_repo

    @property
    def version(self):
        return self._version

    @property
    def branch(self):
        return self._branch
