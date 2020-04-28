from meta.architecture import LogicError
from meta.architecture.entity import Entity, prototype_with
from enum import IntEnum, auto
from typing import NamedTuple, Dict, Any

class Phase(IntEnum):
    UNSTABLE = auto()
    ALPHA = auto()
    BETA = auto()
    RC = auto()
    STABLE = auto()

class VersionType(NamedTuple):
    major: int
    minor: int
    patch: int
    phase: Phase
    phase_index: int
    feature: str

#@prototype_with(VersionType)
class Version(Entity):
    major: int
    minor: int
    patch: int
    phase: Phase
    phase_index: int
    feature: str

    def _reset_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = dict()
        kwargs["major"] = 0
        kwargs["minor"] = 0
        kwargs["patch"] = 0
        kwargs["phase"] = Phase.STABLE
        kwargs["phase_index"] = 0
        kwargs["feature"] = ""
        return kwargs

    def _current_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = dict()
        kwargs["major"] = self.major
        kwargs["minor"] = self.minor
        kwargs["patch"] = self.patch
        kwargs["phase"] = self.phase
        kwargs["phase_index"] = self.phase_index
        kwargs["feature"] = self.feature
        return kwargs

    def _increase_major(self, major: int) -> "Version":
        if major <= 0:
            raise LogicError(f"Increase must be positive: {major}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self.major + major
        return Version(**kwargs)

    def _increase_minor(self, minor: int) -> "Version":
        if minor <= 0:
            raise LogicError(f"Increase must be positive: {minor}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self.major
        kwargs["minor"] = self.minor + minor
        return Version(**kwargs)

    def _increase_patch(self, patch: int) -> "Version":
        if patch <= 0:
            raise LogicError(f"Increase must be positive: {patch}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self.major
        kwargs["minor"] = self.minor
        kwargs["patch"] = self.patch + patch
        return Version(**kwargs)

    def _increase_phase_index(self, phase_index: int) -> "Version":
        if phase_index <= 0:
            raise LogicError(f"Increase must be positive: {phase_index}")

        kwargs = self._current_kwargs()
        kwargs["phase_index"] = self.phase_index + phase_index
        return Version(**kwargs)

    def bump_major(self) -> "Version":
        return self._increase_major(1)

    def bump_minor(self) -> "Version":
        return self._increase_minor(1)

    def bump_patch(self) -> "Version":
        return self._increase_patch(1)

    def bump_phase_index(self) -> "Version":
        return self._increase_phase_index(1)

    def bump_phase(self) -> "Version":
        mapping = dict()
        mapping[Phase.UNSTABLE] = Phase.ALPHA
        mapping[Phase.ALPHA] = Phase.BETA
        mapping[Phase.BETA] = Phase.RC
        mapping[Phase.RC] = Phase.STABLE

        next_phase = mapping.get(self.phase)
        if next_phase is None:
            raise LogicError(f"Cannot bump phase: {self.phase.name}")

        return self.transition_phase(next_phase)

    def transition_phase(self, phase: Phase) -> "Version":
        current = self.phase.value
        replace = phase.value
        if replace == current:
            return self

        elif replace < current:
            higher = self.phase.name
            lower = phase.name
            raise LogicError(f"{higher} cannot transition to {lower}")

        kwargs = self._current_kwargs()
        kwargs["phase"] = phase
        kwargs["phase_index"] = 0
        return Version(**kwargs)

    def set_feature(self, feature: str) -> "Version":
        kwargs: Dict[str, Any] = self._current_kwargs()
        kwargs["phase"] = Phase.UNSTABLE
        kwargs["phase_index"] = 0
        kwargs["feature"] = feature
        return Version(**kwargs)
