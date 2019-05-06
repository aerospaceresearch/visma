from visma.functions.structure import Function, Expression
from visma.functions.exponential import Logarithm
from visma.functions.operator import Plus, Minus, Multiply, Divide

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
        self.type = 'Variable'

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

    def differentiate(self):
        from visma.functions.constant import Constant
        super().differentiate()
        self.value = 1
        self.__class__ = Constant

    def integrate(self, wrtVar):
        if wrtVar not in self.value:
            self.value.append(wrtVar)
            self.power.append(1)
        else:
            for i, val in enumerate(self.value):
                if val == 'wrtVar':
                    break
            if self.power[i] == -1:
                self.power.pop(i)
                self.value.pop(i)
                expression = Expression()
                expression.tokens = [self]
                variable = Variable(1, 'wrtVar', 1)
                expression.tokens.append(Logarithm(variable))
                self.__class__ = Expression
                self = expression
            else:
                self.coefficient /= self.power[i] + 1
                self.power[i] += 1

    def calculate(self, val):
        return self.coefficient * ((val**(self.power)))

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend([Plus(), other])
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Variable):
                    if token.power == self.power:
                        self.coefficient += other.tokens[i].coefficient
                    else:
                        expression.tokens.extend([Plus(), Variable(token)])
                elif isinstance(token, Constant):
                    expression.tokens.extend([Plus(), Constant(token.calculate()*1)])
            expression.tokens[0] = self
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            if other.power == self.power:
                self.coefficient += other.coefficient
                return self
            else:
                expression = Expression()
                expression.tokens = [self]
                expression.tokens.extend([Plus(), other])
                self.type = 'Expression'
                self = expression
                return expression

    def __rsub__(self, other):
        expression = Expression()
        expression.tokens = [other]
        expression.tokens.extend([Minus(), self])
        self.type = 'Expression'
        self = expression
        return expression

    def __sub__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            expression = Expression()
            expression.tokens = [self]
            expression.tokens.extend([Minus(), other])
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Expression):
            expression = Expression()
            expression.tokens = [self]
            for i, token in enumerate(other.tokens):
                if isinstance(token, Variable):
                    if token.power == self.power:
                        self.coefficient -= other.tokens[i].coefficient
                    else:
                        expression.tokens.extend([Minus(), Variable(token)])
                elif isinstance(token, Constant):
                    expression.tokens.extend([Minus(), Constant(token.calculate())])
            expression.tokens[0] = self
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            if other.power == self.power:
                self.coefficient -= other.coefficient
                return self
            else:
                expression = Expression()
                expression.tokens = [self]
                expression.tokens.extend([Minus(), other])
                self.type = 'Expression'
                self = expression
                return expression

    def __rmul__(self, other):
        return self * other

    def __mul__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self.coefficient *= other.calculate()
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            expression.coefficient = self.coefficient * other.coefficient
            for i, token in enumerate(other.tokens):
                if isinstance(token, Variable) or isinstance(token, Constant):
                    expression.tokens.extend([self * token])
                else:
                    expression.tokens.extend([token])
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            variable = Variable()
            variable.value.extend(self.value)
            variable.power.extend(self.power)
            variable.coefficient = self.coefficient * other.coefficient
            for i, val in enumerate(other.value):
                if val in variable.value:
                    variable.power[i] += other.power[i]
                else:
                    variable.value.extend(val)
                    variable.power.extend([other.power[i]])
            self = variable
            return variable

    def __rtruediv__(self, other):
        pass                                    # TODO : Add code for expression / variable

    def __truediv__(self, other):
        from visma.functions.constant import Constant
        if isinstance(other, Constant):
            self.coefficient /= other.calculate()
            return self
        elif isinstance(other, Expression):
            expression = Expression()
            self.coefficient /= other.coefficient
            other.power *= -1
            expression.tokens = [self]
            expression.tokens.extend([Multiply(), other])
            self.type = 'Expression'
            self = expression
            return expression
        elif isinstance(other, Variable):
            variable = Variable()
            variable.value.extend(self.value)
            variable.power.extend(self.power)
            variable.coefficient = self.coefficient / other.coefficient
            for i, val in enumerate(other.value):
                if val in variable.value:
                    variable.power[i] -= other.power[i]
                else:
                    variable.value.extend(val)
                    variable.power.extend([-1*other.power[i]])
            self = variable
            return variable
