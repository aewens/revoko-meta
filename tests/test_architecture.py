from .context import arch
from typing import NamedTuple

def test_entity():
    class TestEntity(arch.Entity):
        attr1: str
        attr2: int

    try:
        te1 = TestEntity("a", 1)

    except arch.LogicError as e:
        assert False

    else:
        assert True

    try:
        te2 = TestEntity("a", 1, 2)

    except arch.LogicError as e:
        assert True

    else:
        assert False

    try:
        te3 = TestEntity("a")

    except arch.LogicError as e:
        assert True

    else:
        assert False

def test_prototype_with():
    class TestType(NamedTuple):
        attr1: str    
        attr2: int

    @arch.prototype_with(TestType)
    class TestEntity(arch.Entity):
        pass

    try:
        te1 = TestEntity("a", 1)

    except arch.LogicError as e:
        assert False

    else:
        assert True

    try:
        te2 = TestEntity("a", 1, 2)

    except arch.LogicError as e:
        assert True

    else:
        assert False

    try:
        te3 = TestEntity("a")

    except arch.LogicError as e:
        assert True

    else:
        assert False
