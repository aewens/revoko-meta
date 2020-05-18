from .context import meta

from sys import stderr
from unittest.mock import patch, call

def test_eprint():
    with patch("builtins.print") as mock_print:
        meta.eprint("ERROR")
        mock_print.assert_called_once_with("ERROR", file=stderr)
