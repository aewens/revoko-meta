from .context import arch

from time import time
from uuid import UUID

def raises(test_case, exception):
    try:
        test_case()

    except exception as e:
        return True

    else:
        return False

def test_vobject():
    class TestNamespace(arch.Namespace):
        test: bool

    tn1 = lambda: TestNamespace(True)
    assert not raises(tn1, Exception)

    tn2 = lambda: TestNamespace()
    assert raises(tn2, arch.LogicError)

    tn = TestNamespace(True)
    assert repr(tn) == "<TestNamespace(test=True)>"
    assert tn._resolve_arguments(False) == {"test": False}

    injected = lambda: tn.inject("key", "value")
    assert not raises(injected, Exception)
    assert tn.key == "value"

    class TestVObject(arch.VObject):
        attr1: str
        attr2: int

    tvo1 = lambda: TestVObject("a", 1)
    assert not raises(tvo1, Exception)

    tvo2 = lambda: TestVObject("a", 1, 2)
    assert raises(tvo2, arch.LogicError) 

    tvo3 = lambda: TestVObject("a")
    assert raises(tvo3, arch.LogicError)

    tvoa = TestVObject("a", 1)
    tvob = TestVObject("a", 1)
    tvoc = TestVObject("c", 1)
    tvod = TestVObject("c", 2)

    assert tvoa == tvob
    assert tvob != tvoc
    assert tvoc != tvod

    class AnotherVObject(arch.VObject):
        attr1: str

    avo = AnotherVObject("a")

    assert tvoa != avo

    tvo = TestVObject("z", -1)

    assert tvo.__attrs__ == ("attr1", "attr2")
    assert hasattr(tvo, "attr1")
    assert hasattr(tvo, "attr2")

    at1 = lambda: setattr(tvo, "attr1", "y")
    assert raises(at1, AttributeError)

    at2 = lambda: setattr(tvo, "attr2", 0)
    assert raises(at2, AttributeError)

def test_entity():
    class TestEntity(arch.Entity):
        attr1: str
        attr2: int

    tel = lambda: TestEntity("a", 1)
    assert not raises(tel, Exception)

    te = tel()
    assert isinstance(te, arch.VObject)
    assert hasattr(te, "uuid")

    nte = lambda: setattr(te, "uuid", None)
    assert raises(nte, AttributeError)

def test_event_store():
    # NOTES
    # arch.EventList == typing.List[arch.Event]
    # arch.EventHandler == typing.Callable[[arch.Event], None]
    # arch.EventHandlers == typing.Tuple[arch.EventHandler, ...]

    class TestInvalidEventStoreBackend(arch.EventStoreBackend):
        """
        Will fail, does not implement save and apply
        """
        pass

    invalid_backend = lambda: TestInvalidEventStoreBackend()
    assert raises(invalid_backend, TypeError)

    class TestEventStoreBackend(arch.EventStoreBackend):
        """
        Stand in for a "real" backend that would read/write to file or database
        While it does not persist data, it is good enough for testing here
        """

        # This is not required and is used purely for testing purposes
        _events: arch.EventList

        def __init__(self):
            super().__init__()

            # This is not required and is used purely for testing purposes
            self._events = list()

        def save(self, events: arch.EventList) -> None:
            """
            A "real" implementation would write to file or database here
            """

            self._events.extend(events)

        def apply(self, *handlers: arch.EventHandler) -> None:
            """
            A "real" implementation would read from file or database here
            """

            for event in self._events:
                print(f"Handlers: {len(handlers)}")
                for handler in handlers:
                    print(handler)
                    print(event)
                    print()
                    handler(event)

            print("END")

        @property
        def events(self):
            """
            This is not required and is used purely for testing purposes
            """
            return self._events

    class TestEntity(arch.Entity):
        attr1: str
        attr2: int

    class TestEvent(arch.Event):
        entity: TestEntity
        data1: str
        data2: int

    def test_event_handler1(events: arch.EventList) -> arch.EventHandler:
        def event_handler(event: arch.Event) -> None:
            events.append(event)
            
        return event_handler

    def test_event_handler2(events: arch.EventList) -> arch.EventHandler:
        def event_handler(event: arch.Event) -> None:
            events.append(event)
            
        return event_handler

    backend = TestEventStoreBackend()
    store = arch.EventStore(backend)

    # Generate test data
    attr1s = ["a", "b", "c"]
    attr2s = [1, 2, 3]
    test_entities = [TestEntity(a1, a2) for a1, a2 in zip(attr1s, attr2s)]

    data1s = ["x", "y", "z"]
    data2s = [10, 20, 30]
    test_events = [[TestEvent(entity, data1=d1, data2=d2)
        for d1, d2 in zip(data1s, data2s)] for entity in test_entities]

    for e, entity in enumerate(test_entities):
        assert test_entities[e].attr1 == attr1s[e]
        assert test_entities[e].attr2 == attr2s[e]

        events = list()
        entity_uuid = entity.uuid
        for ee, event in enumerate(test_events[e]):
            assert hasattr(event, "uuid")
            assert isinstance(event.uuid, UUID)

            assert hasattr(event, "entity")
            assert event.entity.uuid == entity_uuid

            assert hasattr(event, "data1")
            assert event.data1 == data1s[ee]

            assert hasattr(event, "data2")
            assert event.data2 == data2s[ee]

            assert hasattr(event, "created")
            assert isinstance(event.created, float)
            assert event.created > 0
            assert event.created < time()

            events.append(event)

        saved = lambda: store.save(events)
        assert not raises(saved, Exception)

    handled_events1 = list()
    handler1 = test_event_handler1(handled_events1)

    applied1 = lambda: store.apply(handler1)
    assert not raises(applied1, Exception)
    assert len(handled_events1) > 0
    assert handled_events1 == store.events

    # Reset to test again using two handlers
    handled_events1 = list()
    handler1 = test_event_handler1(handled_events1)

    handled_events2 = list()
    handler2 = test_event_handler2(handled_events2)

    applied2 = lambda: store.apply(handler1, handler2)
    assert not raises(applied2, Exception)
    assert len(handled_events1) > 0
    assert len(handled_events2) > 0
    assert handled_events1 == handled_events2
    assert handled_events1 == store.events
