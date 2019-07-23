import math
import copy
from visma.functions.structure import FuncOp, Expression
from visma.functions.operator import Multiply, Plus
from visma.functions.constant import Constant
from visma.functions. exponential import NaturalLog

##########################
# Trignometric Functions #
##########################


class Trigonometric(FuncOp):
    """Parent Class for all the Trigonometric Classes like Sine, Cosine, Tangent etc.

    """
    pass


class Sine(Trigonometric):
    """Class for sin function -- sin(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'sin'

    def inverse(self, rToken, wrtVar, inverseFunction=None):
        inverseFunction = ArcSin()
        super().inverse(self, rToken, wrtVar, inverseFunction)

    def calculate(self, val):
        return self.coefficient * ((math.sin(val))**self.power)

    def differentiate(self, wrtVar=None):
        super().differentiate()
        result = copy.deepcopy(self)
        result.__class__ = Cosine
        result.value = 'cos'
        result.coefficient = 1
        return result

    def integrate(self, wrtVar=None):
        term1 = Constant(-1, 1, 1)
        term2 = copy.deepcopy(self)
        term2.__class__ = Cosine
        term2.value = 'cos'
        term2.coefficient = 1
        result = Expression()
        result.tokens = [term1, Multiply(), term2]
        return result


class Cosine(Trigonometric):
    """Class for cos function -- cos(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'cos'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCos

    def differentiate(self, wrtVar):
        term1 = Constant(-1, 1, 1)
        term2 = copy.deepcopy(self)
        term2.__class__ = Sine
        term2.value = 'sin'
        result = Expression()
        result.tokens = [term1, Multiply(), term2]
        return result

    def integrate(self, wrtVar):
        result = copy.deepcopy(self)
        result.__class__ = Sine
        result.value = 'sin'
        result.coefficient = 1
        return result

    def calculate(self, val):
        return self.coefficient * ((math.cos(val))**self.power)


class Tangent(Trigonometric):
    """Class for tan function -- tan(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'tan'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcTan

    def differentiate(self, wrtVar):
        result = copy.deepcopy(self)
        result.__class__ = Secant
        result.value = 'sec'
        result.coefficient = 1
        result.power = 2
        return result

    def integrate(self, wrtVar):
        term1 = Constant(-1, 1, 1)
        term2 = NaturalLog()
        term3 = Cosine()
        term3.operand = self.operand
        term2.operand = term3
        term2.power = 1
        term2.coefficient = 1
        result = Expression()
        result.tokens = [term1, Multiply(), term2]
        return result

    def calculate(self, val):
        return self.coefficient * ((math.tan(val))**self.power)


class Cotangent(Trigonometric):
    """Class for cot function -- cot(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'cot'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCot

    def differentiate(self, wrtVar):
        term1 = Constant(-1, 1, 1)
        term2 = copy.deepcopy(self)
        term2.__class__ = Cosecant
        term2.value = 'csc'
        term2.coefficient = 1
        term2.power = 2
        result = Expression()
        result.tokens = [term1, Multiply(), term2]
        return result

    def integrate(self, wrtVar):
        result = NaturalLog()
        term1 = Sine()
        term1.operand = self.operand
        term1.power = 1
        term1.coefficient = 1
        result.operand = term1
        return result

    def calculate(self, val):
        return self.coefficient * ((math.cot(val))**self.power)


class Cosecant(Trigonometric):
    """Class for csc function -- csc(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'csc'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcCosec

    def differentiate(self, wrtVar):
        term1 = Constant(-1, 1, 1)
        term2 = Cosecant()
        term2.operand = self.operand
        term2.coefficient = 1
        term3 = Cotangent()
        term3.operand = self.operand
        term3.coefficient = 1
        result = Expression()
        result.tokens = [term1, Multiply(), term2, Multiply(), term3]
        return result

    def integrate(self, wrtVar):
        term1 = Constant(-1, 1, 1)
        term2 = NaturalLog()
        result = Expression()
        term3 = Cosecant()
        term3.operand = self.operand
        term4 = Cotangent()
        term4.operand = self.operand
        inExpression = Expression()
        inExpression.tokens = [term3, Plus(), term4]
        term2.operand = inExpression
        term2.power = 1
        term2.coefficient = 1
        result.tokens = [term1, Multiply(), term2]
        return result

    def __mul__(self, other):
        if isinstance(other, Cotangent):
            result = Expression()
            result.coefficient = self.coefficient * other.coefficient
            c = copy.deepcopy(self)
            d = copy.deepcopy(other)
            result.tokens.extend([c, Multiply(), d])
            return result

    def calculate(self, val):
        return self.coefficient * ((math.cosec(val))**self.power)


class Secant(Trigonometric):
    """Class for sec function -- sec(...)

    Extends:
        Trigonometric
    """

    def __init__(self):
        super().__init__()
        self.value = 'sec'

    def inverse(self, RHS):
        super().inverse(RHS)
        self.__class__ = ArcSec

    def differentiate(self, wrtVar):
        term1 = Tangent()
        term1.operand = self.operand
        term2 = Secant()
        term2.operand = self.operand
        resultTerm = term2 * term1
        return resultTerm

    def integrate(self, wrtVar):
        resultTerm = NaturalLog()
        term3 = Secant()
        term3.operand = self.operand
        term4 = Tangent()
        term4.operand = self.operand
        inExpression = Expression()
        inExpression.tokens = [term3, Plus(), term4]
        resultTerm.operand = inExpression
        resultTerm.power = 1
        resultTerm.coefficient = 1
        return resultTerm

    def __mul__(self, other):
        if isinstance(other, Tangent):
            result = Expression()
            Expression.coefficient = self.coefficient * other.coefficient
            c = copy.deepcopy(self)
            d = copy.deepcopy(other)
            result.tokens.extend([c, Multiply(), d])
            return result

    def calculate(self, val):
        return self.coefficient * ((math.sec(val))**self.power)

##################################
# Inverse Trignometric Functions #
##################################


class ArcSin(Trigonometric):
    pass


class ArcCos(Trigonometric):
    pass


class ArcTan(Trigonometric):
    pass


class ArcCot(Trigonometric):
    pass


class ArcSec(Trigonometric):
    pass


class ArcCsc(Trigonometric):
    pass
