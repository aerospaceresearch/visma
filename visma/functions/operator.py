# This classes is for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' propperties of 'Function' class


class Operator(object):

    def __init__(self, id, scope, value):
        self.id = ""
        self.scope = []
        self.value = None

    def set(self, id=None, scope=None, value=None):
        if id is not None:
            self.id = id
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value

    def level(self):
        return (int((len(self.id)) / 2))


class Binary(Operator):

    def __init__(self):
        super().__init__()

    def set(self):
        super().set()

    def level(self):
        super.level()


class Unary(Operator):

    def __init__(self):
        super().__init__()

    def set(self):
        super().set()

    def level(self):
        super.level()
