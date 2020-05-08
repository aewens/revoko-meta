from meta.architecture import LogicError

from typing import NamedTuple, Dict, Any, Callable

class ProtoValueObject(object):
    """
    Sets the type annotations for the dynamic variables
    """

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        for key in list(self.__annotations__.keys()):
            if key.startswith("_"):
                continue

            self.__dict__[key] = self.__annotations__[key]
            self.__dict__[f"_{key}"] = self.__dict__[key]

class VObject(ProtoValueObject):
    """
    Create immutable class variables and auto-generate __init__ for subclass
    """

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

        keys = [k for k in self.__dict__.keys() if not k.startswith("_")]
        assigned = keys[:]

        if len(args) > len(keys):
            raise LogicError(f"Too many arguments: {args}")

        for a, arg in enumerate(args):
            akey = keys[a]
            _akey = f"_{akey}"
            setattr(self, _akey, arg)
            setattr(VObject, akey, self._inject_property(akey))
            if akey in assigned:
                assigned.remove(akey)

        for key, value in kwargs.items():
            if key not in keys:
                raise LogicError(f"Keyword '{key}' is invalid")

            _key = f"_{key}"
            setattr(self, _key, value)
            setattr(VObject, key, self._inject_property(key))
            if key in assigned:
                assigned.remove(key)

        if len(assigned) > 0:
            unassigned = ", ".join(assigned)
            raise LogicError(f"Did not assign value to: {unassigned}")

    def _inject_property(self, attribute):
        def inject(self):
            return getattr(self, f"_{attribute}")

        return property(inject)

    def __repr__(self):
        attrs = self.__dict__.items()
        pairs = ", ".join(f"{k}={v}" for k, v in attrs if not k.startswith("_"))
        return f"<{self.__class__.__name}({pairs})>" 

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        self_dict = self.__dict__
        other_dict = other.__dict__
        if len(self_dict) != len(other_dict):
            return False

        for key, value in other_dict.items():
            if value != self_dict.get(key):
                return False

        return True

