from visma.functions.structure import FuncOp
from visma.functions.exponential import NaturalLog
import math

########################
# Hyberbolic Functions #
########################


class Sinh(FuncOp):
    """Class for sinh function -- sinh(...)

    Extends:
        FuncOp
    """

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
        return self.coefficient * ((math.sinh(val))**self.power)


class Cosh(FuncOp):
    """Class for cosh function -- cosh(...)

    Extends:
        FuncOp
    """

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
        return self.coefficient * ((math.cosh(val))**self.power)


class Tanh(FuncOp):
    """Class for tanh function -- tanh(...)

        Extends:
            FuncOp
        """

    def __init__(self):
        super().__init__()
        self.value = 'tanh'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcTanh

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosh       # Derivative of Tanh(x) is equal to 1-Tanh^2(x) = Sech^2(x) = Cosh^-2(x), So Class is Cosh, and Power is to be set to (-2).

    def integrate(self):
        self.__class__ = NaturalLog     # Ln(Cosh(x)), value is to be set to Cosh(...).

    def calculate(self, val):
        return self.coefficient * ((math.tanh(val)) ** self.power)

################################
# Inverse Hyperbolic Functions #
################################


class ArcSinh(FuncOp):
    pass


class ArcCosh(FuncOp):
    pass


class ArcTanh(FuncOp):
    pass
