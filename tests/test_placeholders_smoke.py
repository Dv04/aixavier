from subprocess import run
import sys


def test_placeholders_resolved():
    result = run([sys.executable, "tools/placeholder_lint.py"])
    assert (
        result.returncode == 0
    ), "Unresolved placeholders or secret hygiene errors detected"
