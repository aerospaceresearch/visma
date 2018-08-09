import math
from visma.functions.structure import FuncOp

#########################
# Exponential Functions #
#########################


class Logarithm(FuncOp):
    """Class for log function -- log(...)

    Input examples:
        log(2) [without base, default base 10]
        log_4(x+y) [with base]

    Extends:
        FuncOp
    """

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
    """Class for ln function -- ln(...) or use log_e(...)

    Extends:
        Logarithm
    """

    def __init__(self, operand=None):
        super().__init__()
        self.base = math.exp(1)
        self.value = 'ln'


class Exponential(FuncOp):
    """Class for exponential function -- exp(...)

    Extends:
        FuncOp
    """

    def __init__(self):
        super().__init__()
        self.value = 'exp'

    def calculate(self, val):
        return self.coefficient * (math.exp(val))
