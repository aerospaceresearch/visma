import copy
from visma.io.parser import tokensToString
from visma.io.checks import get_level_variables, getOperationsEquation, getOperationsExpression, evaluate_constant, is_number
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.io.tokenize import remove_token


def division_equation(lToks, rToks, direct=False):
    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    animation = []
    comments = []
    if direct:
        comments = [[]]
    animBuilder = lToks
    l = len(lToks)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    animBuilder.append(equalTo)
    if len(rToks) == 0:
        zero = Zero()
        zero.scope = [l + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(get_level_variables(lTokens))
    rVariables = []
    rVariables.extend(get_level_variables(rTokens))
    availableOperations = getOperationsExpression(lVariables, lTokens)
    while '/' in availableOperations:
        var, tok, rem, com = expression_division(lVariables, lTokens)
        lTokens = remove_token(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        l = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [l]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = get_level_variables(lTokens)
        availableOperations = getOperationsExpression(lVariables, lTokens)

    availableOperations = getOperationsExpression(rVariables, rTokens)
    while '/' in availableOperations:
        var, tok, rem, com = expression_division(rVariables, rTokens)
        rTokens = remove_token(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        l = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [l]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = get_level_variables(rTokens)
        availableOperations = getOperationsExpression(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    l = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Zero()
        zero.scope = [l + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    lVariables = get_level_variables(lTokens)
    rVariables = get_level_variables(rTokens)
    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def division(tokens, direct=False):
    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while '/' in availableOperations:
        var, tok, rem, com = expression_division(variables, tokens)
        tokens = remove_token(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = get_level_variables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def multiplication_equation(lToks, rToks, direct=False):
    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    comments = []
    if direct:
        comments = [[]]
    animation = []
    animBuilder = lToks
    l = len(lToks)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    animBuilder.append(equalTo)
    if len(rToks) == 0:
        zero = Zero()
        zero.scope = [l + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(get_level_variables(lTokens))
    rVariables = []
    rVariables.extend(get_level_variables(rTokens))
    availableOperations = getOperationsExpression(lVariables, lTokens)
    while '*' in availableOperations:
        var, tok, rem, com = expression_multiplication(lVariables, lTokens)
        lTokens = remove_token(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        l = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [l]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = get_level_variables(lTokens)
        availableOperations = getOperationsExpression(lVariables, lTokens)

    availableOperations = getOperationsExpression(rVariables, rTokens)
    while '*' in availableOperations:
        var, tok, rem, com = expression_multiplication(rVariables, rTokens)
        rTokens = remove_token(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        l = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [l]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = get_level_variables(rTokens)
        availableOperations = getOperationsExpression(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    l = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Zero()
        zero.scope = [l + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    lVariables = get_level_variables(lTokens)
    rVariables = get_level_variables(rTokens)
    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def multiplication(tokens, direct=False):
    # FIXME: Fix multiplication for variables (Ex: x^-1 * x^2)
    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while '*' in availableOperations:
        var, tok, rem, com = expression_multiplication(variables, tokens)
        tokens = remove_token(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = get_level_variables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments

# del maybe


def multiply_variables(variable1, variable2, coeff):
    variable = Variable()
    variable.value = []
    variable.value.extend(variable1.value)
    variable.power = []
    variable.power.extend(variable1.power)
    if is_number(variable1.coefficient):
        variable.coefficient = float(variable1.coefficient)
    elif isinstance(variable1.coefficient, Function):
        variable.coefficient = evaluate_constant(variable1.coefficient)
    else:
        variable.coefficient = variable1.coefficient
    for j, var in enumerate(variable.value):
        found = False
        for k, var2 in enumerate(variable2.value):
            if var == var2:
                if is_number(variable.power[j]) and is_number(variable2.power[k]):
                    variable.power[j] += variable2.power[k]
                    found = True
                    break
        if not found:
            variable.value.append(variable2.value[j])
            variable.power.append(variable2.power[j])
    variable.coefficient *= variable2.coefficient
    variable.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i+1].scope)
    return variable


def multiply_constants(constant1, constant2, coeff):
    no_1 = False
    no_2 = False
    constant = Constant()
    if is_number(constant1.value):
        no_1 = True
    if is_number(constant2.value):
        no_2 = True
    if no_1 and no_2:
        constant.value = evaluate_constant(
            constant1) * evaluate_constant(constant2) * coeff
        constant.power = 1
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)
    elif no_1 and not no_2:
        constant.value = constant2.value
        constant.power = constant2.power
        done = False
        for i, val in enumerate(constant.value):
            if val == constant1.value:
                constant.power[i] += constant1.power
                done = True
                break
        if not done:
            constant.value.append(constant1.value)
            constant.power.append(constant1.power)
        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)
    elif not no_1 and no_2:
        constant.value = constant1.value
        constant.power = constant1.power
        done = False
        for i, val in enumerate(constant.value):
            if val == constant2.value:
                constant.power[i] += constant2.power
                done = True
                break
        if not done:
            constant.value.append(constant2.value)
            constant.power.append(constant2.power)
        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i+1].scope)
    elif not no_1 and not no_2:
        constant.value = constant2.value
        constant.power = constant2.power
        for i, val in enumerate(constant1.value):
            done = False
            for j, val2 in enumerate(constant.value):
                if val == val2:
                    constant.power[j] += constant1.power[i]
                    done = True
                    break
            if not done:
                constant.value.append(val)
                constant.power.append(constant1.power[i])

        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)

    return constant


def multiply_variable_constant(constant, variable, coeff):
    variable1 = Variable()
    variable1.value = []
    variable1.value.extend(variable.value)
    variable1.power = []
    variable1.power.extend(variable.power)
    if is_number(variable.coefficient):
        variable1.coefficient = float(variable.coefficient)
    elif isinstance(variable.coefficient, Function):
        variable1.coefficient = evaluate_constant(variable.coefficient)
    else:
        variable.coefficient = variable1.coefficient

    variable1.coefficient *= evaluate_constant(constant)
    variable1.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i-1].scope)
    return variable1


def multiply_expression_constant(constant, expression, coeff):
    tokens = copy.deepcopy(expression)
    tokens.coefficient *= (evaluate_constant(constant) * coeff)
    return tokens


def multiply_expression_variable(variable, expression, coeff):
    tokens = []
    for token in expression.tokens:
        if isinstance(token, Variable):
            tokens.append(multiply_variables(
                variable, token, expression.coefficient))
        elif isinstance(token, Constant):
            tokens.append(multiply_variable_constant(
                token, variable, expression.coefficient))
        elif isinstance(token, Expression):
            tokens.append(multiply_expression_variable(
                variable, token, expression.coefficient))
        elif isinstance(token, Binary):
            tokens.append(token)
    return tokens


def multiply_select(token1, token2, coeff=1):
    if isinstance(token1, Variable) and isinstance(token2, Variable):
        return multiply_variables(token1, token2, coeff)
    elif isinstance(token1, Variable) and isinstance(token2, Constant):
        return multiply_variable_constant(token2, token1, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Variable):
        return multiply_variable_constant(token1, token2, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Constant):
        return multiply_constants(token1, token2, coeff)


def multiply_expressions(expression1, expression2):
    tokens = []
    tokens1 = expression1.tokens
    tokens2 = expression2.tokens
    coeff = expression1.coefficient * expression2.coefficient
    for i, token1 in enumerate(tokens1):
        # print token1.value
        op = 1
        if i != 0:
            if isinstance(tokens1[i - 1], Binary):
                if tokens1[i - 1].value == '+':
                    op *= 1
                elif tokens1[i - 1].value == '-':
                    op *= -1
        if isinstance(token1, Variable) or isinstance(token1, Constant):
            for j, token2 in enumerate(tokens2):
                # print token2.value
                op2 = op
                if isinstance(token2, Variable) or isinstance(token2, Constant):
                    if j == 0 and i == 0:
                        pass
                    else:
                        if j != 0:
                            if isinstance(tokens2[j - 1], Binary):
                                if tokens2[j - 1].value == '+':
                                    op2 *= 1
                                elif tokens2[j - 1].value == '-':
                                    op2 *= -1
                        binary = Binary()
                        if op2 == -1:
                            binary.value = '-'
                        elif op2 == 1:
                            binary.value = '+'
                        tokens.append(binary)
                    tokens.append(multiply_select(token1, token2, coeff))
                    # print tokens


def expression_multiplication(variables, tokens):
    removeScopes = []
    comments = []
    for i, token in enumerate(tokens):
        if isinstance(token, Binary):
            if token.value in ['*']:
                prev = False
                nxt = False
                if i != 0:
                    if tokens[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(tokens):
                    if tokens[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if nxt and prev:
                    if isinstance(tokens[i + 1], Constant) and isinstance(tokens[i - 1], Constant):
                        comments.append("Multiplying " + r"$" + tokens[i-1].__str__() + r"$" + " and " + r"$" + tokens[i+1].__str__() + r"$")
                        no_1 = False
                        no_2 = False
                        if is_number(tokens[i - 1].value):
                            no_1 = True
                        if is_number(tokens[i + 1].value):
                            no_2 = True
                        if no_1 and no_2:
                            tokens[i + 1].value = evaluate_constant(
                                tokens[i - 1]) * evaluate_constant(tokens[i + 1])
                            tokens[i + 1].power = 1
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i - 1].scope)
                        elif no_1 and not no_2:
                            tokens[i + 1].value.append(tokens[i - 1].value)
                            tokens[i + 1].power.append(tokens[i - 1].power)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i - 1].scope)
                        elif not no_1 and no_2:
                            tokens[i - 1].value.append(tokens[i + 1].value)
                            tokens[i - 1].power.append(tokens[i + 1].power)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i + 1].scope)
                        elif not no_1 and not no_2:
                            for vals in tokens[i - 1].value:
                                tokens[i + 1].value.append(vals)
                            for pows in tokens[i - 1].power:
                                tokens[i + 1].power.append(pows)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i - 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Variable):
                        comments.append("Multiplying " + r"$" + tokens[i - 1].__str__() + r"$" + " and " + r"$" + tokens[i + 1].__str__() + r"$")
                        for j, var in enumerate(tokens[i + 1].value):
                            found = False
                            for k, var2 in enumerate(tokens[i - 1].value):
                                tokens[i - 1].coefficient *= tokens[i + 1].coefficient
                                if var == var2:
                                    if tokens[i + 1].power[j] == tokens[i - 1].power[k]:
                                        if is_number(tokens[i + 1].power[j]) and is_number(tokens[i - 1].power[k]):
                                            tokens[i - 1].power[k] += tokens[i + 1].power[j]
                                            found = True
                                            break
                            if not found:
                                tokens[i - 1].value.append(tokens[i + 1].value[j])
                                tokens[i - 1].power.append(tokens[i + 1].power[j])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Constant)):
                        comments.append("Multiplying " + r"$" + tokens[i - 1].__str__() + "}" + r"$" + " and " + r"$" + tokens[i + 1].__str__() + r"$")
                        tokens[i + 1].coefficient *= evaluate_constant(tokens[i - 1])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i - 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (isinstance(tokens[i - 1], Variable) and isinstance(tokens[i + 1], Constant)):
                        comments.append("Multiplying " + r"$" + tokens[i - 1].__str__() + r"$" + " and " + r"$" + tokens[i + 1].__str__() + r"$")
                        tokens[i - 1].coefficient *= evaluate_constant(tokens[i + 1])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

    return variables, tokens, removeScopes, comments


def division_variables(variable1, variable2, coeff):
    variable = copy.deepcopy(variable1)
    for j, var in enumerate(variable.value):
        found = False
        for k, var2 in enumerate(variable2.value):
            if var == var2:
                if is_number(variable.power[j]) and is_number(variable2.power[k]):
                    variable.power[j] -= variable2.power[k]
                    found = True
                    break
        if not found:
            variable.value.append(variable2.value[j])
            variable.power.append(-variable2.power[j])
    variable.coefficient /= variable2.coefficient
    variable.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i+1].scope)
    return variable


def division_constants(constant1, constant2, coeff):
    no_1 = False
    no_2 = False
    constant = Constant()
    if is_number(constant1.value):
        no_1 = True
    if is_number(constant2.value):
        no_2 = True
    if no_1 and no_2:
        constant.value = (evaluate_constant(
            constant1) / evaluate_constant(constant2)) * coeff
        constant.power = 1
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)
    elif no_1 and not no_2:
        constant.value = [constant1.value]
        constant.power = [constant1.power]
        for i, val in enumerate(constant2.value):
            done = False
            for j, val2 in enumerate(constant.value):
                if val == val2:
                    constant.power[j] -= constant2.power[i]
                    done = True
                    break
            if not done:
                constant.value.append(val)
                constant.power.append(-constant2.power[i])

        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)
    elif not no_1 and no_2:
        constant.value = constant1.value
        constant.power = constant1.power
        done = False
        for i, val in enumerate(constant.value):
            if val == constant2.value:
                constant.power[i] -= constant2.power
                done = True
                break
        if not done:
            constant.value.append(constant2.value)
            constant.power.append(-constant2.power)
        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i+1].scope)
    elif not no_1 and not no_2:
        constant.value = constant1.value
        constant.power = constant1.power
        for i, val in enumerate(constant2.value):
            done = False
            for j, val2 in enumerate(constant.value):
                if val == val2:
                    constant.power[j] -= constant2.power[i]
                    done = True
                    break
            if not done:
                constant.value.append(val)
                constant.power.append(-constant2.power[i])
        constant.value.append(coeff)
        constant.power.append(1)
        # removeScopes.append(tokens[i].scope)
        # removeScopes.append(tokens[i-1].scope)

    return constant


def division_variable_constant(constant, variable, coeff):
    variable1 = copy.deepcopy(variable)

    variable1.coefficient /= evaluate_constant(constant)
    variable1.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i-1].scope)
    return variable1


def division_constant_variable(constant, variable, coeff):
    variable1 = Variable()
    variable1.coefficient = (evaluate_constant(
        constant) / variable.coefficient) * coeff
    variable1.value = []
    variable1.power = []
    for i, var in enumerate(variable):
        variable1.value.append(var)
        variable1.power.append(-variable.power[i])
    return variable1


def division_expression_constant(constant, expression, coeff):
    tokens = copy.deepcopy(expression)
    tokens.coefficient /= (evaluate_constant(constant))
    tokens.coefficient *= coeff
    return tokens


def division_constant_expression(constant, expression, coeff):
    pass


def division_expression_variable(variable, expression, coeff):
    tokens = []
    for token in expression.tokens:
        if isinstance(token, Variable):
            tokens.append(division_variables(
                token, variable, expression.coefficient))
        elif isinstance(token, Constant):
            tokens.append(division_constant_variable(
                token, variable, expression.coefficient))
        elif isinstance(token, Expression):
            tokens.append(division_expression_variable(
                variable, token, expression.coefficient))
        elif isinstance(token, Binary):
            tokens.append(token)
    return tokens


def division_variable_expression(variable, expression, coeff):
    pass


def division_select(token1, token2, coeff=1):
    if isinstance(token1, Variable) and isinstance(token2, Variable):
        return division_variables(token1, token2, coeff)
    elif isinstance(token1, Variable) and isinstance(token2, Constant):
        return division_variable_constant(token2, token1, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Variable):
        return division_variable_constant(token1, token2, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Constant):
        return division_constants(token1, token2, coeff)


def division_expressions(expression1, expression2):
    pass


def expression_division(variables, tokens):
    removeScopes = []
    comments = []
    for i, token in enumerate(tokens):
        if isinstance(token, Binary):
            if token.value in ['/']:
                prev = False
                nxt = False
                if i != 0:
                    if tokens[i - 1].__class__ in [Variable, Constant]:
                        prev = True
                if i + 1 < len(tokens):
                    if tokens[i + 1].__class__ in [Variable, Constant]:
                        nxt = True
                if nxt and prev:
                    if isinstance(tokens[i + 1], Constant) and isinstance(tokens[i - 1], Constant):
                        comments.append("Dividing " + r"$" + tokens[i - 1].__str__() + r"$" + " by " + r"$" + tokens[i + 1].__str__() + r"$")
                        no_1 = False
                        no_2 = False
                        if is_number(tokens[i - 1].value):
                            no_1 = True
                        if is_number(tokens[i + 1].value):
                            no_2 = True
                        if no_1 and no_2:
                            tokens[i + 1].value = evaluate_constant(
                                tokens[i - 1]) / evaluate_constant(tokens[i + 1])
                            tokens[i + 1].power = 1
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i - 1].scope)
                        elif no_1 and not no_2:
                            value = tokens[i - 1].value
                            power = tokens[i - 1].power
                            tokens[i - 1].value = [value]
                            tokens[i - 1].power = [power]
                            for val in tokens[i + 1].value:
                                tokens[i - 1].value.append(val)
                            for pows in tokens[i + 1].power:
                                tokens[i - 1].power.append(-pows)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i + 1].scope)
                        elif not no_1 and no_2:
                            tokens[i - 1].value.append(tokens[i + 1].value)
                            tokens[i - 1].power.append(-tokens[i + 1].power)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i + 1].scope)
                        elif not no_1 and not no_2:
                            for vals in tokens[i + 1].value:
                                tokens[i - 1].value.append(vals)
                            for pows in tokens[i + 1].power:
                                tokens[i - 1].power.append(pows)
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Variable):
                        comments.append("Dividing " + r"$" + tokens[i - 1].__str__() + r"$" + " by " + r"$" + tokens[i + 1].__str__() + r"$")
                        for j, var in enumerate(tokens[i + 1].value):
                            found = False
                            for k, var2 in enumerate(tokens[i - 1].value):
                                tokens[i-1].coefficient /= tokens[i+1].coefficient
                                if var == var2:
                                    if is_number(tokens[i + 1].power[j]) and is_number(tokens[i - 1].power[k]):
                                        tokens[i - 1].power[k] -= tokens[i + 1].power[j]
                                        if tokens[i - 1].power[k] == 0:
                                            del tokens[i - 1].power[k]
                                            del tokens[i - 1].value[k]
                                        found = True
                                        break
                            if not found:
                                tokens[i - 1].value.append(tokens[i + 1].value[j])
                                tokens[i - 1].power.append(-tokens[i + 1].power[j])

                            if len(tokens[i - 1].value) == 0:
                                constant = Constant()
                                constant.scope = tokens[i - 1].scope
                                constant.power = 1
                                constant.value = tokens[i - 1].coefficient
                                tokens[i - 1] = constant
                            removeScopes.append(tokens[i].scope)
                            removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Constant)):
                        comments.append("Dividing " + r"$" + tokens[i - 1].__str__() + r"$" + " by " + r"$" + tokens[i + 1].__str__() + r"$")
                        val = evaluate_constant(tokens[i - 1])
                        scope = tokens[i - 1].scope
                        tokens[i - 1] = Variable()
                        tokens[i - 1].value = tokens[i + 1].value
                        tokens[i - 1].coefficient = val / \
                            tokens[i + 1].coefficient
                        tokens[i - 1].power = []
                        tokens[i - 1].scope = scope
                        for pows in tokens[i + 1].power:
                            tokens[i - 1].power.append(-pows)

                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (isinstance(tokens[i - 1], Variable) and isinstance(tokens[i + 1], Constant)):
                        comments.append("Dividing " + r"$" + tokens[i - 1].__str__() + r"$" + " by " + r"$" + tokens[i + 1].__str__() + r"$")
                        tokens[i - 1].coefficient /= evaluate_constant(tokens[i + 1])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments
    return variables, tokens, removeScopes, comments
