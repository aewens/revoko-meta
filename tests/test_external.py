from .context import external
from pathlib import Path

def test_jsto():
    assert external.jsto("{\"a\": 1}") == {"a": 1}
    try: 
        external.jsto(None)

    except TypeError as e:
        assert True

    else:
        assert False

def test_jots():
    assert external.jots({"a": 1}) == "{\"a\": 1}"
    assert external.jots([1, 2, 3]) == "[1, 2, 3]"
    assert external.jots({"a": 1}, readable=True) == "{\n    \"a\": 1\n}"
    assert external.jots([1, 2, 3], readable=True) == """
        [\n    1, \n    2, \n    3\n]
    """.strip()
    assert external.jots(None) == "null"
    try: 
        external.jsto(lambda x: x + 1)

    except TypeError as e:
        assert True

    else:
        assert False

def test_json_metadata():
    here = Path(__file__)
    test_file = "test_metadata"
    test_path = here.parent / test_file
    test_data = external.jsto(test_path.read_text())

    jm = external.JSONMetadata(f"/tmp/{test_file}")
    wrote = jm.write(test_data)
    assert wrote is True

    read = jm.read()
    assert read is not None
