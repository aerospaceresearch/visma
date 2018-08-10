from visma.functions.structure import *

########################
# Hyberbolic Functions #
########################


class Sinh(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'sinh'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcSinh

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosh

    def integrate(self):
        self.__class__ = Cosh

    def calculate(self, input):
        return coefficient * ((math.sin(input))**power)


class Cosh(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cosh'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcCosine

    def differentiate(self):
        super().differentiate()
        self.__class__ = Sinh

    def integrate(self):
        self.__class__ = Sinh

    def calculate(self, input):
        return coefficient * ((math.cos(input))**power)


################################
# Inverse Hyperbolic Functions #
################################
