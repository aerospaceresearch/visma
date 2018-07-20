import math
import copy
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Operator, Binary

greek = [u'\u03B1', u'\u03B2', u'\u03B3']


class EquationCompatibility(object):

    def __init__(self, lTokens, rTokens):
        self.lTokens = lTokens
        self.lVariables = []
        self.lVariables.extend(getLevelVariables(self.lTokens))
        self.rTokens = rTokens
        self.rVariables = []
        self.rVariables.extend(getLevelVariables(self.rTokens))
        self.availableOperations = []
        if checkSolveFor(lTokens, rTokens):
            self.availableOperations.append('solve')
        self.availableOperations.extend(getOperationsEquation(self.lVariables, self.lTokens, self.rVariables, self.rTokens))
        # print self.availableOperations


class ExpressionCompatibility(object):
    """docstring for ExpressionCompatibility"""

    def __init__(self, tokens):
        super(ExpressionCompatibility, self).__init__()
        self.tokens = tokens
        self.variables = []
        self.variables.extend(getLevelVariables(self.tokens))
        self.availableOperations = getOperationsExpression(self.variables, self.tokens)


def isNumber(term):
    if isinstance(term, int) or isinstance(term, float):
        return True
    else:
        x = 0
        dot = 0
        if term[0] == '-':
            x += 1
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot != 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1
            if x >= 2:
                return True
            else:
                return False
        else:
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot != 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1
        return True


def isVariable(term):
    """
    Checks if given term is variable
    """
    if term in greek:
        return True
    elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
        x = 0
        while x < len(term):
            if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
                return False
            x += 1
        return True


def isEquation(lTokens, rTokens):
    if len(lTokens) > 0 and len(rTokens) == 1:
        if isinstance(rTokens[0], Constant):
            if rTokens[0].value == 0:
                return True
    return False


def findWRTVariable(lTokens, rTokens=None, variables=None):
    if rTokens is None:
        rTokens = []
    if variables is None:
        variables = []
    for token in lTokens:
        if isinstance(token, Variable):
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif isinstance(token, Expression):
            variables.extend(findWRTVariable(token.tokens))

    for token in rTokens:
        if isinstance(token, Variable):
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif isinstance(token, Expression):
            variables.extend(findWRTVariable(token.tokens, [], variables))
    return variables


def checkEquation(terms, symTokens):
    brackets = 0
    sqrBrackets = 0
    equators = 0
    for i, term in enumerate(terms):
        if term == '(':
            brackets += 1
        elif term == ')':
            brackets -= 1
            if brackets < 0:
                return False
        # TODO: logger.log("Too many ')'")
        elif term == '[':
            sqrBrackets += 1
        elif term == ']':
            sqrBrackets -= 1
            if sqrBrackets < 0:
                return False
        # TODO: logger.log("Too many ']'")
        elif term == '^':
            if symTokens[i + 1] == 'Binary':
                return False
        # TODO: logger.log("Check around '^'")
        elif isVariable(term) or isNumber(term):
            if i + 1 < len(terms):
                if terms[i + 1] == '(':
                    return False
        elif term == '>' or term == '<':
            if terms[i+1] != '=':
                equators += 1
            if equators > 1:
                return False
        elif term == '=':
            equators += 1
            if equators > 1:
                return False
        # TODO: logger.log("Inappropriate number of equator(=,<,>)")
        elif term == ';':
            equators = 0
    if len(terms) != 0:
        i = len(terms) - 1
        if symTokens[i] == 'Binary' or symTokens[i] == 'Unary' or brackets != 0 or sqrBrackets != 0:
            return False
    return True


def checkTypes(lTokens=None, rTokens=None):

    if lTokens is None:
        lTokens = []
    if rTokens is None:
        rTokens = []

    if len(rTokens) != 0:
        equationCompatible = EquationCompatibility(lTokens, rTokens)
        availableOperations = equationCompatible.availableOperations
        isPoly, polyDegree = preprocessCheckPolynomial(copy.deepcopy(lTokens), copy.deepcopy(rTokens))
        if isPoly:
            availableOperations.append('factorize')
            if(polyDegree == 2):
                availableOperations.append("find roots")
        inputType = "equation"
    else:
        expressionCompatible = ExpressionCompatibility(lTokens)
        availableOperations = expressionCompatible.availableOperations
        isPoly, polyDegree = preprocessCheckPolynomial(copy.deepcopy(lTokens), copy.deepcopy(rTokens))
        if isPoly:
            availableOperations.append('factorize')
        availableOperations.append("integrate")
        availableOperations.append("differentiate")
        inputType = "expression"

    return availableOperations, inputType


def checkSolveFor(lTokens, rTokens):
    for token in lTokens:
        if isinstance(token, Variable):
            return True
        elif isinstance(token, Expression):
            if checkSolveFor(token.tokens, []):
                return True

    for token in rTokens:
        if isinstance(token, Variable):
            return True
        elif isinstance(token, Expression):
            if checkSolveFor([], token.tokens):
                return True


def getNumber(term):
    return float(term)


def getLevelVariables(tokens):
    variables = []
    for i, term in enumerate(tokens):
        if isinstance(term, Variable):
            skip = False
            for var in variables:
                if var.value == term.value and var.power[0] == term.power:
                    var.power.append(term.power)
                    var.scope.append(term.scope)
                    var.coefficient.append(term.coefficient)
                    if i != 0 and isinstance(tokens[i - 1], Binary):
                        var.before.append(tokens[i - 1].value)
                        var.beforeScope.append(tokens[i - 1].scope)
                    else:
                        var.before.append('')
                        var.beforeScope.append('')
                    if i + 1 < len(tokens) and isinstance(tokens[i + 1], Binary):
                        var.after.append(tokens[i + 1].value)
                        var.afterScope.append(tokens[i + 1].scope)
                    else:
                        var.after.append('')
                        var.afterScope.append('')
                    skip = True
                    break
            if not skip:
                variable = Variable()
                variable.value = term.value
                variable.scope = [term.scope]
                variable.power = []
                variable.coefficient = []
                variable.before = []
                variable.beforeScope = []
                variable.after = []
                variable.afterScope = []
                variable.power.append(term.power)
                variable.coefficient.append(term.coefficient)
                if i != 0 and isinstance(tokens[i - 1], Binary):
                    variable.before.append(tokens[i - 1].value)
                    variable.beforeScope.append(tokens[i - 1].scope)
                else:
                    variable.before.append('')
                    variable.beforeScope.append('')
                if i + 1 < len(tokens) and isinstance(tokens[i + 1], Binary):
                    variable.after.append(tokens[i + 1].value)
                    variable.afterScope.append(tokens[i + 1].scope)
                else:
                    variable.after.append('')
                    variable.afterScope.append('')
                variables.append(variable)
        elif isinstance(term, Constant):
            skip = False
            for var in variables:
                if isinstance(var.value, list) and isNumber(var.value[0]):
                    if isinstance(term.value, list):
                        term.value = evaluateConstant(term)
                        term.power = 1
                    if var.power[0] == term.power:
                        var.value.append(term.value)
                        var.power.append(term.power)
                        var.scope.append(term.scope)
                        if i != 0 and isinstance(tokens[i - 1], Binary):
                            var.before.append(tokens[i - 1].value)
                            var.beforeScope.append(tokens[i - 1].scope)
                        else:
                            var.before.append('')
                            var.beforeScope.append('')
                        if i + 1 < len(tokens) and isinstance(tokens[i + 1], Binary):
                            var.after.append(tokens[i + 1].value)
                            var.afterScope.append(tokens[i + 1].scope)
                        else:
                            var.after.append('')
                            var.afterScope.append('')
                        skip = True
                        break
            if not skip:
                variable = Constant()
                variable.power = []
                if isinstance(term.value, list):
                    variable.value = [evaluateConstant(term)]
                    variable.power.append(1)
                else:
                    variable.value = [term.value]
                    variable.power.append(term.power)
                variable.scope = [term.scope]
                variable.before = []
                variable.beforeScope = []
                variable.after = []
                variable.afterScope = []
                if i != 0 and isinstance(tokens[i - 1], Binary):
                    variable.before.append(tokens[i - 1].value)
                    variable.beforeScope.append(tokens[i - 1].scope)
                else:
                    variable.before.append('')
                    variable.beforeScope.append('')
                if i + 1 < len(tokens) and isinstance(tokens[i + 1], Binary):
                    variable.after.append(tokens[i + 1].value)
                    variable.afterScope.append(tokens[i + 1].scope)
                else:
                    variable.after.append('')
                    variable.afterScope.append('')
                variables.append(variable)
        elif isinstance(term, Expression):
            var = getLevelVariables(term.tokens)
            retType, val = extractExpression(var)
            if retType == "expression":
                variable = Expression()
                variable.value = val
                variable.tokens = term.tokens
                variables.append(variable)
            elif retType == "constant":
                skip = False
                for var in variables:
                    if isinstance(var.value, list) and isNumber(var.value[0]):
                        if var.power == val.power:
                            var.value.append(val.value)
                            var.power.append(val.power)
                            var.scope.append(val.scope)
                            var.before.append(val.before)
                            var.beforeScope.append(val.beforeScope)
                            var.after.append(val.after)
                            var.afterScope.append(val.afterScope)
                            skip = True
                            break
                if not skip:
                    var = Constant()
                    var.value = [val.value]
                    var.power = [val.power]
                    var.scope = [val.scope]
                    var.before = [val.before]
                    var.beforeScope = [val.beforeScope]
                    var.after = []
                    var.afterScope = ['']
                    variables.append(var)
            elif retType == Variable:
                skip = False
                for var in variables:
                    if var.value == val.value:
                        var.power.append(val.power)
                        var.before.append('')
                        var.beforeScope.append('')
                        var.after.append('')
                        var.afterScope.append('')
                        var.coefficient.append(val.coefficient)
                        var.scope.append(val.scope)
                        skip = True
                        break
                if not skip:
                    var = Constant()
                    var.coefficient = [val.coefficient]
                    var.value = val.value
                    var.power = [val.power]
                    var.scope = [val.scope]
                    var.before = ['']
                    var.beforeScope = ['']
                    var.after = ['']
                    var.afterScope = ['']
                    variables.append(var)
            elif retType == "mixed":
                for v in val:
                    if isinstance(v, Variable):
                        skip = False
                        for var in variables:
                            if var.value == v.value:
                                var.power.extend(v.power)
                                var.before.extend(v.before)
                                var.beforeScope.extend(v.beforeScope)
                                var.after.extend(v.after)
                                var.afterScope.extend(v.afterScope)
                                var.coefficient.extend(v.coefficient)
                                var.scope.extend(v.scope)
                                skip = True
                                break
                        if not skip:
                            var = Constant()
                            var.coefficient = [v.coefficient]
                            var.value = v.value
                            var.power = [v.power]
                            var.scope = [v.scope]
                            var.before = [v.before]
                            var.beforeScope = [v.beforeScope]
                            var.after = [v.after]
                            var.afterScope = [v.afterScope]
                            variables.append(var)
                    elif isinstance(v, Constant):
                        for var in variables:
                            if isinstance(var.value, list) and isNumber(var.value[0]):
                                if var.power == v.power:
                                    var.value.extend(v.value)
                                    var.power.extend(v.power)
                                    var.before.extend(v.before)
                                    var.beforeScope.extend(
                                        v.beforeScope)
                                    var.after.extend(v.after)
                                    var.afterScope.extend(v.afterScope)
                                    var.coefficient.extend(v.coefficient)
                                    var.scope.extend(v.scope)
                                    skip = True
                                    break
                        if not skip:
                            var = Constant()
                            var.coefficient = [v.coefficient]
                            var.value = [v.value]
                            var.power = [v.power]
                            var.scope = [v.scope]
                            var.before = [v.before]
                            var.beforeScope = [v.beforeScope]
                            var.after = [v.after]
                            var.afterScope = [v.afterScope]
                            variables.append(var)
                    elif isinstance(v, Expression):
                        variables.append(v)

    return variables


def getOperationsEquation(lVariables, lTokens, rVariables, rTokens):
    operations = []
    for i, token in enumerate(lTokens):
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                prev = False
                nxt = False
                if i != 0:
                    if lTokens[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(lTokens):
                    if lTokens[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if nxt and prev:
                    op = token.value
                    if op not in operations:
                        operations.append(op)

    for i, token in enumerate(rTokens):
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                prev = False
                nxt = False
                if i != 0:
                    if rTokens[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(rTokens):
                    if rTokens[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if nxt and prev:
                    op = token.value
                    if op not in operations:
                        operations.append(op)

    for i, variable in enumerate(lVariables):
        if isinstance(variable, Constant):
            rCount = 0
            for variable2 in rVariables:
                if isinstance(variable2, Constant):
                    if variable2.power[0] == variable.power[0]:
                        rCount += len(variable2.value)
                        break
            count = 0
            opCount = 0
            ops = []

            if len(variable.value) > 1:
                for j in xrange(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        opCount += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-', '']:
                        count += 1
            else:
                if variable.after[0] in ['+', '-', ''] and variable.before[0] in ['+', '-', '']:
                    count += 1

            if (len(variable.value) > 0 and rCount > 0):
                for variable2 in rVariables:
                    if isinstance(variable2, Constant):
                        for l in xrange(len(variable2.value)):
                            if variable2.after[l] in ['+', '-', ''] and variable2.before[l] in ['+', '-', ''] and variable2.value[l] != 0:
                                count += 1
                                opCount += 1
                                tempOp = '+'
                                if variable2.before[l] == '+' or (variable2.before[l] == '' and getNumber(variable2.value[l]) > 0):
                                    tempOp = '-'
                                else:
                                    tempOp = '+'
                                if not (tempOp in ops):
                                    ops.append(tempOp)

            if count > 1 and opCount > 0:
                for op in ops:
                    if op not in operations:
                        operations.append(op)

        elif isinstance(variable, Variable):
            rCount = 0
            for variable2 in rVariables:
                if isinstance(variable2, Variable):
                    if variable2.value == variable.value:
                        if variable2.power[0] == variable.power[0]:
                            rCount += len(variable2.value)
                            break
            count = 0
            ops = []
            power = []
            opCount = 0
            if len(variable.power) > 1:
                for j in xrange(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        opCount += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                            power.append(variable.power[j])
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-', '']:
                        count += 1
            else:
                if variable.after[0] in ['+', '-', ''] and variable.before[0] in ['+', '-', '']:
                    count += 1

            if len(variable.power) > 0 and rCount > 0:
                for variable2 in rVariables:
                    if isinstance(variable2, Variable):
                        if variable2.value == variable.value and variable2.power[0] == variable.power[0]:
                            for l in xrange(len(variable2.power)):
                                if variable2.after[l] in ['+', '-', ''] and variable2.before[l] in ['+', '-', '']:
                                    count += 1
                                    opCount += 1
                                    tempOp = '+'
                                    if variable2.before[l] == '+' or variable2.before[l] == '':
                                        tempOp = '-'
                                    else:
                                        tempOp = '+'
                                    if not (tempOp in ops):
                                        ops.append(tempOp)
                                        power.append(variable2.power[l])

            if count > 1 and opCount > 0:
                for i, op in enumerate(ops):
                    if not (op in operations):
                        operations.append(op)

        elif isinstance(variable, Expression):
            ops = getOperationsExpression(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)

    for i, variable in enumerate(rVariables):
        if isinstance(variable, Constant):
            if len(variable.value) > 1:
                count = 0
                ops = []
                for j in xrange(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                if count > 1:
                    for op in ops:
                        if op not in operations:
                            operations.append(op)
        elif isinstance(variable, Variable):
            if len(variable.power) > 1:
                count = 0
                ops = []
                power = []
                opCount = 0
                for j in xrange(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        opCount += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                            power.append(variable.power[j])
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-', '']:
                        count += 1

                if count > 1 and opCount > 0:
                    for i, op in enumerate(ops):
                        if not (op in operations):
                            operations.append(op)

        elif isinstance(variable, Expression):
            ops = getOperationsExpression(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)

    return operations


def getOperationsExpression(variables, tokens):
    operations = []
    for i, token in enumerate(tokens):
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                prev = False
                nxt = False
                if i != 0:
                    if tokens[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(tokens):
                    if tokens[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if nxt and prev:
                    op = token.value
                    if op not in operations:
                        operations.append(op)
    for i, variable in enumerate(variables):
        if isinstance(variable, Constant):
            if len(variable.value) > 1:
                count = 0
                opCount = 0
                ops = []
                for j in xrange(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        opCount += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-', '']:
                        count += 1

                if count > 1:
                    for op in ops:
                        if op not in operations:
                            operations.append(op)
        elif isinstance(variable, Variable):
            if len(variable.power) > 1:
                count = 0
                ops = []
                power = []
                opCount = 0
                for j in xrange(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-']:
                        count += 1
                        opCount += 1
                        if not (variable.before[j] in ops):
                            ops.append(variable.before[j])
                            power.append(variable.power[j])
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+', '-', '']:
                        count += 1
                if count > 1 and opCount > 0:
                    for i, op in enumerate(ops):
                        if not (op in operations):
                            operations.append(op)
        elif isinstance(variable, Expression):
            ops = getOperationsExpression(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)
    return operations


def extractExpression(variable):
    if len(variable) == 1:
        if isinstance(variable[0], Expression):
            _, variable = extractExpression(variable[0].value)
        elif isinstance(variable[0], Constant):
            return "constant", variable[0]
        elif isinstance(variable[0], Variable):
            return "variable", variable[0]
    else:
        if not evaluateExpressions(variable):
            return "expression", getLevelVariables(variable)
        else:
            return "mixed", getLevelVariables(variable)


def evaluateConstant(constant):
    if isinstance(constant, Function):
        if isNumber(constant.value):
            return math.pow(constant.value, constant.power)
        elif isinstance(constant.value, list):
            val = 1
            if constant.coefficient is not None:
                val *= constant.coefficient
            for i, c_val in enumerate(constant.value):
                val *= math.pow(c_val, constant.power[i])
            return val
    elif isNumber(constant):
        return constant


def evaluateExpressions(variables):
    var = []
    varPowers = []
    for i, variable in enumerate(variables):
        if isinstance(variable, Expression):
            if evaluateExpressions(variable.tokens):
                return False
        elif isinstance(variable, Variable):
            prev = False
            nxt = False
            if i != 0:
                if isinstance(variables[i - 1], Binary):
                    if variables[i - 1].value in ['-', '+']:
                        prev = True
                else:
                    print(variables[i - 1])
            else:
                prev = True

            if i + 1 < len(variables):
                if isinstance(variables[i + 1], Binary):
                    if variables[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    print(variables[i + 1])
            else:
                nxt = True
            if nxt and prev:
                match = False
                for i, v in enumerate(var):
                    if variable.value == v:
                        for p in varPowers[i]:
                            if variable.power == p:
                                return False
                        varPowers[i].append(variable.power)
                        match = True
                        break
                if not match:
                    var.append(variable.value)
                    varPowers.append([variable.power])
        elif isinstance(variable, Constant):
            prev = False
            nxt = False
            if i != 0:
                if isinstance(variables[i - 1], Binary):
                    if variables[i - 1].value in ['-', '+']:
                        prev = True
                else:
                    print(variables[i - 1])
            else:
                prev = True

            if i + 1 < len(variable):
                if isinstance(variables[i + 1], Binary):
                    if variables[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    print(variables[i + 1])
            else:
                nxt = True
            if nxt and prev:
                match = False
                for i, v in enumerate(var):
                    if isinstance(v.value, list) and isNumber(v.value[0]):
                        for p in varPowers[i]:
                            if variable.power == p:
                                return False
                        varPowers[i].append(variable.power)
                        match = True
                        break
                if not match:
                    var.append([variable.value])
                    varPowers.append([variable.power])
    for i, variable in enumerate(variables):
        if isinstance(variable, Binary):
            prev = False
            nxt = False
            if variable.value in ['*', '/']:
                if i != 0:
                    if variables[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(variables):
                    if variables[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if prev and nxt:
                    return False
    return True


def availableVariables(tokens):
    variables = []
    for token in tokens:
        if isinstance(token, Variable):
            for val in token.value:
                if val not in variables:
                    variables.append(val)
    return variables


def highestPower(tokens, variable):
    maxPow = 0
    for token in tokens:
        if isinstance(token, Variable):
            for i, val in enumerate(token.value):
                if val == variable and token.power[i] > maxPow:
                        maxPow = token.power[i]
    return maxPow


def isIntegerPower(tokens, variable):
    for token in tokens:
        if isinstance(token, Variable):
            for i, val in enumerate(token.value):
                if val == variable and token.power[i] != int(token.power[i]):
                    return False
    return True


def preprocessCheckPolynomial(lTokens, rTokens):
    from visma.simplify.simplify import simplifyEquation  # Circular import
    lTokens, rTokens, _, _, _, _ = simplifyEquation(lTokens, rTokens)
    lVariables = availableVariables(lTokens)
    rVariables = availableVariables(rTokens)
    for token in lTokens:
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                return False, -1
    for token in rTokens:
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                return False, -1
    # OPTIMIZE
    if len(lVariables) == 1 and len(rVariables) == 1:
        if isIntegerPower(lTokens, lVariables[0]) and isIntegerPower(rTokens, rVariables[0]):
            if lVariables[0] == rVariables[0]:
                return True, max(highestPower(lTokens, lVariables[0]), highestPower(rTokens, rVariables[0]))
    elif len(lVariables) == 1 and len(rVariables) == 0:
        if isIntegerPower(lTokens, lVariables[0]):
            return True, highestPower(lTokens, lVariables[0])
    elif len(lVariables) == 0 and len(rVariables) == 1:
        if isIntegerPower(rTokens, rVariables[0]):
            return True, highestPower(lTokens, lVariables[0])
    return False, -1


def commonAttributes(tok1, tok2):
    commAttr = {}
    commAttr['Type'] = commAttr['Coeff'] = commAttr['Value'] = commAttr['Power'] = commAttr['Operand'] = False
    commAttr['Type'] = (tok1.__class__ == tok2.__class__)
    if commAttr['Type']:
        if isinstance(tok1, Function) and isinstance(tok2, Function):
            commAttr['Coeff'] = (tok1.coefficient == tok2.coefficient)
            if isinstance(tok1.value, list) and isinstance(tok2.value, list):
                tok1.value = [val for val, pow in sorted(zip(tok1.value, tok1.power))]
                tok1.power = [pow for val, pow in sorted(zip(tok1.value, tok1.power))]
                tok2.value = [val for val, pow in sorted(zip(tok2.value, tok2.power))]
                tok2.power = [pow for val, pow in sorted(zip(tok2.value, tok2.power))]
            commAttr['Value'] = (tok1.value == tok2.value)
            commAttr['Power'] = (tok1.power == tok2.power)
            operand1 = copy.deepcopy(tok1.operand)
            operand2 = copy.deepcopy(tok2.operand)
            if operand1 is None and operand2 is None:
                commAttr['Operand'] = True
            else:
                # FIXME: Add test for operand in test_io.py
                while operand1 is not None and operand2 is not None:
                    commAttr['Operand'] = (operand1 == operand2)
                    operand1 = operand1.operand
                    operand2 = operand2.operand

    elif isinstance(tok1, Operator) and isinstance(tok2, Operator):
        commAttr['Type'] = commAttr['Coeff'] = commAttr['Value'] = commAttr['Power'] = commAttr['Operand'] = True
        commAttr['Value'] = (tok1.value == tok2.value)
    return commAttr


def areTokensEqual(tok1, tok2):
    commAttr = commonAttributes(tok1, tok2)
    for attr in commAttr:
        if commAttr[attr] is False:
            return False
    return True


def isTokenInToken(tokA, tokB):
    if isinstance(tokA, Variable) and isinstance(tokB, Variable):
        varA = findWRTVariable([tokA])
        varB = findWRTVariable([tokB])
        if all(var in varB for var in varA):
            ratios = []
            for iA, valA in enumerate(tokA.value):
                for iB, valB in enumerate(tokB.value):
                    if valA == valB:
                        ratios.append(tokA.power[iA]/tokB.power[iB])
                        break
            if all(ratio == ratios[0] for ratio in ratios):
                return True
            else:
                return False
        else:
            return False
    elif isinstance(tokA, Variable) and isinstance(tokB, Expression):
        for token in tokB.tokens:
            if isinstance(token, Variable) or isinstance(token, Expression):
                if isTokenInToken(tokA, token) is True:
                    return True
        return False
    else:
        return False


def isTokenInList(token, tokList):
    for tok in tokList:
        if isTokenInToken(token, tok) is True:
            return True
    return False
