
def use(path: str):
    from importlib import import_module
    return import_module(path)

def tostr(tree: str):
    from lark import Tree
    if isinstance(tree, Tree):
        return '(' + ' '.join(map(tostr, tree.children)) + ')'
    else:
        return str(tree)

def get(ret, *parts):
    for part in parts:
        if hasattr(ret, part):
            ret = getattr(ret, part)
        else:
            ret = ret[part]
    return ret

def do(*args):
    return args[-1]

def lt(x, y):
    return x < y

def add(*args):
    ret = 0
    for arg in args:
        ret += arg
    return ret

def sub(*args):
    if len(args) == 1:
        return -args[0]
    ret = args[0]
    for arg in args[1:]:
        ret -= arg
    return ret

def mul(*args):
    ret = 1
    for arg in args:
        ret *= arg
    return ret

def div(*args):
    if len(args) == 1:
        return 0-args[0]
    ret = args[0]
    for arg in args[1:]:
        ret //= arg
    return ret

def call(*args):
    from lark import Token, Tree
    assert all(isinstance(arg, (Tree, Token)) for arg in args)
    return Tree('call', args)

def num(n):
    from lark import Token
    assert isinstance(n, int)
    return Token('NUM', str(n))

def name(text):
    from lark import Token
    assert isinstance(text, str)
    return Token('NAME', text)
