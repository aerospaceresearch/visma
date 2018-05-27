# This classes is for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' propperties of 'Function' class


class Operator(object):

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None

    def set(self, scope=None, value=None, tid=None):
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value
        if tid is not None:
            self.tid = tid

    def level(self):
        return (int((len(self.tid)) / 2))


class Binary(Operator):

    def __init__(self):
        super(Binary, self).__init__()

    def set(self, scope=None, value=None, tid=None):
        super(Binary, self).set(scope, value, tid)

    def level(self):
        super(Binary, self).level()


class Unary(Operator):

    def __init__(self):
        super(Unary, self).__init__()

    def set(self, scope=None, value=None, tid=None):
        super(Unary, self).set(scope, value, tid)

    def level(self):
        super(Unary, self).level()
