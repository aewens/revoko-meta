from meta.types import StrDict
from meta.architecture import LogicError

from typing import Tuple

class Namespace(object):
    """
    Immutable key value store
    """

    # NOTE - All keys for the immutable key value pairs
    __attrs__: Tuple[str, ...] = tuple()

    def __init__(self, *args: tuple, **kwargs: StrDict) -> None:
        """
        Inject in arguments as immutable key value pairs
        """
        arguments = self._resolve_arguments(*args, **kwargs)
        for key, value in arguments.items():
            self.inject(key, value)

    def _resolve_arguments(self, *args: tuple, **kwargs: StrDict) -> StrDict:
        """
        Resolve arbitrary arguments to dictionary using class type annotations
        """

        keys = [key for key in self.__annotations__.keys()]

        # Raise exceptions for missing or excessive arguments
        arguments_length = len(args) + len(kwargs)
        if arguments_length > len(keys):
            raise LogicError(f"Too many arguments: {args} {kwargs}")

        elif arguments_length < len(keys):
            raise LogicError(f"Too few arguments: {args} {kwargs}")

        # Match up arguments to their respective keys
        resolved = {keys[a]: arg for a, arg in enumerate(args)}

        # Merge resolved arguments with the remaining keyword arguments
        return {**resolved, **kwargs}

    def inject(self, key, value):
        """
        Set key value pair and lock them as immutable
        """

        # NOTE - This order is important, swapping will break immutability
        setattr(self, key, value)
        self.__attrs__ = (*self.__attrs__, key)

    def __setattr__(self, key, value):
        """
        Prevents immutable values from being mutated
        """

        if key in self.__attrs__:
            raise AttributeError(f"'{key}' is immutable")

        super().__setattr__(key, value)

    def __repr__(self):
        """
        Representation of the object for debugging 
        """

        attrs = self.__dict__.items()
        pairs = ", ".join(f"{k}={getattr(self, k)}" for k in self.__attrs__)
        return f"<{self.__class__.__name__}({pairs})>" 

    def __eq__(self, other):
        """
        Checks if other namespace has matching type and key value pairs
        """

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
    """
    Extension of Namespace for value object specific features
    """

    def __init__(self, *args: tuple, **kwargs: StrDict) -> None:
        super().__init__(*args, **kwargs)
