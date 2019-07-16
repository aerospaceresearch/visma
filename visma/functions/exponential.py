import math
import copy
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

    def differentiate(self, wrtVar=None):
        from visma.functions.variable import Variable
        result = copy.deepcopy(self)
        result.__class__ = Variable
        result.coefficient = 1
        result.value = wrtVar
        result.power = [-1]
        result.operand = None
        return result


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
    """Class for all constant exponential functions -- as exp(...) or 5^(...)

    Extends:
        FuncOp
    """

    def __init__(self, val=None):
        super().__init__()
        self.value = 'exp'
        if not val:
            self.base = val
        else:
            self.base = math.e

    def calculate(self):
        from visma.functions.constant import Constant
        if isinstance(self.power, int) or isinstance(self.power, float) or isinstance(self.power, Constant):
            const = Constant()
            if isinstance(self.power, Constant):
                self.power = self.power.calculate()
            const.value = self.coefficient * (self.base ** self.power)
            return const
        else:
            return self
