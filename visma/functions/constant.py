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

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self = Constant(self.calculate() * other.calculate())
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            for i, token in enumerate(other.tokens):
                if isinstance(token, Constant):
                    expression.tokens.append(Constant(self.calculate() * token.calculate()))
                elif isinstance(token, Variable):
                    variable = Variable()
                    variable.coefficient = self.calculate() * token.coefficient
                    variable.value.extend(token.value)
                    variable.power.extend(token.power)
                    expression.tokens.extend(['+', variable])
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            variable = Variable()
            variable.coefficient = self.calculate() * other.coefficient
            variable.value.extend(other.value)
            variable.power.extend(other.power)
            self.type = 'Variable'
            self = variable
            return variable

    def __rtruediv__(self, other):
        return self / other

    def __truediv__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self = Constant(self.calculate() / other.calculate())
            return self
        elif isinstance(other, Expression):
            expression = Expression(other.tokens)
            expression.coefficient = self.calculate()/other.coefficient
            expression.power = -1*other.power
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            variable = Variable(other)
            variable.coefficient = self.calculate() / other.coefficient
            variable.value.extend(other.value)
            variable.power.extend([other.power[0]*-1])
            self.type = 'Variable'
            self = variable
            return variable

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
