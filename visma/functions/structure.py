import copy


class Function(object):

    def __init__(self):
        self.tid = None
        self.scope = None
        self.value = None
        self.coefficient = 1
        self.power = 1
        self.operand = None
        self.operator = None
        self.before = None
        self.after = None
        self.beforeScope = None
        self.afterScope = None

    def __str__(self, nv=None, np=None, nc=None):
        # OPTIMIZE: Works but a mess. Organize and add comments
        represent = ""

        if np is None and nv is None and nc is None:
            if self.coefficient != 1:
                represent += str(self.coefficient)
        elif nc is not None:
            if self.coefficient[nc] != 1:
                represent += str(self.coefficient[nc])

        if isinstance(self.value, list):
            if nv is None and np is None:
                for eachValue, eachPower in zip(self.value, self.power):
                    represent += "{" + str(eachValue) + "}"
                    if eachPower != 1:
                        represent += "^" + "{" + str(eachPower) + "}"
            elif nc is None:
                represent += "{" + str(self.value[nv]) + "}"
                if self.power[np] != 1:
                    represent += "^" + "{" + str(self.power[np]) + "}"
            elif nc is not None:
                for i, val in enumerate(self.value):
                    represent += "{" + str(val) + "}"
                    if self.power[np][i] != 1:
                        represent += "^" + "{" + str(self.power[np][i]) + "}"
        elif self.operand is not None:
            represent += "\\" + self.value
            if self.power != 1:
                represent += "^" + "{" + str(self.power) + "}"
            represent += "({" + self.operand.__str__() + "})"
        else:
            represent += "{" + str(self.value) + "}"
            if self.power != 1:
                represent += "^" + "{" + str(self.power) + "}"

        return represent

    def prop(self, tid=None, scope=None, value=None, coeff=None, power=None, operand=None, operator=None):
        if tid is not None:
            self.tid = tid
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value
        if coeff is not None:
            self.coefficient = coeff
        if power is not None:
            self.power = power
        if operand is not None:
            self.operand = operand
        if operator is not None:
            self.operator = operator

    def differentiate(self):
        self.power = 1
        self.coefficient = 1

    def level(self):
        return (int((len(self.tid)) / 2))

    def functionOf(self):
        inst = copy.deepcopy(self)
        while inst.operand is not None:
            inst = inst.operand
        return inst.value


##########
# FuncOp #
##########

class FuncOp(Function):
    """Defined for functions of form sin(), log(), exp() etc which take a function(operand) as argument
    """
    def __init__(self, operand=None):
        super().__init__()
        if operand is not None:
            self.operand = operand

    def __str__(self):
        represent = ""
        represent += "\\" + self.value
        if self.power != 1:
            represent += "^" + "{" + str(self.power) + "}"
        if self.operand is not None:
            represent += "{(" + str(self.operand) + ")}"
        return represent

    def inverse(self, rToken, wrtVar):
        rToken.coefficient /= self.coefficient
        rToken.power /= self.power
        invFunc = copy.deepcopy(self.inverseFunction)
        invFunc.operand = rToken
        self = self.operand
        comment = "Applying inverse function on LHS and RHS"
        return self, rToken, comment


###################
# Mixed Functions #
###################
# For example: sec(x)*tan(x) or sin(x)*log(x) or e^(x)*cot(x)
# Will be taken care by function Expression

class Expression(Function):
    """Class for expression type
    """

    def __init__(self, tokens=None, coefficient=None, power=None):
        super().__init__()
        self.coefficient = 1
        self.power = 1
        self.tokens = []
        if tokens is not None:
            self.tokens.extend(tokens)
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
            represent += "{(" + str(self.operand) + ")}"
        return represent


class Equation(Expression):
    """Class for equation type
    """

    def __init__(self):
        super().__init__()
        self.tokens = None
        self.type = 'Equation'
