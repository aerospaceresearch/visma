# This classes is for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' propperties of 'Function' class


class Operator(object):

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None
        self.type = None

    def level(self):
        return (int((len(self.tid)) / 2))


class Binary(Operator):
    """Class for binary operator
    """

    def __init__(self):
        super(Binary, self).__init__()
        self.type = 'Binary'


class Unary(Operator):
    """Class for unary operator
    """

    def __init__(self):
        super(Unary, self).__init__()
        self.type = 'Unary'


class Sqrt(Operator):
    """Class for sqrt operator
    """

    def __init__(self):
        super(Sqrt, self).__init__()
        self.power = None
        self.expression = None
        self.type = 'Sqrt'
