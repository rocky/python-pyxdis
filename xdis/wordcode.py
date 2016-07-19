"""Python disassembly functions specific to wordcode from python 3.6
Extracted from
"""

def _unpack_opargs(code, opc):
    # enumerate() is not an option, since we sometimes process
    # multiple elements on a single pass through the loop
    extended_arg = 0
    n = len(code)
    i = 0
    while i < n:
        op = code[i]
        offset = i
        i += 1
        arg = None
        if op >= opc.HAVE_ARGUMENT:
            arg = code[i] + code[i+1]*256 + extended_arg
            extended_arg = 0
            i += 2
            if op == opc.EXTENDED_ARG:
                extended_arg = arg*65536
        yield (offset, op, arg)


def _findlinestarts(code):
    """Find the offsets in a byte code which are start of lines in the source.

    Generate pairs (offset, lineno) as described in Python/compile.c.

    """
    byte_increments = code.co_lnotab[0::2]
    line_increments = code.co_lnotab[1::2]

    lastlineno = None
    lineno = code.co_firstlineno
    addr = 0
    for byte_incr, line_incr in zip(byte_increments, line_increments):
        if byte_incr:
            if lineno != lastlineno:
                yield (addr, lineno)
                lastlineno = lineno
            addr += byte_incr
        if line_incr >= 0x80:
            # line_increments is an array of 8-bit signed integers
            line_incr -= 0x100
        lineno += line_incr
    if lineno != lastlineno:
        yield (addr, lineno)


def _findlabels(code, opc):
    """Detect all offsets in a byte code which are jump targets.

    Return the list of offsets.

    """
    labels = []
    for offset, op, arg in _unpack_opargs(code, opc):
        if arg is not None:
            label = -1
            if op in opc.hasjrel:
                label = offset + 3 + arg
            elif op in opc.hasjabs:
                label = arg
            if label >= 0:
                if label not in labels:
                    labels.append(label)
    return labels
