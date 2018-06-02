from visma.functions.structure import Function
from visma.functions.exponential import Logarithm

############
# Variable #
############


class Variable(Function):
    """Class for variable type
    """

    def __init__(self):
        super(Variable, self).__init__()
        self.type = 'Variable'

    def inverse(self, RHS):
        self.operand = RHS.operand
        self.coefficient = (
            RHS.coefficient / self.coefficient)**(1 / self.power)
        self.power = RHS.power / self.power
        self.__class__ = RHS.__class__

    def differentiate(self):
        # FIXME: Circular imports
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
