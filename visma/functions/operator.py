class Operator(object):
    """The Operator class is for operators(+, -, *, / etc)

    Example:
        '+', '-', '*' etc

    Note:
        Not to be confused with 'operator' and 'operand' properties of 'Function' class
    """

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None

    def __str__(self):
        represent = ""
        represent += str(self.value)
        return represent

    def differentiate(self):
        return self


class Binary(Operator):
    """Binary operator takes two operands

    Example:
        '2 + 2', '5/6' etc

    Extends:
        Operator
    """

    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.value = value


class Sqrt(Operator):

    def __init__(self, power=None, operand=None):
        super().__init__()
        if power is not None:
            self.power = power
        if operand is not None:
            self.operand = operand

    def __str__(self):
        represent = ""
        if self.operand.value == -1:
            represent += r"\iota "
        else:
            represent += r"\sqrt" + self.operand.__str__()
        return represent


class Plus(Binary):
    """Class for '+'

    Extends:
        Binary
    """

    def __init__(self):
        super().__init__()
        self.value = '+'


class Minus(Binary):
    """Class for '-'

    Extends:
        Binary
    """

    def __init__(self):
        super().__init__()
        self.value = '-'


class Multiply(Binary):
    """Class for '*'

    Extends:
        Binary
    """

    def __init__(self):
        super().__init__()
        self.value = '*'


class Divide(Binary):
    """Class for '/'

    Extends:
        Binary
    """

    def __init__(self):
        super().__init__()
        self.value = '/'


class EqualTo(Binary):
    """Class for '='

    Extends:
        Binary
    """

    def __init__(self):
        super().__init__()
        self.value = '='
