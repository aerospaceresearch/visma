import math
from visma.functions.structure import Function, Expression
from visma.functions.variable import Variable
from visma.functions.exponential import Exponential
from visma.functions.operator import Plus, Minus

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
        if isinstance(other, Constant):
            if self.before == '-':
                result = Constant(self.calculate() - other.calculate(), self.power)
            else:
                result = Constant(self.calculate() + other.calculate(), self.power)
            self.value = result.value
            if result.value == 0 and result.power == 0:
                result.value = 1
                result.power = 1
            result.scope = self.scope
            result.value = result.calculate()
            return result
        elif self.isZero():
            return other
        elif other.isZero():
            return self
        elif isinstance(other, Expression):
            if other.power == 1 and other.coefficient == 1:
                constFound = False
                for i, var in enumerate(other.tokens):
                    if isinstance(var, Constant):
                        if other.tokens[i-1].value == '+' or i == 0:
                            other.tokens[i] = self + var
                        elif other.tokens[i-1].value == '-':
                            other.tokens[i-1] = self - var
                        constFound = True
                        break
                if not constFound:
                    other.tokens.extend([Plus(), self])
                return other
            else:
                pass
        self.value = self.calculate()
        self.power = 1
        self.coefficient = 1
        exprAdd = Expression([self, Plus(), other])     # Make an Expression and assign the Tokens attribute with the Constant and the Other Variable, Trig. function,...etc.
        return exprAdd

    def __rsub__(self, other):
        return Constant(0) - self + other

    def __sub__(self, other):
        if isinstance(other, Constant):
            self = self + Constant(-1, 1, 1) * other
            return self
        elif isinstance(other, Variable):
            if self.value == 0:
                other.coefficient *= -1
                return other
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend([Minus(), other])
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            if other.power == 1:
                coeff = other.coefficient
                for i, token in enumerate(other.tokens):
                    print(expression, " ", type(token), other.tokens[i-1])
                    if isinstance(token, Constant):
                        if other.tokens[i-1].value == '+' or i == 0:
                            expression.tokens[0] = Constant(self.calculate() - token.calculate()*coeff)
                        elif other.tokens[i-1].value == '-':
                            expression.tokens[0] = Constant(self.calculate() + token.calculate()*coeff)
                    elif isinstance(token, Variable):
                        if other.tokens[i-1].value == '+' or i == 0:
                            expression.tokens.extend([Minus(), Variable(token)])
                        elif other.tokens[i-1].value == '-':
                            expression.tokens.extend([Plus(), Variable(token)])
            else:
                expression.tokens.extend([Minus(), other])
        self = expression
        return expression

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        if other.isZero():
            return other
        elif self.isZero():
            return self
        elif isinstance(other, Constant):
            const = Constant(self.calculate() * other.calculate())
            return const
        elif isinstance(other, Variable):
            variable = Variable()
            variable.coefficient = self.calculate() * other.coefficient
            variable.value.extend(other.value)
            variable.power.extend(other.power)
            self = variable
            return variable
        elif isinstance(other, Expression):
            if other.power == 1:
                other.tokens[0] = self * other.tokens[0]
                for i, var in enumerate(other.tokens):
                    if other.tokens[i-1].value == '+' or other.tokens[i-1].value == '-':
                        other.tokens[i] = self * var
            else:
                if isinstance(other.power, Constant) or isinstance(other.power, int) or isinstance(other.power, float):
                    self = self ** (-1 * other.power)
                    for i, var in enumerate(other.tokens):
                        if other.tokens[i - 1].value == '+' or other.tokens[i - 1].value == '-':
                            other.tokens[i] = self * var
                else:
                    other.coefficient = self * other.coefficient
        else:
            other.coefficient = self.calculate() * other.coefficient
        return other

    def __rtruediv__(self, other):
        return Constant(1) / self * other

    def __truediv__(self, other):
        if other.value in ['+', '-', '*', '/']:
            return other
        elif self.isZero():
            return self
        elif isinstance(other, Constant):
            result = Constant()
            power = Constant(-1, 1, 1)
            result = self * (other ** power)
            return result

        elif isinstance(other, Variable):
            power = Constant(-1, 1, 1)
            self = self * (other ** power)
            return self
        elif isinstance(other, Expression):
            other.power = -1 * other.power
            newCoeff = self * Constant(other.coefficient)
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

    def functionOf(self):
        return []

    def binary(self):
        '''Returns a binary string of the given constant
        '''
        return bin(self.calculate())[2:]


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
