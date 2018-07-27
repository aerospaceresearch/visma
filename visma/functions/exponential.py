import math
from visma.functions.structure import FuncOp

#########################
# Exponential Functions #
#########################


class Logarithm(FuncOp):

    def __init__(self, operand=None):
        super().__init__()
        self.base = 10
        self.value = 'log'

    def inverse(self, rToken, wrtVar, inverseFunction=None):
        inverseFunction = Exponential()
        super().inverse(self, rToken, wrtVar, inverseFunction)

    def calculate(self, val):
        return self.coefficient * ((math.log(val, self.base)))


class NaturalLog(Logarithm):

    def __init__(self, operand=None):
        super().__init__()
        self.base = math.exp(1)
        self.value = 'ln'


class Exponential(FuncOp):

    def __init__(self):
        super().__init__()
        self.value = 'exp'

    def calculate(self, val):
        return self.coefficient * (math.exp(val))
