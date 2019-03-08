from visma.functions.structure import Function, Expression
from visma.functions.exponential import Logarithm
from visma.functions.operator import Divide

############
# Variable #
############


class Variable(Function):
    """Class for variable function type

    Examples:
        x
        2x^2
        3xyz^3

    Extends:
        Function
    """

    def __init__(self, coeff=None, value=None, power=None):
        super().__init__()
        # Report
        self.coefficient = 1
        if coeff is not None:
            self.coefficient = coeff
        self.value = []
        if value is not None:
            self.value.append(value)
        self.power = []
        if power is not None:
            self.power.append(power)
        self.type = 'Variable'

    def inverse(self, rToken, wrtVar):
        l2rVar = Variable()
        for i, var in enumerate(self.value):
            if var != wrtVar:
                l2rVar.value.append(self.value.pop(i))
                l2rVar.power.append(self.power.pop(i))
        if l2rVar.value != []:
            rToken = Expression([rToken, Divide(), l2rVar])
        rToken.coefficient /= (self.coefficient)**(1/self.power[0])
        rToken.power /= self.power[0]
        self.coefficient = 1
        self.power[0] = 1
        comment = "Therefore, " + r"$" + wrtVar + r"$" + " can be written as:"
        return self, rToken, comment

    def differentiate(self):
        from visma.functions.constant import Constant
        super().differentiate()
        self.value = 1
        self.__class__ = Constant

    def integrate(self, wrtVar):
        if wrtVar not in self.value:
            self.value.append(wrtVar)
            self.power.append(1)
        else:
            for i, val in enumerate(self.value):
                if val == 'wrtVar':
                    break
            if self.power[i] == -1:
                self.power.pop(i)
                self.value.pop(i)
                expression = Expression()
                expression.tokens = [self]
                variable = Variable(1, 'wrtVar', 1)
                expression.tokens.append(Logarithm(variable))
                self.__class__ = Expression
                self = expression
            else:
                self.coefficient /= self.power[i] + 1
                self.power[i] += 1

    def calculate(self, val):
        return self.coefficient * ((val**(self.power)))
