from visma.functions import Function
from visma.functions.exponential import Logarithm

##########################
# Variable and Constants #
##########################


class Variable(Function):

    def __init__(self):
        super(Variable, self).__init__()

    def set(self, value=None, power=None, coefficient=None, scope=None, operand=None, operator=None):
        super(Variable, self).set(value, power, coefficient, scope, operand, operator)

    def inverse(self, RHS):
        self.operand = RHS.operand
        self.coefficient = (
            RHS.coefficient / self.coefficient)**(1 / self.power)
        self.power = RHS.power / self.power
        self.__class__ = RHS.__class__

    def differentiate(self):
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


class Constant(Function):

    def __init__(self):
        super(Constant, self).__init__()

    def set(self, value=None, power=None, coefficient=None, scope=None, operand=None, operator=None):
        super().set(value, power, coefficient, scope, operand, operator)

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
