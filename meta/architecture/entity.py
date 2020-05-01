from meta.architecture import LogicError

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Dict, Any, Callable

class ProtoEntity(object):
    """
    Sets the type annotations for the dynamic variables
    """

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        for key in list(self.__annotations__.keys()):
            if key.startswith("_"):
                continue

            self.__annotations__[f"_{key}"] = self.__annotations__[key]

class Entity(ProtoEntity, metaclass=ABCMeta):
    """
    Create immutable class variables and auto-generate __init__ for subclass
    """

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

        keys = [k for k in self.__annotations__.keys() if not k.startswith("_")]
        assigned = keys[:]

        if len(args) > len(keys):
            raise LogicError(f"Too many arguments: {args}")

        for a, arg in enumerate(args):
            akey = keys[a]
            _akey = f"_{akey}"
            setattr(self, _akey, arg)
            setattr(Entity, akey, self._inject_property(akey))
            if akey in assigned:
                assigned.remove(akey)

        for key, value in kwargs.items():
            if key not in keys:
                raise LogicError(f"Keyword '{key}' is invalid")

            _key = f"_{key}"
            setattr(self, _key, value)
            setattr(Entity, key, self._inject_property(key))
            if key in assigned:
                assigned.remove(key)

        if len(assigned) > 0:
            unassigned = ", ".join(assigned)
            raise LogicError(f"Did not assign value to: {unassigned}")

    def _inject_property(self, attribute):
        def inject(self):
            return getattr(self, f"_{attribute}")

        return property(inject)
