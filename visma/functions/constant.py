import math
from visma.functions.structure import Function, Expression
from visma.functions.variable import Variable

############
#   Constant #
############


class Constant(Function):
    """Class for constant type tokens

    Example:
        1, -2, 3.14, 4i + 5 etc

    Extends:
        Function
    """

    def __init__(self, value=None):
        super().__init__()
        self.coefficient = 1
        self.power = 1
        self.type = 'Constant'
        if value is not None:
            self.value = value

    def inverse(self, RHS):
        pass

    def differentiate(self):
        super().differentiate()
        self.value = 0

    def integrate(self, intwrt):
        self.coefficient = (self.value)**(self.power)
        self.__class__ = Variable
        self.power = [1]
        self.value = [intwrt]

    def calculate(self):
        return self.coefficient * ((self.value**(self.power)))

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self = Constant(self.calculate() + other.calculate())
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Constant):
                    self = Constant(self.calculate() + other.calculate())
                elif isinstance(token, Variable):
                    expression.tokens.extend(['+', Variable(token)])
            expression.tokens[0] = self
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend(['+', other])
            self.type = 'Expression'
            self = expression
            return expression

    def __rsub__(self, other):
        return self - other

    def __sub__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self = Constant(self.calculate() - other.calculate())
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Constant):
                    self = Constant(self.calculate() - other.calculate())
                elif isinstance(token, Variable):
                    expression.tokens.extend(['-', Variable(token)])
            expression.tokens[0] = self
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend(['-', other])
            self.type = 'Expression'
            self = expression
            return expression

    def functionOf(self):
        return []


class Zero(Constant):

    def __init__(self):
        super().__init__()
        self.value = 0


class One(Constant):

    def __init__(self):
        super().__init__()
        self.value = 1


class Pi(Constant):

    def __init__(self):
        super().__init__()
        self.value = math.pi


class Euler(Constant):

    def __init__(self):
        super().__init__()
        self.value = math.e


class Iota(Constant):

    def __init__(self):
        super().__init__()
        self.value = 1j
