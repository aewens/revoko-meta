from meta.architecture import LogicError
from meta.architecture.entity import Entity
from enum import IntEnum, auto
from typing import Dict, Any

class VersionPhase(IntEnum):
    UNSTABLE = auto()
    ALPHA = auto()
    BETA = auto()
    RC = auto()
    STABLE = auto()

class Version(Entity):
    major: int
    minor: int
    patch: int
    phase: VersionPhase
    phase_index: int
    feature: str

    def _reset_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = dict()
        kwargs["major"] = 0
        kwargs["minor"] = 0
        kwargs["patch"] = 0
        kwargs["phase"] = VersionPhase.STABLE
        kwargs["phase_index"] = 0
        kwargs["feature"] = ""
        return kwargs

    def _current_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = dict()
        kwargs["major"] = self._major
        kwargs["minor"] = self._minor
        kwargs["patch"] = self._patch
        kwargs["phase"] = self._phase
        kwargs["phase_index"] = self._phase_index
        kwargs["feature"] = self._feature
        return kwargs

    def _increase_major(self, major: int) -> "Version":
        if major <= 0:
            raise LogicError(f"Increase must be positive: {major}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self._major + major
        return Version(**kwargs)

    def _increase_minor(self, minor: int) -> "Version":
        if minor <= 0:
            raise LogicError(f"Increase must be positive: {minor}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self._major
        kwargs["minor"] = self._minor + minor
        return Version(**kwargs)

    def _increase_patch(self, patch: int) -> "Version":
        if patch <= 0:
            raise LogicError(f"Increase must be positive: {patch}")

        kwargs = self._reset_kwargs()
        kwargs["major"] = self._major
        kwargs["minor"] = self._minor
        kwargs["patch"] = self._patch + patch
        return Version(**kwargs)

    def _increase_phase_index(self, phase_index: int) -> "Version":
        if phase_index <= 0:
            raise LogicError(f"Increase must be positive: {phase_index}")

        kwargs = self._current_kwargs()
        kwargs["phase_index"] = self._phase_index + phase_index
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
        mapping[VersionPhase.UNSTABLE] = VersionPhase.ALPHA
        mapping[VersionPhase.ALPHA] = VersionPhase.BETA
        mapping[VersionPhase.BETA] = VersionPhase.RC
        mapping[VersionPhase.RC] = VersionPhase.STABLE

        next_phase = mapping.get(self._phase)
        if next_phase is None:
            raise LogicError(f"Cannot bump phase: {self._phase.name}")

        return self.transition_phase(next_phase)

    def transition_phase(self, phase: VersionPhase) -> "Version":
        current = self._phase.value
        replace = phase.value
        if replace == current:
            return self

        elif replace < current:
            higher = self._phase.name
            lower = phase.name
            raise LogicError(f"{higher} cannot transition to {lower}")

        kwargs = self._current_kwargs()
        kwargs["phase"] = phase
        kwargs["phase_index"] = 0
        return Version(**kwargs)

    def set_feature(self, feature: str) -> "Version":
        kwargs: Dict[str, Any] = self._current_kwargs()
        kwargs["phase"] = VersionPhase.UNSTABLE
        kwargs["phase_index"] = 0
        kwargs["feature"] = feature
        return Version(**kwargs)
