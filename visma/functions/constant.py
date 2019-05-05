import math
from visma.functions.structure import Function, Expression
from visma.functions.variable import Variable
from visma.functions.exponential import Exponential

#############
# Constant  #
#############


class Constant(Function):
    """Class for constant type tokens

    Example:
        1, -2, 3.14, 4i + 5 etc

    Extends:
        Function
    """

    def __init__(self, value=None, power=1, coefficient=1):
        super().__init__()
        self.coefficient = coefficient
        self.power = power
        self.type = 'Constant'
        if value is not None:
            self.value = value
        if self.value is not None:
            self.value = self.calculate()
            self.coefficient = 1
            self.power = 1

    def inverse(self, RHS):
        pass

    def differentiate(self):
        super().differentiate()
        self.value = 0

    def integrate(self, intwrt):
        self.coefficient = self.value ** self.power
        self.__class__ = Variable
        self.power = [1]
        self.value = [intwrt]

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        if self.isZero():   # if one of them is Empty, we can return the other one even it is Empty too because we need at least one to be returned.
            return other
        elif other.isZero():
            return self
        elif isinstance(other, Constant):
            const = Constant()
            const.value = self.calculate() + other.calculate()
            return const
        elif isinstance(other, Expression):
            if other.power == 1:
                constFound = False
                for i, var in enumerate(other.tokens):
                    if isinstance(var, Constant):
                        other.tokens[i] = self + var
                        constFound = True
                        break
                if not constFound:
                    other.tokens.extend(['+', self])
                return other
            else:
                pass
        self.value = self.calculate()
        self.power = 1
        self.coefficient = 1
        exprAdd = Expression([self, '+', other])     # Make an Expression and assign the Tokens attribute with the Constant and the Other Variable, Trig. function,...etc.
        return exprAdd

    def __rsub__(self, other):
        return self - other

    def __sub__(self, other):
        if self.isZero():
            return -1 * other
        elif other.isZero():
            return self
        elif isinstance(other, Constant):
            const = Constant()
            const.value = self.calculate() - other.calculate()
            return const
        self.value = self.calculate()
        self.power = 1
        self.coefficient = 1
        exprSub = Expression([self, '-', other])
        return exprSub

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        if other in ['+', '-', '*', '/']:
            return other
        elif self.isZero():
            return self
        elif isinstance(other, int) or isinstance(other, float):
            const = Constant()
            const.value = self.calculate() * other
            return const
        elif isinstance(other, Constant):
            if other.isZero():
                return other
            const = Constant()
            const.value = self.calculate() * other.calculate()
            return const
        elif isinstance(other, Expression):
            if other.power == 1:
                other.tokens[0] = self * other.tokens[0]
                for i, var in enumerate(other.tokens):
                    if other.tokens[i-1] == '+' or other.tokens[i-1] == '-':
                        other.tokens[i] = self * var
            else:
                if isinstance(other.power, Constant) or isinstance(other.power, int) or isinstance(other.power, float):
                    self = self ** (-1 * other.power)
                    for i, var in enumerate(other.tokens):
                        if other.tokens[i - 1] == '+' or other.tokens[i - 1] == '-':
                            other.tokens[i] = self * var
                else:
                    other.coefficient = self * other.coefficient
        else:
            if other.isZero():
                return other
            other.coefficient = self.calculate() * other.coefficient
        return other

    def __rtruediv__(self, other):
        return self / other

    def __truediv__(self, other):
        if other in ['+', '-', '*', '/']:
            return other
        elif self.isZero():
            return self
        elif isinstance(other, Constant):
            if other.isZero():
                return self     # ToDo: Raise a Division by Zero Error
            const = Constant()
            const.value = self.calculate() / other.calculate()
            return const
        elif isinstance(other, Expression):
            other.power = -1 * other.power
            newCoeff = self * other.coefficient
            other.coefficient = newCoeff
            return other
        else:
            if other.isZero():  # ToDo: Raise a Division by Zero Error
                return other
            other.coefficient = self.calculate() / other.coefficient
            other.power = [-1 * eachPower for eachPower in other.power]
        return other

    def __pow__(self, val):
        if isinstance(val, int) or isinstance(val, float):
            if self.power == 0 and self.value == 0:
                self.power = 1
                self.value = 1
            else:
                self.value = (self.value ** self.power)
                self.power = 1
            return self
        elif isinstance(val, Constant):
            self.value = self.calculate() ** val.calculate()
            self.coefficient = 1
            self.power = 1
            return self
        else:
            constExponent = Exponential()
            constExponent.base = self.value
            constExponent.coefficient = self.coefficient
            constExponent.power = val
            return constExponent

    def calculate(self):
        return self.coefficient * (self ** self.power).value

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
            for token in other.tokens:
                if isinstance(token, Constant):
                    self = Constant(self.calculate() + token.calculate())
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
        expression = Expression()
        expression.tokens = [other]
        expression.tokens.extend(['-', self])
        self.type = 'Expression'
        self = expression
        return expression

    def __sub__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self = Constant(self.calculate() - other.calculate())
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for token in other.tokens:
                if isinstance(token, Constant):
                    self = Constant(self.calculate() - token.calculate())
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
            for token in other.tokens:
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
        expression = Expression(other.tokens)
        expression.coefficient = other.coefficient/self.calculate()
        self.type = 'Expression'
        self = expression
        return expression

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
