# This classes is for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' propperties of 'Function' class


class Operator(object):

    def __init__(self, tid, scope, value):
        self.tid = ""
        self.scope = []
        self.value = None

    def setprop(self, tid=None, scope=None, value=None):
        if tid is not None:
            self.tid = tid
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value

    def level(self):
        return (int((len(self.tid)) / 2))


class Binary(Operator):

    def __init__(self):
        super().__init__()

    def setprop(self):
        super().setprop(args)

    def level(self):
        super.level()


class Unary(Operator):

    def __init__(self):
        super().__init__()

    def setprop(self):
        super().setprop(args)

    def level(self):
        super.level()
