from meta.architecture import LogicError, VObject

from typing import Dict, Any
from uuid import UUID, uuid4

class Entity(VObject):
    """
    Implements VObject, but includes a unique identifier
    """

    uuid: UUID

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inject("uuid", uuid4())
