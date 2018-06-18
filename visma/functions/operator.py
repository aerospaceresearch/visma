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
        self.operand = None
        self.type = 'sqrt'

    def __str__(self):
        represent = ""
        if self.operand.value == -1:
            represent += "\iota "
        else:
            represent += "\sqrt" + self.operand.__str__()
        return represent


class Plus(Binary):

    def __init__(self):
        super(Plus, self).__init__()
        self.value = '+'


class Minus(Binary):

    def __init__(self):
        super(Minus, self).__init__()
        self.value = '-'


class Multiply(Binary):

    def __init__(self):
        super(Multiply, self).__init__()
        self.value = '*'


class Divide(Binary):

    def __init__(self):
        super(Divide, self).__init__()
        self.value = '/'
