

from typing import TypeAlias, Union

class Call:
    __slots__ = ('args',)

    def __init__(self, args: list['Expr']) -> None:
        self.args = args

    def __str__(self) -> str:
        return ' '.join(map(str, self.args))

class Number:
    value: int

    __slots__ = ('value',)

    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
Expr: TypeAlias = Union[Call, Number]
Value: TypeAlias = Union[Expr]
