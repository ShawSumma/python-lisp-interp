
from lark import Lark, Token, Tree
from sys import argv
from functools import cache
import core

parser = Lark.open("lisp.lark")

scope = {}

class Macro:
    def __init__(self, params, then):
        self.params = params
        self.then = then

    @cache
    def __call__(self, *args):
        old = bind(self.params, args)

        body = visit(self.then)

        unbind(old)

        return body

def bind(params, args):
    old = {}
    dels = []
    for arg, param in zip(args, params):
        if param in scope:
            old[param] = scope[param]
        else:
            dels.append(param)
        scope[param] = arg
    return old, dels

def unbind(args):
    old, dels = args
    for key, value in old.items():
        scope[key] = value
    for name in dels:
        del scope[name]

def visit(tree):
    if isinstance(tree, Tree):
        children = tree.children
        match tree.data:
            case 'start':
                for child in children:
                    res = visit(child)
                    if res is not None:
                        print(res)
                return
            case 'call':
                if isinstance(children[0], Token):
                    match str(children[0]):
                        case 'macro':
                            params = [str(param) for param in children[1].children]

                            return Macro(params, children[2])
                        case 'define':
                            scope[str(children[1])] = visit(children[2])
                            return
                        case 'if':
                            if visit(children[1]):
                                return visit(children[2])
                            else:
                                return visit(children[3])
                        case 'lambda':
                            params = [str(param) for param in children[1].children]
                            
                            def func(*args):
                                old = bind(params, args)
                                for child in children[2:-1]:
                                    visit(child)
                                ret = visit(children[-1])
                                unbind(old)
                                return ret
                            
                            return func
                func = visit(children[0])
                if isinstance(func, Macro):
                    return visit(func(*children[1:]))
                data = [visit(child) for child in children[1:]]
                return func(*data)
    else:
        match tree.type:
            case 'STR':
                return tree[1:-1]
            case 'NUM':
                return int(tree)
            case 'NAME':
                name = str(tree)
                if tree in scope:
                    return scope[name]
                return getattr(core, name) 
    raise NotImplementedError(str(tree))

def main():
    with open(argv[1]) as f:
        ast = parser.parse(f.read())

    visit(ast)

if __name__ == '__main__':
    main()
