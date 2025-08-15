
from src.lisp import Env
from sys import argv

def main():
    match argv:
        case [file, *args]:
            env = Env()
            with open(argv[1]) as f:
                ast = lisp.parser.parse(f.read())
            context = Lisp()
            lisp.bind()
            lisp.visit(ast)

if __name__ == '__main__':
    main()

