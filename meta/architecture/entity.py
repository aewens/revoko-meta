from meta.architecture import LogicError

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Dict, Any, Callable

def prototype_with(prototype: Any) -> Callable[..., Any]:
    if not hasattr(prototype, "__annotations__"):
        raise LogicError(f"Cannot prototype using: {prototype}")

    def wrapper_prototype_with(cls) -> Callable[..., Any]:
        cls.__annotations__ = prototype.__annotations__

        return cls

    return wrapper_prototype_with

class Entity(metaclass=ABCMeta):
    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        keys = list(self.__annotations__.keys())
        assigned = [key for key in keys]

        if len(args) > len(keys):
            raise LogicError(f"Too many arguments: {args}")

        for a, arg in enumerate(args):
            akey = keys[a]
            setattr(self, akey, arg)
            assigned.remove(akey)

        for key, value in kwargs.items():
            if key not in keys:
                raise LogicError(f"Keyword '{key}' is invalid")

            setattr(self, key, value)
            assigned.remove(key)

        if len(assigned) > 0:
            unassigned = ", ".join(assigned)
            raise LogicError(f"Did not assign value to: {unassigned}")
