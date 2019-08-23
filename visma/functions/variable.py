import copy
from visma.functions.structure import Function, Expression
from visma.functions.exponential import Logarithm
from visma.functions.operator import Plus, Minus, Multiply, Divide, Binary


############
# Variable #
############


class Variable(Function):
    """Class for variable function type

    Examples:
        x
        2x^2
        3xyz^3

    Extends:
        Function
    """

    def __init__(self, coeff=None, value=None, power=None):
        super().__init__()
        # Report
        self.coefficient = 1
        if coeff is not None:
            self.coefficient = coeff
        self.value = []
        if value is not None:
            self.value.append(value)
        self.power = []
        if power is not None:
            self.power.append(power)

    def inverse(self, rToken, wrtVar):
        l2rVar = Variable()
        for i, var in enumerate(self.value):
            if var != wrtVar:
                l2rVar.value.append(self.value.pop(i))
                l2rVar.power.append(self.power.pop(i))
        if l2rVar.value != []:
            rToken = Expression([rToken, Divide(), l2rVar])
        rToken.coefficient /= (self.coefficient)**(1/self.power[0])
        rToken.power /= self.power[0]
        self.coefficient = 1
        self.power[0] = 1
        comment = "Therefore, " + r"$" + wrtVar + r"$" + " can be written as:"
        return self, rToken, comment

    def differentiate(self, wrtVar):
        from visma.functions.constant import Constant, Zero
        result = copy.deepcopy(self)
        if wrtVar in result.functionOf():
            for i, var in enumerate(result.value):
                if var == wrtVar:
                    result.coefficient *= result.power[i]
                    result.power[i] -= 1
                    if(result.power[i] == 0):
                        del result.power[i]
                        del result.value[i]
                        if result.value == []:
                            result.__class__ = Constant
                            result.value = result.coefficient
                            result.coefficient = 1
                            result.power = 1
        else:
            result = Zero()
        return result

    def integrate(self, wrtVar=None):
        from visma.functions.constant import Constant
        result = copy.deepcopy(self)
        log = False
        for i, var in enumerate(result.value):
            if var == wrtVar:
                if(result.power[i] == -1):
                    log = True
                    funcLog = Logarithm()
                    funcLog.operand = Variable()
                    funcLog.operand.coefficient = 1
                    funcLog.operand.value.append(result.value[i])
                    funcLog.operand.power.append(1)
                    del result.power[i]
                    del result.value[i]
                    if result.value == []:
                        result.__class__ = Constant
                        result.value = result.coefficient
                        result.coefficient = 1
                        result.power = 1
                    result = [result]
                    funcJoin = Binary()
                    funcJoin.value = '*'
                    result.append(funcJoin)
                    result.append(funcLog)
                else:
                    result.power[i] += 1
                    result.coefficient /= result.power[i]
        print(result)
        return result, log

    def calculate(self, val):
        return self.coefficient * ((val**(self.power)))

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Variable):
            sortedValuesSelf = sorted(self.value)
            sortedValuesOther = sorted(other.value)
            if self.coefficient == 0:
                return Constant(0, 1, 1)
            if (self.power == other.power) & (sortedValuesSelf == sortedValuesOther):
                if self.before == '-':
                    self.coefficient -= other.coefficient
                else:
                    self.coefficient += other.coefficient
                return self
        elif isinstance(other, Constant):
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend([Plus(), other])
            self = expression
            return expression
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Variable):
                    tokenValueSorted = sorted(token.value)
                    selfValueSorted = sorted(self.value)
                    if (token.power == self.power) & (tokenValueSorted == selfValueSorted):
                        if other.tokens[i - 1].value == '+' or (i == 0):
                            self.coefficient += other.tokens[i].coefficient
                        elif other.tokens[i - 1].value == '-':
                            self.coefficient -= other.tokens[i].coefficient
                    else:
                        if other.tokens[i-1].value == '+' or i == 0:
                            expression.tokens.extend([Plus(), Variable(token)])
                        elif other.tokens[i-1].value == '-':
                            expression.tokens.extend([Minus(), Variable(token)])
                elif not isinstance(token, Binary):
                    if other.tokens[i - 1].value == '+' or (i == 0):
                        expression.tokens.extend([Plus(), token])
                    elif other.tokens[i - 1].value == '-':
                        expression.tokens.extend([Minus(), token])
            expression.tokens[0] = self
            self = expression
            return expression

    def __rsub__(self, other):
        from visma.functions.constant import Constant
        return Constant(0, 1, 1) - self + other

    def __sub__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Variable):
            otherValueSorted = sorted(other.value)
            selfValueSorted = sorted(self.value)
            if (other.power == self.power) & (selfValueSorted == otherValueSorted):
                self = self + Constant(-1, 1, 1) * other
                return self
            else:
                expression = Expression()
                expression.tokens = [self]
                expression.tokens.extend([Minus(), other])
                self = expression
                return expression
        elif isinstance(other, Constant):
            if other.isZero():
                return self
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend([Minus(), other])
            self = expression
            return expression
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Variable):
                    tokenValueSorted = sorted(token.value)
                    selfValueSorted = sorted(self.value)
                    if (token.power == self.power) & (tokenValueSorted == selfValueSorted):
                        if other.tokens[i - 1].value == '+' or (i == 0):
                            self.coefficient -= other.tokens[i].coefficient
                        elif other.tokens[i - 1].value == '-':
                            self.coefficient += other.tokens[i].coefficient
                    else:
                        if other.tokens[i-1].value == '+' or i == 0:
                            expression.tokens.extend([Plus(), Variable(token)])
                        elif other.tokens[i-1].value == '-':
                            expression.tokens.extend([Minus(), Variable(token)])
                elif not isinstance(token, Binary):
                    if other.tokens[i - 1].value == '+' or (i == 0):
                        expression.tokens.extend([Minus(), token])
                    elif other.tokens[i - 1].value == '-':
                        expression.tokens.extend([Plus(), token])
            expression.tokens[0] = self
            self = expression
            return expression

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        from visma.io.checks import isNumber
        from visma.functions.constant import Constant

        if isinstance(other, Variable):
            for j, var in enumerate(other.value):
                found = False
                for k, var2 in enumerate(self.value):
                    self.coefficient *= other.coefficient
                    if var == var2:
                        if isNumber(other.power[j]) and isNumber(self.power[k]):
                            self.power[k] += other.power[j]
                            if self.power[k] == 0:
                                del self.power[k]
                                del self.value[k]
                            found = True
                            break
                if not found:
                    self.value.append(other.value[j])
                    self.power.append(other.power[j])

                if len(self.value) == 0:
                    result = Constant(self.coefficient)
                    result.scope = self.scope
                    result.power = 1
                    result.value = self.coefficient
                    self = result
            return self
        elif isinstance(other, Constant):
            self.coefficient *= other.calculate()
            return self
        elif isinstance(other, Expression):
            result = Expression()
            for _, token in enumerate(other.tokens):
                if isinstance(token, Variable) or isinstance(token, Constant):
                    c = copy.deepcopy(self)
                    result.tokens.extend([c * token])
                else:
                    result.tokens.extend([token])
            return result

    def __pow__(self, other):
        from visma.functions.constant import Constant

        if isinstance(other, Constant):
            if other.value == -1:
                one = Constant(1, 1, 1)
                result = Variable()
                result.value = self.value
                result.coefficient = one.calculate() / self.coefficient
                result.power = []
                for pows in self.power:
                    result.power.append(-pows)
                return result

    def __rtruediv__(self, other):
        pass                                    # TODO : Add code for expression / variable

    def __truediv__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Variable) or isinstance(other, Constant):
            self = self * (other ** Constant(-1, 1, 1))
            return self

        elif isinstance(other, Expression):
            expression = Expression()
            self.coefficient /= other.coefficient
            other.power *= -1
            expression.tokens = [self]
            expression.tokens.extend([Multiply(), other])
            self = expression
            return expression
