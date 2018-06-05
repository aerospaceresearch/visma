# This module contains classes for all functions


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

    def __str__(self):
        represent = ""
        if self.coefficient != 1:
            represent += str(self.coefficient)
        if isinstance(self.value, list):
            for eachValue, eachPower in zip(self.value, self.power):
                represent += "{" + str(eachValue) + "}"
                if eachPower != 1:
                    represent += "^" + "{" + str(eachPower) + "}"
        else:
            represent += "{" + str(self.value) + "}"
            if self.power != 1:
                represent += "^" + "{" + str(self.power) + "}"
            if self.operand is not None:
                represent += "({" + str(self.power) + "})"
        return represent

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
        self.coefficient = 1
        self.power = 1
        self.tokens = None
        self.type = 'Expression'

    def __str__(self):
        represent = ""
        if self.coefficient != 1:
            represent += str(self.coefficient) + "*"
        represent += "{("
        for token in self.tokens:
            represent += token.__str__()
        represent += ")}"
        if self.power != 1:
            represent += "^" + "{" + str(self.power) + "}"
        if self.operand is not None:
            represent += "{(" + str(self.operand.__str__) + ")}"
        return represent


class Equation(Function):
    """Class for equation type
    """

    def __init__(self):
        super(Equation, self).__init__()
        self.tokens = None
        self.type = 'Equation'
