from visma.functions.structure import Function
import math

########################
# Hyberbolic Functions #
########################


class Sinh(Function):

    def __init__(self):
        super().__init__()
        self.value = 'sinh'

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

    def __init__(self):
        super().__init__()
        self.value = 'cosh'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCosh

    def differentiate(self):
        super().differentiate()
        self.__class__ = Sinh

    def integrate(self):
        self.__class__ = Sinh

    def calculate(self, val):
        return self.coefficient * ((math.cos(val))**self.power)


class Tanh(Function):
    pass

################################
# Inverse Hyperbolic Functions #
################################


class ArcSinh(Function):
    pass


class ArcCosh(Function):
    pass


class ArcTanh(Function):
    pass
