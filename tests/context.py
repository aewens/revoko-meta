import sys
from pathlib import Path

import_path = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(import_path))

import meta
import meta.creating as creating
