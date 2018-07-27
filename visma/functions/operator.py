# These classes are for operators (+, -, *, / etc)
# Not to be confused with 'operator' and 'operand' properties of 'Function' class


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


class Binary(Operator):
    """Class for binary operator
    """

    def __init__(self, value=None):
        super().__init__()
        self.type = 'Binary'
        if value is not None:
            self.value = value


class Sqrt(Operator):
    """Class for sqrt operator
    """

    def __init__(self):
        super().__init__()
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
        super().__init__()
        self.value = '+'


class Minus(Binary):

    def __init__(self):
        super().__init__()
        self.value = '-'


class Multiply(Binary):

    def __init__(self):
        super().__init__()
        self.value = '*'


class Divide(Binary):

    def __init__(self):
        super().__init__()
        self.value = '/'


class EqualTo(Binary):

    def __init__(self):
        super().__init__()
        self.value = '='
