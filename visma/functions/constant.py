import math
from visma.functions.structure import Function
from visma.functions.variable import Variable

############
# Constant #
############


class Constant(Function):
    """Class for constant type
    """

    def __init__(self):
        super(Constant, self).__init__()
        self.type = 'Constant'

    def inverse(self, RHS):
        """
        """

    def differentiate(self):
        super(Constant, self).differentiate()
        self.value = 0

    def integrate(self, intwrt):
        self.power = 1
        self.coefficient = (self.value)**(self.power)
        self.__class__ = Variable
        self.value = intwrt.value

    def calculate(self):
        return self.coefficient * ((self.value**(self.power)))


class Zero(Constant):

    def __init__(self):
        super(Zero, self).__init__()
        self.coefficient = 1
        self.value = 0
        self.power = 1


class One(Constant):

    def __init__(self):
        super(One, self).__init__()
        self.coefficient = 1
        self.value = 1
        self.power = 1


class Pi(Constant):

    def __init__(self):
        super(Pi, self).__init__()
        self.coefficient = 1
        self.value = math.pi
        self.power = 1


class Euler(Constant):

    def __init__(self):
        super(Euler, self).__init__()
        self.coefficient = 1
        self.value = math.e
        self.power = 1


class Iota(Constant):

    def __init__(self):
        super(Iota, self).__init__()
        self.coefficient = 1
        self.value = 1j
        self.power = 1
