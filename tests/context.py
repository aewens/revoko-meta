import sys
from pathlib import Path

import_path = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(import_path))

import meta
import meta.domain as domain
import meta.service as service
import meta.infrastructure as infrastructure
import meta.external as external
