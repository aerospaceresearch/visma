from visma.functions.structure import *

#########################
# Exponential Functions #
#########################


class Logarithm(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = []

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()

    def differentiate(self):
        super().differentiate()
        self.power = -1
        self.__class__ = operand.__class__

    def integrate(self, d):
        """
        """

    def calculate(self, input):
        return self.coefficient * ((math.log(input, self.base)))


class Exponential(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = []

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()

    def differentiate(self):
        super().differentiate()

    def integrate(self, d):
        """
        """

    def calculate(self, input):
        return self.coefficient * ((math.exp(input)))
