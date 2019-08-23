import copy


class Function(object):
    """Basis function class for all functions

    The Function class forms the basis for the functions tokens of all types.
    """

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
        """Equation token to string

        Coverts equation tokens to string for text and LaTeX rendering

        Keyword Arguments:
            nv {int} -- number of values (default: {None})
            np {int} -- number of powers (default: {None})
            nc {int} -- number of coefficients (default: {None})

        Returns:
            represent {string} -- string/latex representation of equation
        """
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
        """Set function token properties

        Keyword Arguments:
            tid {[type]} -- Token ID (default: {None})
            scope {int} -- Scope (default: {None})
            value {int or list} -- Value (default: {None})
            coeff {int} -- Coefficient (default: {None})
            power {int or list} -- Power (default: {None})
            operand {visma.functions.structure.Function} -- Operand (default: {None})
            operator {visma.functions.structure.Function} -- Operator (default: {None})
        """
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
        """Differentiate function token
        """
        self.power = 1
        self.coefficient = 1

    def level(self):
        """Level of function token
        """
        return (int((len(self.tid)) / 2)), 5

    def functionOf(self):
        inst = copy.deepcopy(self)
        while inst.operand is not None:
            inst = inst.operand
        return inst.value

    def isZero(self):
        """
        It checks if the Function is equal to Zero or not, to decide it should be Added, Subtracted,...etc. or not.
        :returns: bool
        """
        if (self.value == 0 and self.power != 0) or self.coefficient == 0:
            return True
        return False


##########
# FuncOp #
##########

class FuncOp(Function):
    """Defined for functions of form sin(...), log(...), exp(...) etc which take a function(operand) as argument
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

    def inverse(self, rToken, wrtVar, inverseFunction):
        """Returns inverse of function

        Applies inverse of function to RHS and LHS.

        Arguments:
            rToken {visma.functions.structure.Function} -- RHS token
            wrtVar {string} -- with respect to variable
            inverseFunction {visma.functions.structure.Function} -- inverse of the function itself

        Returns:
            self {visma.functions.structure.Function} -- function itself(operand before inverse)
            rToken {visma.functions.structure.Function} -- new RHS token
            comment {string} -- steps comment
        """
        rToken.coefficient /= self.coefficient
        rToken.power /= self.power
        invFunc = copy.deepcopy(inverseFunction)
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
        if coefficient is not None:
            self.coefficient = coefficient
        else:
            self.coefficient = 1
        if power is not None:
            self.power = power
        else:
            self.power = 1
        self.tokens = []
        if tokens is not None:
            self.tokens.extend(tokens)

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

    def __mul__(self, other):
        from visma.functions.constant import Constant
        from visma.functions.variable import Variable

        if isinstance(other, Expression):
            result = Expression()
            for i, _ in enumerate(self.tokens):
                c = copy.deepcopy(self)
                d = copy.deepcopy(other)
                if isinstance(c.tokens[i], Constant) or isinstance(c.tokens[i], Variable):
                    result.tokens.extend([c.tokens[i] * d])
                else:
                    result.tokens.extend([c.tokens[i]])
            return result

    def __add__(self, other):
        from visma.functions.constant import Constant
        from visma.functions.variable import Variable
        from visma.functions.operator import Plus
        if isinstance(other, Expression):
            result = Expression()
            for tok1 in self.tokens:
                result.tokens.append(tok1)
            result.tokens.append(Plus())
            if (other.tokens[0], Constant):
                if (other.tokens[0].value < 0):
                    result.tokens.pop()
            elif (other.tokens[0], Variable):
                if (other.tokens[0].coefficient < 0):
                    result.tokens.pop()
            for tok2 in other.tokens:
                result.tokens.append(tok2)
            return result
        elif isinstance(other, Constant):
            result = self
            constFound = False
            for i, _ in enumerate(self.tokens):
                if isinstance(self.tokens[i], Constant):
                    self.tokens[i] += other
                    constFound = True
            if constFound:
                return result
            else:
                result.tokens += other
                return result
        elif isinstance(other, Variable):
            result = Expression()
            result = other + self
            return result

    def __sub__(self, other):
        from visma.functions.constant import Constant
        from visma.functions.variable import Variable
        from visma.functions.operator import Plus, Minus
        if isinstance(other, Expression):
            result = Expression()
            for tok1 in self.tokens:
                result.tokens.append(tok1)
            for _, x in enumerate(other.tokens):
                if x.value == '+':
                    x.value = '-'
                elif x.value == '-':
                    x.value = '+'
            result.tokens.append(Minus())
            if (isinstance(other.tokens[0], Constant)):
                if (other.tokens[0].value < 0):
                    result.tokens[-1] = Plus()
                    other.tokens[0].value = abs(other.tokens[0].value)
            elif (isinstance(other.tokens[0], Variable)):
                if (other.tokens[0].coefficient < 0):
                    result.tokens[-1] = Plus()
                    other.tokens[0].coefficient = abs(other.tokens[0].coefficient)
            return result
        elif isinstance(other, Constant):
            result = self
            result += (Constant(0) - other)
            return result
        elif isinstance(other, Variable):
            result = self
            a = Constant(0) - other
            result = a + result
            return result


class Equation(Expression):
    """Class for equation type
    """

    def __init__(self):
        super().__init__()
        self.tokens = None
