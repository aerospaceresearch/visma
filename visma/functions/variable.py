from visma.functions.structure import Function, Expression
from visma.functions.exponential import Logarithm
from visma.functions.operator import Divide

############
# Variable #
############


class Variable(Function):
    """Class for variable type
    """

    def __init__(self, coeff=None, value=None, power=None):
        super(Variable, self).__init__()
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
        rVar = Variable()
        for i, var in enumerate(self.value):
            if var != wrtVar:
                rVar.value.append(self.value.pop(i))
                rVar.power.append(self.power.pop(i))
        if rVar.value != []:
            rToken = Expression([rToken, Divide(), rVar])
        rToken.coefficient /= (self.coefficient)**(1/self.power[0])
        rToken.power /= self.power[0]
        self.coefficient = 1
        self.power[0] = 1
        comment = "Therefore, " + r"$" + wrtVar + r"$" + " can be written as:"
        return rToken, comment

    def differentiate(self):
        from visma.functions.constant import Constant
        super(Variable, self).differentiate()
        self.value = 1
        self.__class__ = Constant

    def integrate(self):
        if self.power == -1:
            self.power = 1
            self.__class__ = Logarithm
        else:
            self.coefficient /= self.power + 1
            self.power += 1

    def calculate(self, val):
        return self.coefficient * ((val**(self.power)))
