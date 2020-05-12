from meta.architecture import LogicError

from typing import Dict, Tuple, Any

class Namespace(object):
    """
    Immutable key value store
    """

    __attrs__: Tuple[str, ...] = tuple()

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        arguments = self._resolve_arguments(*args, **kwargs)
        for key, value in arguments.items():
            self.inject(key, value)

    def _resolve_arguments(self, *args: tuple,
        **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        key: str
        keys = [key for key in self.__annotations__.keys()]

        arguments_length = len(args) + len(kwargs)
        if arguments_length > len(keys):
            raise LogicError(f"Too many arguments: {args} {kwargs}")

        elif arguments_length < len(keys):
            raise LogicError(f"Too few arguments: {args} {kwargs}")

        resolved = {keys[a]: arg for a, arg in enumerate(args)}
        return {**resolved, **kwargs}

    def inject(self, key, value):
        setattr(self, key, value)
        self.__attrs__ = (*self.__attrs__, key)

    def __setattr__(self, key, value):
        if key in self.__attrs__:
            raise AttributeError(f"'{key}' is immutable")

        super().__setattr__(key, value)

    def __repr__(self):
        attrs = self.__dict__.items()
        pairs = ", ".join(f"{k}={getattr(self, k)}" for k in self.__attrs__)
        return f"<{self.__class__.__name__}({pairs})>" 

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        self_attrs = self.__attrs__
        other_attrs = other.__attrs__
        if len(self_attrs) != len(other_attrs):
            return False

        for key in other_attrs:
            if getattr(other, key, None) != getattr(self, key, None):
                return False

        return True

class VObject(Namespace):
    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
