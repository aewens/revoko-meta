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
    def __init__(self, metadata: Metadata, repo: GitRepo) -> None:
        self._metadata = metadata
        self._repo = repo
        self._version = self._metadata.version
        self._branch = self._repo.current_branch 

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @property
    def repo(self) -> GitRepo:
        return self._repo

    @property
    def version(self) -> Version:
        return self._version

    @property
    def branch(self) -> GitBranch:
        return self._branch
