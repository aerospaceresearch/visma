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
