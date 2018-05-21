from visma.functions import Function


##########################
# Variable and Constants #
##########################


class Variable(Function):

    def __init__(self):
        super().__init__()
        self.value = []

    def setprop(self, tid, scope, coefficient, power, operand, operator, value):
        super().setprop(args)

    def inverse(self, RHS):
        self.operand = RHS.operand
        self.coefficient = (
            RHS.coefficient / self.coefficient)**(1 / self.power)
        self.power = RHS.power / self.power
        self.__class__ = RHS.__class__

    def differentiate(self):
        super().differentiate()
        self.value = 1
        self.__class__ = Constant

    def integrate(self):
        if self.power == -1:
            self.power = 1
            self.__class__ = Logarithm
        else:
            self.coefficient /= power + 1
            self.power += 1

    def calculate(self, val):
        return self.coefficient * ((val**(self.power)))


class Constant(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = []

    def setprop(self, args):
        super().setprop(args)

    def inverse(self, RHS):
        """
        """

    def differentiate(self):
        super().differentiate()
        self.value = 0

    def integrate(self, intwrt):
        self.power = 1
        self.coefficient = (self.value)**(self.power)
        self.__class__ = Variable
        self.value = intwrt.value

    def calculate(self):
        return self.coefficient * ((self.value**(self.power)))
