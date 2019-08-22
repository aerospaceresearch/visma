import math
import copy
from visma.config.values import ROUNDOFF
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Operator, Binary


greek = [u'\u03B1', u'\u03B2', u'\u03B3']

funcs = ['log', 'log_', 'ln', 'exp', 'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']
funcSyms = ['Log', 'LogB', 'LogN', 'Exp', 'Sin', 'Cos', 'Tan', 'Csc', 'Sec', 'Cot', 'Asin', 'Acos', 'Atan', 'Sinh', 'Cosh', 'Tanh', 'Asinh', 'Acosh', 'Atanh']


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
        # print(self.availableOperations)


class ExpressionCompatibility(object):

    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens
        self.variables = []
        self.variables.extend(getLevelVariables(self.tokens))
        self.availableOperations = getOperationsExpression(self.variables, self.tokens)


def isFloat(val):

    try:
        float(val)
        return True
    except ValueError:
        return False


def isInt(val):

    try:
        int(val)
        return True
    except ValueError:
        return False


def isNumber(term):

    if isInt(term) or isFloat(term):
        return True
    else:
        return False


def isVariable(term):

    if term in greek:
        return True
    elif ('a' <= term[0] <= 'z') or ('A' <= term[0] <= 'Z'):
        x = 0
        while x < len(term):
            if term[x] < 'A' or ('Z' < term[x] < 'a') or term[x] > 'z':
                return False
            x += 1
        return True


def isFunction(term):

    if term in funcs:
        return True
    return False


def isEquation(lTokens, rTokens):

    if len(lTokens) > 0 and len(rTokens) == 1:
        if isinstance(rTokens[0], Constant):
            if rTokens[0].value == 0:
                return True
    return False


def getVariables(lTokens, rTokens=None, variables=None):
    """Finds all the variables present in the expression

    Arguments:
        lTokens {list} -- list of function tokens

    Keyword Arguments:
        rTokens {list} -- list of function tokens (default: {None})
        variables {list} -- list of variables (default: {None})

    Returns:
        variables {list} -- list of variables
    """
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
            variables.extend(getVariables(token.tokens))

    for token in rTokens:
        if isinstance(token, Variable):
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif isinstance(token, Expression):
            variables.extend(getVariables(token.tokens, [], variables))
    return variables


def getVariableSim(eqnTokens):
    from visma.io.tokenize import getLHSandRHS

    variables = []
    for _, tokens in enumerate(eqnTokens):
        lTokens, rTokens = getLHSandRHS(tokens)
        variablesEach = getVariables(lTokens, rTokens)
        variables.extend(variablesEach)
    variables = list(dict.fromkeys(variables))
    variables.sort()    # List of all the variables in all 3 equation in sorted order
    return variables


def checkEquation(terms, symTokens):
    """Checks if input is a valid expression or equation

    Arguments:
        terms {list} -- list of input terms
        symTokens {list} -- list of symbol tokens

    Returns:
        bool -- if valid or not
        log {string} -- error message if bool is False
    """
    brackets = 0
    sqrBrackets = 0
    equators = 0
    terminalLatex = 0
    for i, term in enumerate(terms):
        if term == '(':
            brackets += 1
        elif term == ')':
            brackets -= 1
        elif term == '[':
            sqrBrackets += 1
        elif term == ']':
            sqrBrackets -= 1
        elif term == '^':
            if i + 1 < len(terms):
                if symTokens[i + 1] == 'Binary':
                    log = "Check around '^'"
                    return False, log
            else:
                log = "Missing exponent after '^'"
                return False, log
        elif isFunction(term):
            if i + 1 < len(terms):
                if terms[i + 1] != '(':
                    log = "Use parenthesis to contain the function"
                    return False, log
        elif isVariable(term) or isNumber(term):
            if i + 1 < len(terms):
                if terms[i + 1] == '(':
                    log = "Invalid expression"
                    return False, log
        if not isNumber(term):
            x = 0
            dot = 0
            while x < len(term):
                if str(term[x]) == '.':
                    dot += 1
                    if dot > 1:
                        log = "Remove Multiple decimal points."
                        return False, log
                x += 1
        elif term == '>' or term == '<':
            if i + 1 < len(terms):
                if terms[i+1] != '=':
                    equators += 1
        elif term == '=':
            equators += 1
        elif term == ';':
            equators = 0
        elif term == '$':
            terminalLatex = 1 - terminalLatex

    if brackets < 0:
        log = "Too many ')'"
        return False, log
    elif brackets > 0:
        log = "Too many '('"
        return False, log
    if sqrBrackets < 0:
        log = "Too many ']'"
        return False, log
    elif sqrBrackets > 0:
        log = "Too many '['"
        return False, log
    if equators > 1:
        log = "Inappropriate number of equators(=,<,>)"
        return False, log
    if len(terms) != 0:
        i = len(terms) - 1
        if symTokens[i] == 'Binary' or symTokens[i] == 'Unary' or brackets != 0 or sqrBrackets != 0:
            log = "Invalid expression"
            return False, log
    if terminalLatex == 1:
        log = "LaTeX detected: Missing ending $"
        return False, log
    return True


def checkTypes(lTokens=None, rTokens=None):
    """Checks input type and available operations

    Keyword Arguments:
        lTokens {list} -- list of function tokens (default: {None})
        rTokens {list} -- list of function tokens (default: {None})

    Returns:
        availableOperations {list} -- list of operations
        inputType {string} -- function tokens' type
    """

    if lTokens is None:
        lTokens = []
    if rTokens is None:
        rTokens = []

    # Temporary solution to handle Expressions until tokezizing modules are made expression friendly.
    expressionPresent = False
    for x in lTokens:
        if isinstance(x, Expression):
            expressionPresent = True
            break
    for x in rTokens:
        if isinstance(x, Expression):
            expressionPresent = True
            break
    if expressionPresent:
        if len(rTokens) == 0:
            return ['integrate', 'differentiate'], 'expression'
        else:
            return ['integrate', 'differentiate'], 'equation'

    if len(rTokens) != 0:
        equationCompatible = EquationCompatibility(lTokens, rTokens)
        availableOperations = equationCompatible.availableOperations
        isPoly, polyDegree = preprocessCheckPolynomial(copy.deepcopy(lTokens), copy.deepcopy(rTokens))
        if isPoly:
            availableOperations.append('factorize')
            if (polyDegree == 2 or polyDegree == 3 or polyDegree == 4):
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
        availableOperations.append("factorial")
        inputType = "expression"

    return availableOperations, inputType


def checkSolveFor(lTokens, rTokens):
    """Checks if there exists any variable so that solve can be called

    Arguments:
        lTokens {list} -- list of function tokens
        rTokens {list} -- list of function tokens

    Returns:
        bool -- if 'solve' possible or not
    """
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


def getNumber(term, rod=ROUNDOFF):
    """Converts string to float

    Arguments:
        term {string} -- number of type string

    Keyword Arguments:
        rod {int} -- number of decimal places to roundoff (default: ROUNDOFF {int})

    Returns:
        term {float} -- number of type float
    """
    term = round(float(term), rod)

    return term


def getLevelVariables(tokens):
    """Returns tokens of Function class from a list of function tokens

    Arguments:
        tokens {list} -- list of function tokens

    Returns:
        variables {list} -- list of tokens of Function class(Variable/Constant)
    """
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
            elif retType == "variable":
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
    """Returns a list of operations which can be performed on given equation tokens

    Arguments:
        lVariables {list} -- list of Function(Variable/Constant) tokens
        lTokens {list} -- list of function tokens
        rVariables {list} -- list of Function(Variable/Constant) tokens
        rTokens {list} -- list of function tokens

    Returns:
        operations {list} -- list of operations which can be performed
    """
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
                for j in range(len(variable.value)):
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
                        for l in range(len(variable2.value)):
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
                for j in range(len(variable.power)):
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
                            for l in range(len(variable2.power)):
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
                for j in range(len(variable.value)):
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
                for j in range(len(variable.power)):
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
    """[Returns a list of operations which can be performed on given equation tokens

    Arguments:
        variables {list} -- list of Function(Variable/Constant) tokens
        tokens {list} -- list of function tokens

    Returns:
        operations {list} -- list of operations which can be performed
    """
    operations = []
    for i, token in enumerate(tokens):
        if isinstance(token, Binary):
            if token.value in ['*', '/']:
                prev = False
                nxt = False
                if i != 0:
                    if isinstance(tokens[i - 1], Function):
                        prev = True
                if i + 1 < len(tokens):
                    if isinstance(tokens[i + 1], Variable) or isinstance(tokens[i + 1], Constant) or isinstance(tokens[i - 1], Expression):
                        nxt = True
                if nxt and prev:
                    op = token.value
                    if op not in operations:
                        operations.append(op)
        elif isinstance(token, Expression):
            ops = getOperationsExpression([], token.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)
    for i, variable in enumerate(variables):
        if isinstance(variable, Constant):
            if len(variable.value) > 1:
                count = 0
                opCount = 0
                ops = []
                for j in range(len(variable.value)):
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
                for j in range(len(variable.power)):
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
            ops = getOperationsExpression(variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)
    return operations


def extractExpression(variable):
    """Get function tokens from tokens property of an expression

    Arguments:
        string -- token type
        visma.functions.structure.Function/list -- function token/s
    """
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
    """Returns constant value for a given visma.functions.Function or constant term

    Arguments:
        constant {visma.functions.Function/string} -- input term

    Returns:
       constant value -- value of input term
    """
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
                    pass
                    # print(variables[i - 1])
            else:
                prev = True

            if i + 1 < len(variables):
                if isinstance(variables[i + 1], Binary):
                    if variables[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    pass
                    # print(variables[i + 1])
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
                    pass
                    # print(variables[i - 1])
            else:
                prev = True

            if i + 1 < len(variables):
                if isinstance(variables[i + 1], Binary):
                    if variables[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    pass
                    # print(variables[i + 1])
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


def highestPower(tokens, variable):
    """Returns the highest power of given variable value among given tokens list

    Arguments:
        tokens {list} -- list of function tokens
        variable {string} -- variable value

    Returns:
        maxPow {int} -- highest power of given variable
    """
    maxPow = 0
    for token in tokens:
        if isinstance(token, Variable):
            for i, val in enumerate(token.value):
                if val == variable and token.power[i] > maxPow:
                    maxPow = token.power[i]
    return maxPow


def isIntegerPower(tokens, variable):
    """Checks if given variable has integer powers

    Arguments:
        tokens {list} -- list of function tokens
        variable {string} -- variable value

    Returns:
        bool -- if variable has integer powers or not
    """
    for token in tokens:
        if isinstance(token, Variable):
            for i, val in enumerate(token.value):
                if val == variable and token.power[i] != int(token.power[i]):
                    return False
    return True


def preprocessCheckPolynomial(lTokens, rTokens):
    """Checks if given equation is a polynomial and returns degree

    Arguments:
        lTokens {list} -- list of function tokens
        rTokens {list} -- list of function tokens

    Returns:
        bool -- if polynomial or not
        int -- degree of polynomial (-1 if bool is False)
    """
    from visma.simplify.simplify import simplifyEquation  # Circular import
    lTokens, rTokens, _, _, _, _ = simplifyEquation(lTokens, rTokens)
    lVariables = getVariables(lTokens)
    rVariables = getVariables(rTokens)
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


def commonAttributes(tokA, tokB):
    """Gets the common attributes between two given tokens

    Arguments:
        tokA {visma.functions.structure.Function} -- function token
        tokB {visma.functions.structure.Function} -- function token

    Returns:
        commAttr {dict} -- A dict of attributes where the property is given by key
    """
    commAttr = {}
    commAttr['Type'] = commAttr['Coeff'] = commAttr['Value'] = commAttr['Power'] = commAttr['Operand'] = False
    commAttr['Type'] = (tokA.__class__ == tokB.__class__)
    if commAttr['Type']:
        if isinstance(tokA, Function) and isinstance(tokB, Function):
            commAttr['Coeff'] = (tokA.coefficient == tokB.coefficient)
            if isinstance(tokA.value, list) and isinstance(tokB.value, list):
                tokA.value = [val for val, pow in sorted(zip(tokA.value, tokA.power))]
                tokA.power = [pow for val, pow in sorted(zip(tokA.value, tokA.power))]
                tokB.value = [val for val, pow in sorted(zip(tokB.value, tokB.power))]
                tokB.power = [pow for val, pow in sorted(zip(tokB.value, tokB.power))]
            commAttr['Value'] = (tokA.value == tokB.value)
            commAttr['Power'] = (tokA.power == tokB.power)
            operand1 = copy.deepcopy(tokA.operand)
            operand2 = copy.deepcopy(tokB.operand)
            if operand1 is None and operand2 is None:
                commAttr['Operand'] = True
            else:
                # FIXME: Add test for operand in test_io.py
                while operand1 is not None and operand2 is not None:
                    commAttr['Operand'] = (operand1 == operand2)
                    operand1 = operand1.operand
                    operand2 = operand2.operand

    elif isinstance(tokA, Operator) and isinstance(tokB, Operator):
        commAttr['Type'] = commAttr['Coeff'] = commAttr['Value'] = commAttr['Power'] = commAttr['Operand'] = True
        commAttr['Value'] = (tokA.value == tokB.value)
    return commAttr


def areTokensEqual(tokA, tokB):
    """Checks if given tokens are equal

    Arguments:
        tokA {visma.functions.structure.Function} -- function token
        tokB {visma.functions.structure.Function} -- function token

    Returns:
        bool -- if given tokens are equal or not
    """
    commAttr = commonAttributes(tokA, tokB)
    for attr in commAttr:
        if commAttr[attr] is False:
            return False
    return True


def isTokenInToken(tokA, tokB):
    """Checks if token is present in another token

    Arguments:
        tokA {visma.functions.structure.Function} -- function token
        tokB {visma.functions.structure.Function} -- function token

    Returns:
        bool -- if token present in token or not
    """
    if isinstance(tokA, Variable) and isinstance(tokB, Variable):
        varA = getVariables([tokA])
        varB = getVariables([tokB])
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
    """Checks if token is present in given function list

    Arguments:
        token {visma.functions.structure.Function} -- function token
        tokList {list} -- list of function tokens

    Returns:
        bool -- if token present in list or not
    """
    for tok in tokList:
        if isTokenInToken(token, tok) is True:
            return True
    return False


def getTokensType(tokens):
    """Checks if input tokens are expression, equation or inequality

    Arguments:
        tokens {list} -- list of function tokens

    Returns:
        string -- tokens type
    """
    for token in tokens:
        if isinstance(token, Binary):
            if token.value == '=':
                return "equation"
            elif token.value in ['<', '>', '<=', '>=']:
                return "inequality"
    return "expression"


def mathError(equationToken):
    '''Checks if an equation token is mathematically correct or not
    Typically, being used to check last equation token
    (Checks if LHS and RHS of equation token are equal or not)

    Arguments:
        equationToken{list} -- Equation token

    Returns:
        True{bool} -- if there is some math error in the last step of equation
        False{bool} -- if there is no math error in the last step of equation
    '''
    if len(equationToken) == 3:
        if (isinstance(equationToken[0], Constant) and isinstance(equationToken[1], Binary) and isinstance(equationToken[2], Constant)):
            if (equationToken[0].value != equationToken[2].value and equationToken[1].value == '='):
                return True
    return False


def postSimplification(tokens, animation):
    '''Intended to apply certain transformations which may be needed to be applied after expression simplification
    Typically being used to remove redundant '+' sign in expression beginning with it

    Arguments:
        tokens{list} -- tokens of CURRENT step
        animation{list} -- list of tokens of ALL steps yet

    Returns:
        tokens{list} -- posprocessed tokens of CURRENT step
        animation{list} -- list of postprocesses tokens of ALL steps
    '''
    if len(animation[-1]) == 2:
        if isinstance(animation[-1][0], Binary) and animation[-1][0].value == '+':
            animation[-1] = animation[-1][1:]
            tokens = tokens[1:]
    return tokens, animation
