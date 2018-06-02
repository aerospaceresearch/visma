# This module contains classes for all functions
# TODO: Add exponential, logarithmic, trigonometric and hyperbolic functions
# FIXME: Fix method arguments


class Function(object):

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None
        self.coefficient = None
        self.power = None
        self.operand = None
        self.operator = None
        self.before = None
        self.after = None
        self.beforeScope = None
        self.afterScope = None

    def inverse(self, RHS):
        RHS.coefficient = (RHS.coefficient / self.coefficient)**(1 / self.power)
        RHS.power /= self.power
        self.operand = RHS
        self.coefficient = 1
        self.power = 1

    def differentiate(self):
        self.power = 1
        self.coefficient = 1

    def level(self):
        return (int((len(self.tid)) / 2))


###################
# Mixed Functions #
###################
# For example: sec(x)*tan(x) or sin(x)*log(x) or e^(x)*cot(x)
# Will be taken care by function 'Token ID'ing/tokening module

class Expression(Function):
    """Class for expression type
    """

    def __init__(self):
        super(Expression, self).__init__()
        self.tokens = None
        self.type = 'Expression'


class Equation(Function):
    """Class for equation type
    """

    def __init__(self):
        super(Equation, self).__init__()
        self.tokens = None
        self.type = 'Equation'
