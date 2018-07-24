from visma.functions.structure import Function
import math

##########################
# Trignometric Functions #
##########################


class Sine(Function):

    def __init__(self):
        super().__init__()
        self.value = 'sin'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSin

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosine

    def integrate(self):
        self.coefficient = -1
        self.__class__ = Cosine

    def calculate(self, val):
        return self.coefficient * ((math.sin(val))**self.power)


class Cosine(Function):

    def __init__(self):
        super().__init__()
        self.value = 'cos'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCos

    def differentiate(self):
        super().differentiate()
        self.coefficient = -1
        self.__class__ = Sine

    def integrate(self):
        self.__class__ = Sine

    def calculate(self, val):
        return self.coefficient * ((math.cos(val))**self.power)


class Tangent(Function):

    def __init__(self):
        super().__init__()
        self.value = 'tan'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcTan

    def differentiate(self):
        super().differentiate()
        self.power = 2
        self.__class__ = Secant

    def integrate(self):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.tan(val))**self.power)


class Cotangent(Function):

    def __init__(self):
        super().__init__()
        self.value = 'cot'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCot

    def differentiate(self):
        super().differentiate()
        self.coefficient = -1
        self.power = 2
        self.__class__ = Cosecant

    def integrate(self):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.cot(val))**self.power)


# Incomplete

class Cosecant(Function):

    def __init__(self):
        super().__init__()
        self.value = 'csc'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCosec

    def differentiate(self):
        super().differentiate()

    def integrate(self):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.cosec(val))**self.power)


class Secant(Function):

    def __init__(self):
        super().__init__()
        self.value = 'sec'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSec

    def differentiate(self):
        super().differentiate()

    def integrate(self):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.sec(val))**self.power)

##################################
# Inverse Trignometric Functions #
##################################


class ArcSin(Function):
    pass


class ArcCos(Function):
    pass


class ArcTan(Function):
    pass


class ArcCot(Function):
    pass


class ArcSec(Function):
    pass


class ArcCsc(Function):
    pass
