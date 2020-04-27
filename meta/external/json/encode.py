from meta.external.json.types import JSONType

from typing import Optional
from json import loads as json_loads, dumps as json_dumps

def jsto(data: str, verbose: bool=False) -> Optional[JSONType]:
    try:
        return json_loads(data)

    except ValueError as e:
        if verbose:
            eprint(e)

    return None

def jots(data: JSONType, readable: bool=False,
    verbose: bool=False) -> Optional[str]:
    kwargs = dict()

    # If readable is set, it pretty prints the JSON to be more human-readable
    if readable:
        # kwargs["sort_keys"] = True
        kwargs["indent"] = 4 
        kwargs["separators"] = (", ", ": ")

    try:
        return json_dumps(data, **kwargs)

    except Exception as e:
        if verbose:
            eprint(e)

    return None
