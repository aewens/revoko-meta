from meta import eprint
from meta.external.json.types import JSONType
from meta.external.json.encode import jsto, jots

from pathlib import Path
from typing import Optional

class JSONMetadata(object):
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def read(self, verbose: bool=False) -> Optional[JSONType]:
        if not self._path.exists():
            return None

        contents = self._path.read_text()
        return jsto(contents, verbose)

    def write(self, data: JSONType, verbose: bool=False) -> bool:
        encoded = jots(data, readable=True, verbose=verbose)
        if encoded is None:
            return False

        self._path.write_text(encoded)
        return True
