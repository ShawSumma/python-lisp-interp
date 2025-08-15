
from lark import Lark, Token, Tree
from functools import cache
import src.core as core
from collections.abc import Sequence

Bindings = tuple[dict[str, object], list[str]]
AST = Tree | Token

parser = Lark.open("src/lisp.lark", rel_to = __file__)

class Macro:
    def __init__(self, params, body, then):
        self.params = params
        self.body = body
        self.then = then

    @cache
    def __call__(self, env: 'Env', *args: object):
        old = env.bind(self.params, args)

        for thing in self.body:
            env.visit(thing)

        body = env.visit(self.then)

        env.unbind(old)

        return body

class Env:
    scope: dict[str, object]

    def __init__(self) -> None:
        self.scope = {}

    def bind(self, params: Sequence[str], args: Sequence[object]) -> Bindings:
        old: dict[str, object] = {}
        dels: list[str] = []
        for arg, param in zip(args, params):
            if param in self.scope:
                old[param] = self.scope[param]
            else:
                dels.append(param)
            self.scope[param] = arg
        return old, dels

    def unbind(self, args: Bindings):
        old, dels = args
        for key, value in old.items():
            self.scope[key] = value
        for name in dels:
            del self.scope[name]

    def visit(self, tree: AST | str):
        if isinstance(tree, Tree):
            children = tree.children
            match tree.data:
                case 'start':
                    for child in children:
                        res = self.visit(child)
                        if res is not None:
                            print(res)
                    return
                case 'call':
                    if isinstance(children[0], Token):
                        match str(children[0]):
                            case 'macro':
                                params = [str(param) for param in children[1].children]

                                return Macro(params, children[2:-1], children[-1])
                            case 'define':
                                self.scope[str(children[1])] = self.visit(children[2])
                                return
                            case 'if':
                                if self.visit(children[1]):
                                    return self.visit(children[2])
                                else:
                                    return self.visit(children[3])
                            case 'lambda':
                                params = [str(param) for param in children[1].children]
                                
                                def lambda_func(*args):
                                    old = self.bind(params, args)
                                    for child in children[2:-1]:
                                        self.visit(child)
                                    ret = self.visit(children[-1])
                                    self.unbind(old)
                                    return ret
                                
                                return lambda_func
                    
                    func = self.visit(children[0])
                    if isinstance(func, Macro):
                        return self.visit(func(*children[1:]))
                    args = [self.visit(child) for child in children[1:]]
                    return func(*args)
        else:
            match tree.type:
                case 'STR':
                    return tree[1:-1]
                case 'NUM':
                    return int(tree)
                case 'NAME':
                    name, *dot = str(tree).split('.')
                    if name == '':
                        def inner_name(obj):
                            for part in dot:
                                if hasattr(obj, part):
                                    obj = getattr(obj, part)
                                else:
                                    obj = obj[part]
                            return obj
                        return inner_name
                    if name in self.scope:
                        ret = self.scope[name]
                    else:
                        ret = getattr(core, name)
                    return core.get(ret, *dot)
        raise NotImplementedError(str(tree))

