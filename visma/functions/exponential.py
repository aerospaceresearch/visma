from visma.functions.structure import Function
import math

#########################
# Exponential Functions #
#########################


class Logarithm(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = []

    def setprop(self, args):
        super().setprop(args)

    def inverse(self, RHS):
        super().inverse(RHS)

    def differentiate(self):
        super().differentiate()
        self.power = -1
        self.__class__ = operand.__class__

    def integrate(self, d):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.log(val, self.base)))


class Exponential(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = []

    def setprop(self, args):
        super().setprop(args)

    def inverse(self, RHS):
        super().inverse(RHS)

    def differentiate(self):
        super().differentiate()

    def integrate(self, d):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.exp(val)))
