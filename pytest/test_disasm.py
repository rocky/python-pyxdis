import os
import pytest
import re

from xdis.main import disassemble_file
from xdis import PYTHON3, PYTHON_VERSION

if PYTHON3:
    from io import StringIO

    hextring_file = "testdata/01_hexstring-2.7-for3x.right"
else:
    from StringIO import StringIO

    hextring_file = "testdata/01_hexstring-2.7.right"


def get_srcdir():
    filename = os.path.normcase(os.path.dirname(__file__))
    return os.path.realpath(filename)


if PYTHON_VERSION >= 3.2:
    @pytest.mark.parametrize(
        ("test_tuple", "function_to_test"),
        [
            (
                ("../test/bytecode_3.6/01_fstring.pyc", "testdata/fstring-3.6.right"),
                disassemble_file,
            ),
            (
                ("../test/bytecode_3.0/04_raise.pyc", "testdata/raise-3.0.right"),
                disassemble_file,
            ),
            (
                (
                    "../test/bytecode_2.7pypy/04_pypy_lambda.pyc",
                    "testdata/pypy_lambda.right",
                ),
                disassemble_file,
            ),
            (
                ("../test/bytecode_3.6/03_big_dict.pyc", "testdata/big_dict-3.6.right"),
                disassemble_file,
            ),
            (("../test/bytecode_2.7/01_hexstring.pyc", hextring_file), disassemble_file),
        ],
    )
    def test_funcoutput(capfd, test_tuple, function_to_test):
        in_file, filename_expected = [os.path.join(get_srcdir(), p) for p in test_tuple]
        resout = StringIO()
        function_to_test(in_file, resout)
        expected = "".join(open(filename_expected, "r").readlines())
        got_lines = resout.getvalue().split("\n")
        got_lines = [
            re.sub(" at 0x[0-9a-f]+", " at 0xdeadbeef0000", line) for line in got_lines
        ]
        got_lines = [
            re.sub(
                "<code object .*>|<xdis.code.Code[23] (object|instance) .*>",
                "<xdis.code.thingy instance at 0xdeadbeef0000>",
                line,
            )
            for line in got_lines
        ]
        got = "\n".join(got_lines[5:])

        if "XDIS_DONT_WRITE_DOT_GOT_FILES" not in os.environ:
            if got != expected:
                with open(filename_expected + ".got", "w") as out:
                    out.write(got)
        assert got == expected

    @pytest.mark.parametrize(
        ("obfuscated_bytecode_file", "expected_variable_name"),
        [
            ("../test/bytecode_3.7/02_invalid_variable_name1.pyc", "y____Hello___"),
            ("../test/bytecode_3.7/02_invalid_variable_name2.pyc", "_for"),
            ("../test/bytecode_3.7/02_invalid_variable_name3.pyc", "_x"),
        ],
    )
    def test_obfuscation(obfuscated_bytecode_file, expected_variable_name):
        INVALID_VARS_ERROR_MSG = "# WARNING: Code contains variables with invalid Python variable names."
        testfile = os.path.join(get_srcdir(), obfuscated_bytecode_file)
        resout = StringIO()
        disassemble_file(testfile, resout, header=True, warn_invalid_vars=True)
        assert INVALID_VARS_ERROR_MSG in resout.getvalue(), "Warning about invalid variables not found when disassembling %s" % obfuscated_bytecode_file

        resout = StringIO()
        disassemble_file(testfile, resout, warn_invalid_vars=False, fix_invalid_vars=True)
        assert expected_variable_name in resout.getvalue(), "Expected obfuscated variable in testfile %s to be repaired to %s" % (obfuscated_bytecode_file, expected_variable_name)
