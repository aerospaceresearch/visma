from visma.functions.structure import FuncOp
import math

#########################
# Exponential Functions #
#########################


class Logarithm(FuncOp):

    def __init__(self, operand=None):
        super().__init__()
        self.base = 10
        self.value = 'log'

    def differentiate(self):
        super().differentiate()
        self.power = -1
        self.__class__ = self.operand.__class__

    def calculate(self, val):
        return self.coefficient * ((math.log(val, self.base)))


class NaturalLog(FuncOp):

    def __init__(self, operand=None):
        super().__init__()
        self.base = math.exp(1)
        self.value = 'ln'


class Exponential(FuncOp):

    def __init__(self):
        super().__init__()
        self.value = 'exp'

    def inverse(self, RHS):
        super().inverse(RHS)

    def differentiate(self):
        super().differentiate()

    def integrate(self, d):
        pass

    def calculate(self, val):
        return self.coefficient * (math.exp(val))
