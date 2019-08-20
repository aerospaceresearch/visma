import copy
from visma.io.parser import tokensToString
from visma.io.checks import getLevelVariables, getOperationsEquation, getOperationsExpression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.io.tokenize import removeToken

##################
# Multiplication #
##################


def multiplication(tokens, direct=False):
    """Function deals with multiplication related operations (driver function in multiplication module)

    Arguments:
        tokens {list} -- list of tokens
        direct {bool} -- True when we are only concerned about multiplications terms in the input

    Returns:
        tokens {list} -- list of tokens
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(getLevelVariables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while '*' in availableOperations:
        _, tok, rem, com = expressionMultiplication(variables, tokens)
        tokens = removeToken(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = getLevelVariables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def expressionMultiplication(variables, tokens):
    """Function deals with multiplication related operations of two terms (called from driver function)

    Arguments:
        variables {list} -- list of LevelVariables
        tokens {list} -- list of tokens

    Returns:
        variables {list} -- list of LevelVariables
        tokens {list} -- list of tokens
        removeScopes {list} -- indices of those tokens (/terms) which are removed as two terms in the equations get multiplied
        comments {list} -- list of comments in equation solving process
    """

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
                    comments.append("Multiplying " + r"$" + tokens[i-1].__str__() + r"$" + " and " + r"$" + tokens[i+1].__str__() + r"$")
                    if isinstance(tokens[i + 1], Constant) and isinstance(tokens[i - 1], Constant):
                        tokens[i + 1] = tokens[i + 1] * tokens[i - 1]
                        removeScopes.extend([tokens[i].scope, tokens[i - 1].scope])

                    elif isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Variable):
                        tokens[i - 1] = tokens[i - 1] * tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i + 1].scope])

                    elif (isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Constant)):
                        tokens[i + 1] = tokens[i - 1] * tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i - 1].scope])

                    elif (isinstance(tokens[i - 1], Variable) and isinstance(tokens[i + 1], Constant)):
                        tokens[i - 1] = tokens[i - 1] * tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i + 1].scope])

    return variables, tokens, removeScopes, comments


def multiplicationEquation(lToks, rToks, direct=False):
    """Function deals with multiplication related operations FOR EQUATIONS (driver function in multiplication module)

    Arguments:
        rtoks {list} -- list of right tokens
        ltoks {list} -- list of left tokens
        direct {bool} -- True when we are only concerned about multiplications terms in the input

    Returns:
        rtoks {list} -- list of right tokens
        ltoks {list} -- list of left tokens
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    comments = []
    if direct:
        comments = [[]]
    animation = []
    animBuilder = lToks
    lenToks = len(lToks)
    equalTo = Binary()
    equalTo.scope = [lenToks]
    equalTo.value = '='
    animBuilder.append(equalTo)
    if len(rToks) == 0:
        zero = Zero()
        zero.scope = [lenToks + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(getLevelVariables(lTokens))
    rVariables = []
    rVariables.extend(getLevelVariables(rTokens))
    availableOperations = getOperationsExpression(lVariables, lTokens)
    while '*' in availableOperations:
        _, tok, rem, com = expressionMultiplication(lVariables, lTokens)
        lTokens = removeToken(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        lenToks = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [lenToks]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [lenToks + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = getLevelVariables(lTokens)
        availableOperations = getOperationsExpression(lVariables, lTokens)

    availableOperations = getOperationsExpression(rVariables, rTokens)
    while '*' in availableOperations:
        _, tok, rem, com = expressionMultiplication(rVariables, rTokens)
        rTokens = removeToken(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        lenToks = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [lenToks]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [lenToks + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = getLevelVariables(rTokens)
        availableOperations = getOperationsExpression(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    lenToks = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [lenToks]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Zero()
        zero.scope = [lenToks + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    lVariables = getLevelVariables(lTokens)
    rVariables = getLevelVariables(rTokens)
    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


############
# Division #
############


def division(tokens, direct=False):
    """Function deals with division related operations (driver function in division module)

    Arguments:
        tokens {list} -- list of tokens
        direct {bool} -- True when we are only concerned about multiplications terms in the input

    Returns:
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(getLevelVariables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while '/' in availableOperations:
        _, tok, rem, com = expressionDivision(variables, tokens)
        tokens = removeToken(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = getLevelVariables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def expressionDivision(variables, tokens):
    """Function deals with multiplication related operations of two terms (called from driver function)

    Arguments:
        variables {list} -- list of LevelVariables
        tokens {list} -- list of tokens

    Returns:
        variables {list} -- list of LevelVariables
        tokens {list} -- list of tokens
        removeScopes {list} -- indices of those tokens (/terms) which are removed as two terms in the equations get multiplied
        comments {list} -- list of comments in equation solving process
    """

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
                    comments.append("Dividing " + r"$" + tokens[i - 1].__str__() + r"$" + " by " + r"$" + tokens[i + 1].__str__() + r"$")
                    if isinstance(tokens[i + 1], Constant) and isinstance(tokens[i - 1], Constant):
                        tokens[i + 1] = tokens[i - 1] / tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i - 1].scope])

                    elif isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Variable):
                        tokens[i - 1] = tokens[i - 1] / tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i + 1].scope])

                    elif (isinstance(tokens[i + 1], Variable) and isinstance(tokens[i - 1], Constant)):
                        scope = tokens[i - 1].scope
                        tokens[i - 1] = tokens[i - 1] / tokens[i + 1]
                        tokens[i - 1].scope = scope
                        removeScopes.extend([tokens[i].scope, tokens[i + 1].scope])

                    elif (isinstance(tokens[i - 1], Variable) and isinstance(tokens[i + 1], Constant)):
                        tokens[i - 1] = tokens[i - 1] / tokens[i + 1]
                        removeScopes.extend([tokens[i].scope, tokens[i + 1].scope])

    return variables, tokens, removeScopes, comments


def divisionEquation(lToks, rToks, direct=False):
    """Function deals with division related operations FOR EQUATIONS (driver function in division module)

    Arguments:
        rtoks {list} -- list of right tokens
        ltoks {list} -- list of left tokens
        direct {bool} -- True when we are only concerned about multiplications terms in the input

    Returns:
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    animation = []
    comments = []
    if direct:
        comments = [[]]
    animBuilder = lToks
    lenToks = len(lToks)
    equalTo = Binary()
    equalTo.scope = [lenToks]
    equalTo.value = '='
    animBuilder.append(equalTo)
    if len(rToks) == 0:
        zero = Zero()
        zero.scope = [lenToks + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(getLevelVariables(lTokens))
    rVariables = []
    rVariables.extend(getLevelVariables(rTokens))
    availableOperations = getOperationsExpression(lVariables, lTokens)
    while '/' in availableOperations:
        _, tok, rem, com = expressionDivision(lVariables, lTokens)
        lTokens = removeToken(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        lenToks = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [lenToks]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [lenToks + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = getLevelVariables(lTokens)
        availableOperations = getOperationsExpression(lVariables, lTokens)

    availableOperations = getOperationsExpression(rVariables, rTokens)
    while '/' in availableOperations:
        _, tok, rem, com = expressionDivision(rVariables, rTokens)
        rTokens = removeToken(tok, rem)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        lenToks = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [lenToks]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.scope = [lenToks + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = getLevelVariables(rTokens)
        availableOperations = getOperationsExpression(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    lenToks = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [lenToks]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Zero()
        zero.scope = [lenToks + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    lVariables = getLevelVariables(lTokens)
    rVariables = getLevelVariables(rTokens)
    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


################################################
# TODO: Expression multiplication and division #
################################################

'''
def multiplySelect(token1, token2, coeff=1):

    if isinstance(token1, Variable) and isinstance(token2, Variable):
        return multiplyVariables(token1, token2, coeff)
    elif isinstance(token1, Variable) and isinstance(token2, Constant):
        return multiplyVariableConstant(token2, token1, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Variable):
        return multiplyVariableConstant(token1, token2, coeff)
    elif isinstance(token1, Constant) and isinstance(token2, Constant):
        return multiplyConstants(token1, token2, coeff)


def multiplyConstants(constant1, constant2, coeff):

    no_1 = False
    no_2 = False
    constant = Constant()
    if isNumber(constant1.value):
        no_1 = True
    if isNumber(constant2.value):
        no_2 = True
    if no_1 and no_2:
        constant.value = evaluateConstant(
            constant1) * evaluateConstant(constant2) * coeff
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


def multiplyVariables(variable1, variable2, coeff):

    variable = Variable()
    variable.value = []
    variable.value.extend(variable1.value)
    variable.power = []
    variable.power.extend(variable1.power)
    if isNumber(variable1.coefficient):
        variable.coefficient = float(variable1.coefficient)
    elif isinstance(variable1.coefficient, Function):
        variable.coefficient = evaluateConstant(variable1.coefficient)
    else:
        variable.coefficient = variable1.coefficient
    for j, var in enumerate(variable.value):
        found = False
        for k, var2 in enumerate(variable2.value):
            if var == var2:
                if isNumber(variable.power[j]) and isNumber(variable2.power[k]):
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


def multiplyVariableConstant(constant, variable, coeff):

    variable1 = Variable()
    variable1.value = []
    variable1.value.extend(variable.value)
    variable1.power = []
    variable1.power.extend(variable.power)
    if isNumber(variable.coefficient):
        variable1.coefficient = float(variable.coefficient)
    elif isinstance(variable.coefficient, Function):
        variable1.coefficient = evaluateConstant(variable.coefficient)
    else:
        variable.coefficient = variable1.coefficient

    variable1.coefficient *= evaluateConstant(constant)
    variable1.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i-1].scope)
    return variable1


def multiplyExpressions(expression1, expression2):

    tokens = []
    tokens1 = expression1.tokens
    tokens2 = expression2.tokens
    coeff = expression1.coefficient * expression2.coefficient
    for i, token1 in enumerate(tokens1):
        # print(token1.value)
        op = 1
        if i != 0:
            if isinstance(tokens1[i - 1], Binary):
                if tokens1[i - 1].value == '+':
                    op *= 1
                elif tokens1[i - 1].value == '-':
                    op *= -1
        if isinstance(token1, Variable) or isinstance(token1, Constant):
            for j, token2 in enumerate(tokens2):
                # print(token2.value)
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
                    tokens.append(multiplySelect(token1, token2, coeff))
                    # print(tokens)


def multiply_expression_constant(constant, expression, coeff):

    tokens = copy.deepcopy(expression)
    tokens.coefficient *= (evaluateConstant(constant) * coeff)
    return tokens


def multiply_expression_variable(variable, expression, coeff):

    tokens = []
    for token in expression.tokens:
        if isinstance(token, Variable):
            tokens.append(multiplyVariables(
                variable, token, expression.coefficient))
        elif isinstance(token, Constant):
            tokens.append(multiplyVariableConstant(
                token, variable, expression.coefficient))
        elif isinstance(token, Expression):
            tokens.append(multiply_expression_variable(
                variable, token, expression.coefficient))
        elif isinstance(token, Binary):
            tokens.append(token)
    return tokens


def division_variables(variable1, variable2, coeff):

    variable = copy.deepcopy(variable1)
    for j, var in enumerate(variable.value):
        found = False
        for k, var2 in enumerate(variable2.value):
            if var == var2:
                if isNumber(variable.power[j]) and isNumber(variable2.power[k]):
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
    if isNumber(constant1.value):
        no_1 = True
    if isNumber(constant2.value):
        no_2 = True
    if no_1 and no_2:
        constant.value = (evaluateConstant(
            constant1) / evaluateConstant(constant2)) * coeff
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

    variable1.coefficient /= evaluateConstant(constant)
    variable1.coefficient *= coeff
    # removeScopes.append(tokens[i].scope)
    # removeScopes.append(tokens[i-1].scope)
    return variable1


def division_constantVariable(constant, variable, coeff):

    variable1 = Variable()
    variable1.coefficient = (evaluateConstant(
        constant) / variable.coefficient) * coeff
    variable1.value = []
    variable1.power = []
    for i, var in enumerate(variable):
        variable1.value.append(var)
        variable1.power.append(-variable.power[i])
    return variable1


def division_expression_constant(constant, expression, coeff):

    tokens = copy.deepcopy(expression)
    tokens.coefficient /= (evaluateConstant(constant))
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
            tokens.append(division_constantVariable(
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
'''
