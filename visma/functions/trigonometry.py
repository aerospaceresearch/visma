from visma.functions.structure import *

##########################
# Trignometric Functions #
##########################


class Sine(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'sin'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcSine

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosine

    def integrate(self):
        self.coefficient = -1
        self.__class__ = Cosine

    def calculate(self, input):
        return coefficient * ((math.sin(input))**power)


class Cosine(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cos'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcCosine

    def differentiate(self):
        super().differentiate()
        self.coefficient = -1
        self.__class__ = Sine

    def integrate(self):
        self.__class__ = Sine

    def calculate(self, input):
        return coefficient * ((math.cos(input))**power)


class Tangent(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'tan'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcTangent

    def differentiate(self):
        super().differentiate()
        self.power = 2
        self.__class__ = Secant

    def integrate(self):
        """
        """

    def calculate(self, input):
        return coefficient * ((math.tan(input))**power)


class Cotangent(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cot'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcCot

    def differentiate(self):
        super().differentiate()
        self.coefficient = -1
        self.power = 2
        self.__class__ = Cosecant

    def integrate(self):
        """
        """

    def calculate(self, input):
        return coefficient * ((math.cot(input))**power)


# Incomplete

class Secant(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cot'

    def set(args):
        super().set()

    def inverse(self, RHS):
        super().inverse()
        self.__class__ = ArcSec

    def differentiate(self):
        super().differentiate()

    def integrate(self):
        """
        """

    def calculate(self, input):
        return coefficient * ((math.cot(input))**power)

##################################
# Inverse Trignometric Functions #
##################################
