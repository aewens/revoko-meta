from .context import arch
from typing import NamedTuple

def raises(test_case, exception):
    try:
        test_case()

    except exception as e:
        return True

    else:
        return False

def test_vobject():
    class TestVObject(arch.VObject):
        attr1: str
        attr2: int

    tvo1 = lambda: TestVObject("a", 1)
    assert not raises(tvo1, arch.LogicError)

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

def test_entity():
    class TestEntity(arch.Entity):
        attr1: str
        attr2: int

    tel = lambda: TestEntity("a", 1)
    assert not raises(tel, arch.LogicError)

    te = tel()
    assert isinstance(te, arch.VObject)
    assert hasattr(te, "uuid")

    nte = lambda: setattr(te, "uuid", None)
    assert raises(nte, AttributeError)
