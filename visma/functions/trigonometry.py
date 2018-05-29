from visma.functions.structure import Function
import math

##########################
# Trignometric Functions #
##########################


class Sine(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'sin'

    def set(self, args):
        super().set(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSine

    def differentiate(self):
        super().differentiate()
        self.__class__ = Cosine

    def integrate(self):
        self.coefficient = -1
        self.__class__ = Cosine

    def calculate(self, val):
        return self.coefficient * ((math.sin(val))**self.power)


class Cosine(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cos'

    def set(self, args):
        super().set(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCosine

    def differentiate(self):
        super().differentiate()
        self.coefficient = -1
        self.__class__ = Sine

    def integrate(self):
        self.__class__ = Sine

    def calculate(self, val):
        return self.coefficient * ((math.cos(val))**self.power)


class Tangent(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'tan'

    def set(self, args):
        super().set(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcTangent

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

    def __init__(self, arg):
        super().__init__()
        self.value = 'cot'

    def set(self, args):
        super().set(args)

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

class Secant(Function):

    def __init__(self, arg):
        super().__init__()
        self.value = 'cot'

    def set(self, args):
        super().set(args)

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSec

    def differentiate(self):
        super().differentiate()

    def integrate(self):
        """
        """

    def calculate(self, val):
        return self.coefficient * ((math.cot(val))**self.power)

##################################
# Inverse Trignometric Functions #
##################################
