"""
CPython 3.1 bytecode opcodes

This is used in scanner (bytecode disassembly) and parser (Python grammar).

This is a superset of Python 3.1's opcode.py with some opcodes that simplify
parsing and semantic interpretation.
"""

from copy import deepcopy

import xdis.opcodes.opcode_3x as opcode_3x
from xdis.opcodes.opcode_3x import findlabels, findlinestarts
from xdis.opcodes.opcode_3x import fields2copy, rm_op

# FIXME: can we DRY this even more?

opmap = {}
opname = [''] * 256
hasjrel = []
hasjabs = []

for object in fields2copy:
    globals()[object] =  deepcopy(getattr(opcode_3x, object))

def def_op(name, op):
    opname[op] = name
    opmap[name] = op

def_op('DUP_TOPX', 99)
def_op('EXTENDED_ARG', 143)
def_op('ROT_FOUR', 5)

# These are in Python 3.2 but not in Python 3.0
rm_op('DUP_TOP_TWO', 5, locals())

# There are no opcodes to add or change.
# If there were, they'd be listed below.

def updateGlobal():
    # JUMP_OPs are used in verification are set in the scanner
    # and used in the parser grammar
    globals().update({'PJIF': opmap['POP_JUMP_IF_FALSE']})
    globals().update({'PJIT': opmap['POP_JUMP_IF_TRUE']})
    globals().update(dict([(k.replace('+', '_'), v) for (k, v) in opmap.items()]))
    globals().update({'JUMP_OPs': map(lambda op: opname[op], hasjrel + hasjabs)})

updateGlobal()

from xdis import PYTHON_VERSION
if PYTHON_VERSION == 3.1:
    import dis
    for item in dis.opmap.items():
        if item not in opmap.items():
            print(item)
    assert all(item in opmap.items() for item in dis.opmap.items())

# opcode_3x.dump_opcodes(opmap)
