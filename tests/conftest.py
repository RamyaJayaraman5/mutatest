"""Test suite large and shared fixtures.
"""
import ast
import contextlib
import sys

from io import StringIO
from pathlib import Path
from textwrap import dedent
from typing import NamedTuple

import pytest

from mutatest.maker import LocIndex


class FileAndTest(NamedTuple):
    """Container for paired file and test location in tmp_path_factory fixtures."""

    src_file: Path
    test_file: Path


@pytest.fixture(scope="session")
def binop_file(tmp_path_factory):
    """A simple python file with binary operations."""
    contents = dedent(
        """\
    def myfunc(a):
        print("hello", a)


    def add_ten(b):
        return b + 11 - 1


    def add_five(b):
        return b + 5


    def add_five_divide_3(b):
        x = add_five(b)
        return x / 3

    print(add_five(5))
    """
    )

    fn = tmp_path_factory.mktemp("binops") / "binops.py"

    with open(fn, "w") as output_fn:
        output_fn.write(contents)

    return fn


@pytest.fixture(scope="session")
def binop_expected_locs():
    """Expected target locations for the binop_file fixture."""
    return {
        LocIndex(ast_class="BinOp", lineno=6, col_offset=11, op_type=ast.Add),
        LocIndex(ast_class="BinOp", lineno=6, col_offset=18, op_type=ast.Sub),
        LocIndex(ast_class="BinOp", lineno=10, col_offset=11, op_type=ast.Add),
        LocIndex(ast_class="BinOp", lineno=15, col_offset=11, op_type=ast.Div),
    }


@pytest.fixture(scope="session")
def single_binop_file_with_good_test(tmp_path_factory):
    """Single binop file and test file where mutants will be detected."""
    contents = dedent(
        """\
    def add_five(b):
        return b + 5

    print(add_five(5))
    """
    )

    test_good = dedent(
        """\
    from single import add_five

    def test_add_five():
        assert add_five(5) == 10
    """
    )

    folder = tmp_path_factory.mktemp("single_binops_good")
    fn = folder / "single.py"
    good_test_fn = folder / "test_good_single.py"

    for f, c in [(fn, contents), (good_test_fn, test_good)]:
        with open(f, "w") as output_fn:
            output_fn.write(c)

    return FileAndTest(fn, good_test_fn)


@pytest.fixture(scope="session")
def single_binop_file_with_bad_test(tmp_path_factory):
    """Single binop file and test file where mutants will survive."""
    contents = dedent(
        """\
    def add_five(b):
        return b + 5

    print(add_five(5))
    """
    )

    test_bad = dedent(
        """\
    from single import add_five

    def test_add_five():
        assert True
    """
    )

    folder = tmp_path_factory.mktemp("single_binops_bad")
    fn = folder / "single.py"
    bad_test_fn = folder / "test_single_bad.py"

    for f, c in [(fn, contents), (bad_test_fn, test_bad)]:
        with open(f, "w") as output_fn:
            output_fn.write(c)

    return FileAndTest(fn, bad_test_fn)


@pytest.fixture(scope="session")
def stdoutIO():
    """Stdout redirection as a context manager to evaluating code mutations."""

    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    return stdoutIO