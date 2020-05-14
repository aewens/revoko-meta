from meta.types import StrDict
from meta.architecture import LogicError, VObject

from typing import Dict, Any
from uuid import UUID, uuid4

class Entity(VObject):
    """
    Extension of VObject for domain entity specific features
    """

    uuid: UUID

    def __init__(self, *args: tuple, **kwargs: StrDict) -> None:
        super().__init__(*args, **kwargs)
        self.inject("uuid", uuid4())
