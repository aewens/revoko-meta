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
