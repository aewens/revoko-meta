from meta.architecture import LogicError, VObject

from typing import Dict, Any
from uuid import uuid4

class Entity(VObject):
    """
    Implements VObject, but includes a unique identifier
    """

    def __init__(self, *args: tuple, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

        self._uuid = uuid4()

    @property
    def uuid(self):
        return self._uuid
