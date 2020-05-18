from meta.types import StrDict
from meta.architecture import LogicError, Namespace, Entity

from abc import ABCMeta, abstractmethod
from typing import Any, List, Tuple, Callable
from time import time

class Event(Entity):
    """
    Captures an event that occurred during the lifetime of the process
    """

    created: float

    def __init__(self, *args: tuple, **kwargs: StrDict) -> None:
        super().__init__(*args, **kwargs)
        self.inject("created", time())

# Aliases to the type signatures used in the event system
EventList = List[Event]
EventHandler = Callable[[Event], None]
#EventHandlers = Tuple[EventHandler, ...]

class EventStoreBackend(metaclass=ABCMeta):
    """
    Ensures event store backends all implemented required methods
    """

    @abstractmethod
    def save(self, events: EventList) -> None:
        """
        Save events to storage location of backend
        """

    @abstractmethod
    def apply(self, *handlers: EventHandler) -> None:
        """
        Iterate over saved events to apply event handlers
        """

class EventStore(object):
    """
    Wrapper for backends to save events and apply them to event handlers
    """

    def __init__(self, backend: EventStoreBackend) -> None:
        """
        Dynamically inherit attributes from backend
        """

        self._backend = backend

        # NOTE - I may remove this later if scope creep becomes and issue
        for attribute in dir(self._backend):
            # Will only inherit public attributes
            if attribute.startswith("_"):
                continue

            # These attributes are already handled 
            if attribute in ["save", "apply"]:
                continue

            # Inject the attribute from the backend to the event store
            setattr(self, attribute, getattr(self._backend, attribute))

    def save(self, events: EventList) -> None:
        """
        Pass list of events to backend to be saved
        """

        self._backend.save(events)

    def apply(self, *handlers: EventHandler) -> None:
        """
        Pass event handlers to iterated over saved events
        """

        self._backend.apply(*handlers)
