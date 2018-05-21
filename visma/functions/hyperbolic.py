from visma.functions.structure import Function
import math
########################
# Hyberbolic Functions #
########################


class Sinh(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'sinh'

    def setprop(self, args):
        super().setprop(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSinh

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosh

    def integrate(self):
        self.__class__ = Cosh

    def calculate(self, val):
        return self.coefficient * ((math.sin(val))**self.power)


class Cosh(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cosh'

    def setprop(self, args):
        super().setprop(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCosine

    def differentiate(self):
        super().differentiate()
        self.__class__ = Sinh

    def integrate(self):
        self.__class__ = Sinh

    def calculate(self, val):
        return self.coefficient * ((math.cos(val))**self.power)


################################
# Inverse Hyperbolic Functions #
################################
