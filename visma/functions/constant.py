import math
from visma.functions.structure import Function
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
