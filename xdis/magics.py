import imp, struct, sys

def int2magic(magic):
    if (sys.version_info >= (3, 0)):
        return struct.pack('Hcc', magic, bytes('\r', 'utf-8'), bytes('\n', 'utf-8'))
    else:
        return struct.pack('Hcc', magic, '\r', '\n')

def magic2int(magic):
    return struct.unpack('Hcc', magic)[0]

PYTHON_MAGIC_INT = magic2int(imp.get_magic())

by_magic = {}
by_version = {}

def __by_version(magics):
    for m, v in list(magics.items()):
        by_magic[m] = v
        by_version[v] = m
    return by_version

versions = {
    # taken from from Python/import.c
    # or importlib/_bootstrap.py
    # magic, version
    int2magic(20121): '1.5', # 1.5, 1.5.1, 1.5.2
    int2magic(50428): '1.6', # 1.6
    int2magic(50823): '2.0', # 2.0, 2.0.1
    int2magic(60202): '2.1', # 2.1, 2.1.1, 2.1.2
    int2magic(60717): '2.2', # 2.2
    int2magic(62011): '2.3', # 2.3a0
    int2magic(62021): '2.3', # 2.3a0
    int2magic(62041): '2.4', # 2.4a0
    int2magic(62051): '2.4', # 2.4a3
    int2magic(62061): '2.4', # 2.4b1
    int2magic(62071): '2.5', # 2.5a0
    int2magic(62081): '2.5', # 2.5a0 (ast-branch)
    int2magic(62091): '2.5', # 2.5a0 (with)
    int2magic(62092): '2.5', # 2.5a0 (changed WITH_CLEANUP opcode)
    int2magic(62101): '2.5', # 2.5b3 (fix wrong code: for x, in ...)
    int2magic(62111): '2.5', # 2.5b3 (fix wrong code: x += yield)
    int2magic(62121): '2.5', # 2.5c1 (fix wrong lnotab with for loops and
                                 #  storing constants that should have been removed
    int2magic(62131): '2.5', # 2.5c2 (fix wrong code: for x, in ... in listcomp/genexp)
    int2magic(62151): '2.6', # 2.6a0 (peephole optimizations & STORE_MAP)
    int2magic(62161): '2.6', # 2.6a1 (WITH_CLEANUP optimization)
    int2magic(62171): '2.7', # 2.7a0 (optimize list comprehensions/change LIST_APPEND)
    int2magic(62181): '2.7', # 2.7a0 (optimize conditional branches:
                                 #  introduce POP_JUMP_IF_FALSE and POP_JUMP_IF_TRUE)
    int2magic(62191): '2.7', # 2.7a0 (introduce SETUP_WITH)
    int2magic(62201): '2.7', # 2.7a0 (introduce BUILD_SET)
    int2magic(62211): '2.7', # 2.7a0 (introduce MAP_ADD and SET_ADD)
    int2magic(62218): '2.7', # 2.7 pypy?
    int2magic(3000): '3.0',  # 3.000
    int2magic(3010): '3.0',  # 3.000 (removed UNARY_CONVERT)
    int2magic(3020): '3.0',  # 3.000 (added BUILD_SET)
    int2magic(3030): '3.0',  # 3.000 (added keyword-only parameters)
    int2magic(3040): '3.0',  # 3.000 (added signature annotations)
    int2magic(3050): '3.0',  # 3.000 (print becomes a function)
    int2magic(3060): '3.0',  # 3.000 (PEP 3115 metaclass syntax)
    int2magic(3061): '3.0',  # 3.000 (string literals become unicode)
    int2magic(3071): '3.0',  # 3.000 (PEP 3109 raise changes)
    int2magic(3081): '3.0',  # 3.000 (PEP 3137 make __file__ and __name__ unicode)
    int2magic(3091): '3.0',  # 3.000 (kill str8 interning)
    int2magic(3101): '3.0',  # 3.000 (merge from 2.6a0, see 62151)
    int2magic(3103): '3.0',  # 3.000 (__file__ points to source file)
    int2magic(3111): '3.0',  # 3.0a4 (WITH_CLEANUP optimization).
    int2magic(3131): '3.0',  # 3.0a5 (lexical exception stacking, including POP_EXCEPT)
    int2magic(3141): '3.1',  # 3.1a0 (optimize list, set and dict comprehensions)
    int2magic(3151): '3.1',  # 3.1a0 (optimize conditional branches)
    int2magic(3160): '3.2',  # 3.2a0 (add SETUP_WITH)
    int2magic(3170): '3.2',  # 3.2a1 (add DUP_TOP_TWO, remove DUP_TOPX and ROT_FOUR)
    int2magic(3180): '3.2',  # 3.2a2 (add DELETE_DEREF)
    int2magic(3190): '3.3',  # 3.3a0  3190 __class__ super closure changed
    int2magic(3200): '3.3',  # 3.3a0  3200 (__qualname__ added)
    int2magic(3210): '3.3',  # 3210 (added size modulo 2**32 to the pyc header)
    int2magic(3220): '3.3',  # 3.3a1  3220 (changed PEP 380 implementation)
    int2magic(3230): '3.3',  # 3.3a4  3230 (revert changes to implicit __class__ closure)
    int2magic(3250): '3.4',  # 3.4a1  3250 (evaluate positional default arg
                                 # keyword-only defaults)
    int2magic(3260): '3.4',  # 3.4a1  3260 (add LOAD_CLASSDEREF;
                                 # allow locals of class to override free vars)
    int2magic(3270): '3.4',  # 3.4a1  3270 (various tweaks to the __class__ closure)
    int2magic(3280): '3.4',  # 3.4a1  3280 (remove implicit class argument)
    int2magic(3290): '3.4',  # 3.4a4  3290 (changes to __qualname__ computation)
    int2magic(3300): '3.4',  # 3.4a4  3300 (more changes to __qualname__ computation)
    int2magic(3310): '3.4',  # 3.4rc2 3310 (alter __qualname__ computation)
    int2magic(3350): '3.5',  # 3.5.0
    int2magic(3361): '3.6',  # 3.6.0a1
    int2magic(3370): '3.6',  # 3.6
}

magics = __by_version(versions)

def __show(text, magic):
    print(text, struct.unpack('BBBB', magic), struct.unpack('HBB', magic))

def test():
    magic_20 = magics['2.0']
    current = imp.get_magic()
    magic_current = by_magic[ current ]
    print(type(magic_20), len(magic_20), repr(magic_20))
    print()
    print('This Python interpreter has version', magic_current)
    print('Magic code: ', PYTHON_MAGIC_INT)
    print(type(magic_20), len(magic_20), repr(magic_20))

if __name__ == '__main__':
    test()
