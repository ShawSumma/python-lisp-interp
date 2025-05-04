
class Call:
    __slots__ = ('args',)

    def __init__(self, args):
        self.args = args

class Value:
    __slots__ = ('value',)

    def __init__(self, value):
        self.value = value
