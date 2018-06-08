import math
import copy
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary

greek = [u'\u03B1', u'\u03B2', u'\u03B3']


def is_variable(term):
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


def is_number(term):
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


def get_num(term):
    return float(term)


def is_equation(lTokens, rTokens):
    if len(lTokens) > 0 and len(rTokens) == 1:
        if isinstance(rTokens[0], Constant):
            if rTokens[0].value == 0:
                return True
    return False


def find_wrt_variable(lTokens, rTokens=None, variables=None):
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
            variables.extend(find_wrt_variable(token.tokens))

    for token in rTokens:
        if isinstance(token, Variable):
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif isinstance(token, Expression):
            variables.extend(find_wrt_variable(token.tokens, [], variables))
    return variables


def checkTypes(lTokens=None, rTokens=None):

    from visma.solvers.polynomial.roots import preprocess_check_quadratic_roots

    if lTokens is None:
        lTokens = []
    if rTokens is None:
        rTokens = []

    if len(rTokens) != 0:
        equationCompatible = EquationCompatibility(lTokens, rTokens)
        availableOperations = equationCompatible.availableOperations

        if preprocess_check_quadratic_roots(copy.deepcopy(lTokens), copy.deepcopy(rTokens)):
            availableOperations.append("find roots")
        type = "equation"
    else:
        expressionCompatible = ExpressionCompatibility(lTokens)
        availableOperations = expressionCompatible.availableOperations
        availableOperations.append("integrate")
        availableOperations.append("differentiate")
        type = "expression"

    return availableOperations, type


def check_solve_for(lTokens, rTokens):
    for token in lTokens:
        if isinstance(token, Variable):
            return True
        elif isinstance(token, Expression):
            if check_solve_for(token.tokens):
                return True

    for token in rTokens:
        if isinstance(token, Variable):
            return True
        elif isinstance(token, Expression):
            if check_solve_for(token.tokens):
                return True


def get_level_variables(tokens):
    variables = []
    for i, term in enumerate(tokens):
        if isinstance(term, Variable):
            skip = False
            for var in variables:
                if var.value == term.value:
                    if var.power[0] == term.power:
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
                if isinstance(var.value, list) and is_number(var.value[0]):
                    if isinstance(term.value, list):
                        term.value = evaluate_constant(term)
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
                    variable.value = [evaluate_constant(term)]
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
            var = get_level_variables(term.tokens)
            retType, val = extract_expression(var)
            if retType == "expression":
                variable = Expression()
                variable.value = val
                variable.tokens = term.tokens
                variables.append(variable)
            elif retType == "constant":
                skip = False
                for var in variables:
                    if isinstance(var.value, list) and is_number(var.value[0]):
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
                            if isinstance(var.value, list) and is_number(var.value[0]):
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
                                if variable2.before[l] == '+' or (variable2.before[l] == '' and get_num(variable2.value[l]) > 0):
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


def extract_expression(variable):
    if len(variable) == 1:
        if isinstance(variable[0], Expression):
            retType, variable = extract_expression(variable[0].value)
        elif isinstance(variable[0], Constant):
            return "constant", variable[0]
        elif isinstance(variable[0], Variable):
            return "variable", variable[0]
    else:
        if not eval_expressions(variable):
            return "expression", get_level_variables(variable)
        else:
            return "mixed", get_level_variables(variable)


def evaluate_constant(constant):
    if isinstance(constant, Function):
        if is_number(constant.value):
            return math.pow(constant.value, constant.power)
        elif isinstance(constant.value, list):
            val = 1
            if constant.coefficient is not None:
                val *= constant.coefficient
            for i, c_val in enumerate(constant.value):
                val *= math.pow(c_val, constant.power[i])
            return val
    elif is_number(constant):
        return constant


def eval_expressions(variables):
    var = []
    varPowers = []
    for i, variable in enumerate(variables):
        if isinstance(variable, Expression):
            if eval_expressions(variable.tokens):
                return False
        elif isinstance(variable, Variable):
            prev = False
            nxt = False
            # CHECKME: Undefined i and tokens. Which tokens ?
            if i != 0:
                if isinstance(variables[i - 1], Binary):
                    if variable[i - 1].value in ['-', '+']:
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
                if isinstance(variable[i - 1], Binary):
                    if variable[i - 1].value in ['-', '+']:
                        prev = True
                else:
                    print(variable[i - 1])
            else:
                prev = True

            if i + 1 < len(variable):
                if isinstance(variable[i + 1], Binary):
                    if variable[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    print(variable[i + 1])
            else:
                nxt = True
            if nxt and prev:
                match = False
                for i, v in enumerate(var):
                    if isinstance(v.value, list) and is_number(v.value[0]):
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


class EquationCompatibility(object):

    def __init__(self, lTokens, rTokens):
        self.lTokens = lTokens
        self.lVariables = []
        self.lVariables.extend(get_level_variables(self.lTokens))
        self.rTokens = rTokens
        self.rVariables = []
        self.rVariables.extend(get_level_variables(self.rTokens))
        self.availableOperations = []
        if check_solve_for(lTokens, rTokens):
            self.availableOperations.append('solve')
        self.availableOperations.extend(getOperationsEquation(self.lVariables, self.lTokens, self.rVariables, self.rTokens))
        # print self.availableOperations


class ExpressionCompatibility(object):
    """docstring for ExpressionCompatibility"""

    def __init__(self, tokens):
        super(ExpressionCompatibility, self).__init__()
        self.tokens = tokens
        self.variables = []
        self.variables.extend(get_level_variables(self.tokens))
        self.availableOperations = getOperationsExpression(self.variables, self.tokens)
