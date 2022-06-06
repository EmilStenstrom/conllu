import contextlib
import doctest
import os
import re
import tempfile
from doctest import OutputChecker
from pathlib import Path
from unittest import mock


class ReadmeOutputChecker(OutputChecker):
    def check_output(self, want, got, optionflags):
        # Allow dicts and lists to be formatted with whitespace around brackets
        if want.startswith("{") or want.startswith("["):
            want = re.sub(r"\s*([\{\[\]\}])\s*", r"\1", want, flags=re.MULTILINE)
            got = re.sub(r"\s*([\{\[\]\}])\s*", r"\1", got, flags=re.MULTILINE)

        return OutputChecker.check_output(self, want, got, optionflags)

@contextlib.contextmanager
def temporary_chdir():
    try:
        old = os.getcwd()
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            yield
    finally:
        os.chdir(old)

def test_readme():
    readme_file = Path("README.md")

    # Copy contents of README, to remove ``` and run all code in one session
    readme_data = ""
    with open(readme_file, "r") as f:
        for line in f:
            if line == "```\n":
                readme_data += "\n"
            else:
                readme_data += line

    with temporary_chdir():
        with mock.patch('doctest.OutputChecker', ReadmeOutputChecker):
            doctest.run_docstring_examples(
                readme_data,
                globs={},
                name=readme_file.name,
                optionflags=(
                    doctest.ELLIPSIS
                    | doctest.NORMALIZE_WHITESPACE
                    | doctest.FAIL_FAST
                    | doctest.REPORT_NDIFF
                ),
            )
