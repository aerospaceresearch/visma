# This classes is for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' propperties of 'Function' class


class Operator(object):

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None
        self.type = None

    def __str__(self):
        represent = ""
        represent += str(self.value)
        return represent

    def level(self):
        return (int((len(self.tid)) / 2))

    def functionOf(self):
        return None


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

    def __str__(self):
        represent = ""
        if self.expression.value == -1:
            represent += "\iota "
        else:
            represent += "{" + self.expression.__str__() + "}"
        return represent
