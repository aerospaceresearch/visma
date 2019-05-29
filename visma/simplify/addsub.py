import copy
from visma.io.parser import tokensToString
from visma.io.checks import getLevelVariables, getOperationsEquation, getOperationsExpression
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.io.tokenize import changeToken, removeToken

############
# Addition #
############


def addition(tokens, direct=False):

    animation = [copy.deepcopy(tokens)]
    variables = []
    comments = []
    if direct:
        comments = [[]]
    variables.extend(getLevelVariables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)

    while '+' in availableOperations:
        _, tok, rem, change, com = expressionAddition(variables, tokens)
        tokens = changeToken(removeToken(tok, rem), change)
        if not tokens:
            tokens.append(Zero())
        animation.append(copy.deepcopy(tokens))
        comments.append(com)
        variables = getLevelVariables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def additionEquation(lToks, rToks, direct=False):

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
    while '+' in availableOperations:
        _, tok, rem, change, com = expressionAddition(lVariables, lTokens)
        lTokens = changeToken(removeToken(tok, rem), change)
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
    while '+' in availableOperations:
        _, tok, rem, change, com = expressionAddition(rVariables, rTokens)
        rTokens = changeToken(removeToken(tok, rem), change)
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

    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    while '+' in availableOperations:
        lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, com = equationAddition(
            lVariables, lTokens, rVariables, rTokens)
        rTokens = changeToken(removeToken(rTokens, rRemoveScopes), rChange)
        lTokens = changeToken(removeToken(lTokens, lRemoveScopes), lChange)
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
        rVariables = getLevelVariables(rTokens)
        availableOperations = getOperationsEquation(
            lVariables, lTokens, rVariables, rTokens)

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
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def expressionAddition(variables, tokens):

    removeScopes = []
    change = []
    comments = []
    for _, variable in enumerate(variables):
        if isinstance(variable, Constant):
            if len(variable.value) > 1:
                constantAdd = []
                constant = []
                for j in range(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '-']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    for consAdd in constantAdd:
                        for const in constant:
                            comments.append("Adding " + r"$" + variable.__str__(consAdd, const) + r"$" + " and " + r"$" + variable.__str__(const, const) + r"$")

                            c1 = Constant(variable.value[consAdd], variable.power[consAdd])
                            c1.scope = variable.scope[consAdd]
                            c1.after = variable.after[consAdd]
                            c1.before = variable.before[consAdd]
                            c1.beforeScope = variable.beforeScope[consAdd]

                            c2 = Constant(variable.value[const], variable.power[const])
                            c2.scope = variable.scope[const]
                            c2.after = variable.after[const]
                            c2.before = variable.before[const]
                            c2.beforeScope = variable.beforeScope[const]

                            valChange = c2 + c1

                            if c2.value == 0 and c2.power != 0:
                                removeScopes.append(
                                    c2.scope)
                                removeScopes.append(
                                    c2.beforeScope)

                            if c2.value < 0 and c2.before in ['-', '+']:
                                valChange.value = - \
                                    1 * valChange.value
                                c2.value = - \
                                    1 * c2.value
                                signChange = Binary()
                                signChange.scope = c2.beforeScope
                                if c2.before == '-':
                                    signChange.value = '+'
                                elif c2.before == '+':
                                    signChange.value = '-'
                                change.append(signChange)
                            change.append(valChange)
                            removeScopes.append(c1.scope)
                            removeScopes.append(c1.beforeScope)
                            return _, tokens, removeScopes, change, comments

                        for consAdd1 in constantAdd:
                            comments.append("Adding " + r"$" + variable.__str__(consAdd, consAdd1) + r"$" + " and " + r"$" + variable.__str__(consAdd1, consAdd1) + r"$")

                            c1 = Constant(variable.value[consAdd1], variable.power[consAdd1])
                            c1.scope = variable.scope[consAdd1]
                            c1.after = variable.after[consAdd1]
                            c1.before = variable.before[consAdd1]
                            c1.beforeScope = variable.beforeScope[consAdd1]

                            c2 = Constant(variable.value[consAdd], variable.power[consAdd])
                            c2.scope = variable.scope[consAdd]
                            c2.after = variable.after[consAdd]
                            c2.before = variable.before[consAdd]
                            c2.beforeScope = variable.beforeScope[consAdd]

                            valChange = c2 + c1

                            if c2.value < 0 and c2.before in ['-', '+']:
                                valChange.value = - \
                                    1 * valChange.value
                                c2.value = - \
                                    1 * c2.value
                                signChange = Binary()
                                signChange.scope = c2.beforeScope
                                if c2.before == '-':
                                    signChange.value = '+'
                                elif c2.before == '+':
                                    signChange.value = '-'
                                change.append(signChange)
                            change.append(valChange)
                            removeScopes.append(c1.scope)
                            removeScopes.append(c1.beforeScope)
                            return _, tokens, removeScopes, change, comments

                elif len(constant) == 0 and len(constantAdd) > 1:
                    i = 0
                    while i < len(constantAdd):
                        for j, const in enumerate(constantAdd):
                            if i != j:
                                comments.append("Adding " + r"$" + variable.__str__(constantAdd[i], const) + r"$" + " and " + r"$" + variable.__str__(const, const) + r"$")

                                c1 = Constant(variable.value[constantAdd[i]], variable.power[constantAdd[i]])
                                c1.scope = variable.scope[constantAdd[i]]
                                c1.after = variable.after[constantAdd[i]]
                                c1.before = variable.before[constantAdd[i]]
                                c1.beforeScope = variable.beforeScope[constantAdd[i]]

                                c2 = Constant(variable.power[const], variable.power[const])
                                c2.scope = variable.scope[const]
                                c2.after = variable.after[const]
                                c2.before = variable.before[const]
                                c2.beforeScope = variable.beforeScope[const]

                                valChange = c2 + c1

                                if c2.value < 0 and c2.before in ['-', '+']:
                                    valChange.value = - \
                                        1 * valChange.value
                                    c2.value = - \
                                        1 * c2.value
                                    signChange = Binary()
                                    signChange.scope = c2.beforeScope
                                    if c2.before == '-':
                                        signChange.value = '+'
                                    elif c2.before == '+':
                                        signChange.value = '-'
                                    change.append(signChange)
                                change.append(valChange)
                                removeScopes.append(c1.scope)
                                removeScopes.append(c1.beforeScope)
                                return _, tokens, removeScopes, change, comments
                        i += 1

        elif isinstance(variable, Variable):
            if len(variable.power) > 1:
                varAdd = []
                var = []
                for j in range(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+']:
                        varAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '-']:
                        var.append(j)
                if len(var) > 0 and len(varAdd) > 0:
                    for varAddItr in varAdd:
                        for varItr in var:
                            comments.append("Adding " + r"$" + variable.__str__(varAddItr, varAddItr, varAddItr) + r"$" + " and " + r"$" + variable.__str__(varItr, varItr, varItr) + r"$")

                            v1 = Variable(variable.coefficient[varAddItr])
                            v1.power = variable.power[varAddItr]
                            v1.scope = variable.scope[varAddItr]
                            v1.before = variable.before[varAddItr]
                            v1.beforeScope = variable.beforeScope[varAddItr]

                            v2 = Variable(variable.coefficient[varItr])
                            v2.power = variable.power[varItr]
                            v2.scope = variable.scope[varItr]
                            v2.before = variable.before[varItr]
                            v2.beforeScope = variable.beforeScope[varItr]

                            valChange = v2 + v1
                            valChange.value = variable.value

                            if v2.coefficient == 0:
                                removeScopes.append(v2.scope)
                                removeScopes.append(v2.beforeScope)
                            else:
                                if v2.coefficient < 0 and v2.before in ['-', '+']:
                                    valChange.coefficient = - \
                                        1 * valChange.coefficient
                                    v2.coefficient = - \
                                        1 * v2.coefficient
                                    signChange = Binary()
                                    signChange.scope = v2.beforeScope
                                    if v2.before == '-':
                                        signChange.value = '+'
                                    elif v2.before == '+':
                                        signChange.value = '-'
                                    change.append(signChange)
                                change.append(valChange)
                            removeScopes.append(v1.beforeScope)
                            removeScopes.append(v1.scope)
                            return variables, tokens, removeScopes, change, comments

                        for varAddItr1 in varAdd:
                            comments.append("Adding " + r"$" + variable.__str__(varAddItr, varAddItr, varAddItr) + r"$" + " and " + r"$" + variable.__str__(varAddItr1, varAddItr1, varAddItr1) + r"$")

                            v1 = Variable(variable.coefficient[varAddItr])
                            v1.power = variable.power[varAddItr]
                            v1.scope = variable.scope[varAddItr]
                            v1.before = variable.before[varAddItr]
                            v1.beforeScope = variable.beforeScope[varAddItr]

                            v2 = Variable(variable.coefficient[varAddItr1])
                            v2.power = variable.power[varAddItr1]
                            v2.scope = variable.scope[varAddItr1]
                            v2.before = variable.before[varAddItr1]
                            v2.beforeScope = variable.beforeScope[varAddItr1]

                            valChange = v2 + v1
                            valChange.value = variable.value

                            if v2.coefficient == 0:
                                removeScopes.append(v2.scope)
                                removeScopes.append(v2.beforeScope)
                            else:
                                if v2.coefficient < 0 and v2.before in ['-', '+']:
                                    valChange.coefficient = - \
                                        1 * valChange.coefficient
                                    v2.coefficient = - \
                                        1 * v2.coefficient
                                    signChange = Binary()
                                    signChange.scope = v2.beforeScope
                                    if v2.before == '-':
                                        signChange.value = '+'
                                    elif v2.before == '+':
                                        signChange.value = '-'
                                    change.append(signChange)
                                change.append(valChange)
                            removeScopes.append(v1.beforeScope)
                            removeScopes.append(v1.scope)
                            return variables, tokens, removeScopes, change, comments

                elif len(var) == 0 and len(varAdd) > 1:
                    i = 0
                    while i < len(varAdd):
                        for j, varAddItr in enumerate(varAdd):
                            if i != j:
                                comments.append("Adding " + r"$" + variable.__str__(varAdd[i], varAdd[i], varAdd[i]) + r"$" + " and " + r"$" + variable.__str__(varAddItr, varAddItr, varAddItr) + r"$")

                                v1 = Variable(variable.coefficient[varAdd[i]])
                                v1.power = variable.power[varAdd[i]]
                                v1.scope = variable.scope[varAdd[i]]
                                v1.before = variable.before[varAdd[i]]
                                v1.beforeScope = variable.beforeScope[varAdd[i]]

                                v2 = Variable(variable.coefficient[varAddItr])
                                v2.power = variable.power[varAddItr]
                                v2.scope = variable.scope[varAddItr]
                                v2.before = variable.before[varAddItr]
                                v2.beforeScope = variable.beforeScope[varAddItr]

                                valChange = v2 + v1
                                valChange.value = variable.value

                                if v2.coefficient == 0:
                                    removeScopes.append(v2.scope)
                                    removeScopes.append(v2.beforeScope)
                                else:
                                    if v2.coefficient < 0 and v2.before in ['-', '+']:
                                        valChange.coefficient = - \
                                            1 * valChange.coefficient
                                        v2.coefficient = - \
                                            1 * v2.coefficient
                                        signChange = Binary()
                                        signChange.scope = v2.beforeScope
                                        if v2.before == '-':
                                            signChange.value = '+'
                                        elif v2.before == '+':
                                            signChange.value = '-'
                                        change.append(signChange)
                                    change.append(valChange)
                                removeScopes.append(v1.beforeScope)
                                removeScopes.append(v1.scope)
                                return variables, tokens, removeScopes, change, comments
                        i += 1
        elif isinstance(variable, Expression):
            pass
    return variables, tokens, removeScopes, change, comments


def equationAddition(lVariables, lTokens, rVariables, rTokens):

    lRemoveScopes = []
    rRemoveScopes = []
    lChange = []
    rChange = []
    comments = []
    for variable in lVariables:
        if isinstance(variable, Constant):
            for j in range(len(variable.value)):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if isinstance(variable2, Constant):
                            if variable2.power[0] == variable.power[0] and variable2.value[0] == variable.value[0]:
                                for k in range(len(variable2.value)):
                                    if (variable2.before[k] == '-' or (variable2.before[k] == '' and variable2.value[k] < 0)) and variable2.after[k] in ['-', '+', '']:
                                        comments.append(
                                            "Moving " + r"$" + variable2.before[k] + variable2.__str__() + r"$" + " to LHS")
                                        if variable.before[j] == '-':
                                            variable.value[j] -= variable2.value[k]
                                        elif variable2.before[k] == '' and variable2.value[k] < 0:
                                            variable.value[j] -= variable2.value[k]
                                        else:
                                            variable.value[j] += variable2.value[k]
                                        if variable.value[j] == 0:
                                            if variable.power[j] == 0:
                                                variable.value[j] = 1
                                                variable.power[j] = 1
                                                lChange1 = Function()
                                                lChange1.scope = variable.scope[j]
                                                lChange1.power = variable.power[j]
                                                lChange1.value = variable.value[j]
                                                lChange.append(lChange1)
                                            else:
                                                lRemoveScopes.append(
                                                    variable.scope[j])
                                                lRemoveScopes.append(
                                                    variable.beforeScope[j])
                                        else:
                                            lChange1 = Function()
                                            lChange1.scope = variable.scope[j]
                                            lChange1.power = variable.power[j]
                                            lChange1.value = variable.value[j]
                                            if variable.value[j] < 0 and variable.before[j] in ['-', '+']:
                                                lChange1.value = - \
                                                    1 * lChange1.value
                                                variable.value[j] = - \
                                                    1 * variable.value[j]
                                                lChange2 = Binary()
                                                lChange2.scope = variable.beforeScope[j]
                                                if variable.before[j] == '-':
                                                    lChange2.value = '+'
                                                elif variable.before[j] == '+':
                                                    lChange2.value = '-'
                                                lChange.append(lChange2)
                                            lChange.append(lChange1)

                                        rRemoveScopes.append(
                                            variable2.scope[k])
                                        rRemoveScopes.append(
                                            variable2.beforeScope[k])
                                        return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments

        elif isinstance(variable, Variable):
            for j in range(len(variable.power)):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if isinstance(variable2, Variable):
                            if variable2.power[0] == variable.power[0] and variable2.value[0] == variable.value[0]:
                                for k in range(len(variable2.value)):
                                    if variable2.before[k] == '-' and variable2.after[k] in ['-', '+', '']:
                                        comments.append("Moving " + r"$" + variable2.before[k] + variable2.__str__() + r"$" + " to LHS")
                                        if variable.before[j] == '-':
                                            variable.coefficient[j] -= variable2.coefficient[k]
                                        else:
                                            variable.coefficient[j] += variable2.coefficient[k]
                                        if variable.coefficient[j] == 0:
                                            lRemoveScopes.append(
                                                variable.scope[j])
                                            lRemoveScopes.append(
                                                variable.beforeScope[j])
                                        else:
                                            lChange1 = Function()
                                            lChange1.scope = variable.scope[j]
                                            lChange1.power = variable.power[j]
                                            lChange1.value = variable.value[j]
                                            lChange1.coefficient = variable.coefficient[j]
                                            if variable.coefficient[j] < 0 and variable.before[j] in ['-', '+']:
                                                lChange1.coefficient = - \
                                                    1 * lChange1.coefficient
                                                variable.coefficient[j] = - \
                                                    1 * \
                                                    variable.coefficient[j]
                                                lChange2 = Binary()
                                                lChange2.scope = variable.beforeScope[j]
                                                if variable.before[j] == '-':
                                                    lChange2.value = '+'
                                                elif variable.before[j] == '+':
                                                    lChange2.value = '-'
                                                lChange.append(lChange2)
                                            lChange.append(lChange1)

                                        rRemoveScopes.append(
                                            variable2.scope[k])
                                        rRemoveScopes.append(
                                            variable2.beforeScope[k])
                                        return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments
    return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments


###############
# Subtraction #
###############


def subtraction(tokens, direct=False):

    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(getLevelVariables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while '-' in availableOperations:
        _, tok, rem, change, com = expressionSubtraction(variables, tokens)
        tokens = changeToken(removeToken(tok, rem), change)
        if not tokens:
            tokens.append(Zero())
        animation.append(copy.deepcopy(tokens))
        comments.append(com)
        variables = getLevelVariables(tokens)
        availableOperations = getOperationsExpression(variables, tokens)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def subtractionEquation(lToks, rToks, direct=False):

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
    while '-' in availableOperations:
        _, tok, rem, change, com = expressionSubtraction(
            lVariables, lTokens)
        lTokens = changeToken(removeToken(tok, rem), change)
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
    while '-' in availableOperations:
        _, tok, rem, change, com = expressionSubtraction(
            rVariables, rTokens)
        rTokens = changeToken(removeToken(tok, rem), change)
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

    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    while '-' in availableOperations:
        lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, com = equationSubtraction(
            lVariables, lTokens, rVariables, rTokens)
        rTokens = changeToken(removeToken(rTokens, rRemoveScopes), rChange)
        lTokens = changeToken(removeToken(lTokens, lRemoveScopes), lChange)
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
        rVariables = getLevelVariables(rTokens)
        availableOperations = getOperationsEquation(
            lVariables, lTokens, rVariables, rTokens)

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
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def expressionSubtraction(variables, tokens):

    removeScopes = []
    change = []
    comments = []
    for i, variable in enumerate(variables):
        if isinstance(variable, Constant):
            if len(variable.value) > 1:
                constantAdd = []
                constant = []
                for j in range(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['-']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '+']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], const) + r"$" + " from " + r"$" + variable.__str__(const, const) + "}" + r"$")
                                if variable.before[const] == '+' or variable.before[const] == '':
                                    variable.value[const] -= variable.value[constantAdd[i]]
                                else:
                                    variable.value[const] += variable.value[constantAdd[i]]
                                if variable.value[const] == 0:
                                    if variable.power[const] == 0:
                                        variable.value[const] = 1
                                        variable.power[const] = 1
                                        change1 = Function()
                                        change1.scope = variable.scope[const]
                                        change1.power = variable.power[const]
                                        change1.value = variable.value[const]
                                        change.append(change1)
                                    else:
                                        removeScopes.append(
                                            variable.scope[const])
                                        removeScopes.append(
                                            variable.beforeScope[const])
                                else:
                                    change1 = Function()
                                    change1.scope = variable.scope[const]
                                    change1.power = variable.power[const]
                                    change1.value = variable.value[const]
                                    if variable.value[const] < 0 and variable.before[const] in ['-', '+']:
                                        change1.value = - \
                                            1 * change1.value
                                        variable.value[const] = - \
                                            1 * variable.value[const]
                                        change2 = Binary()
                                        change2.scope = variable.beforeScope[const]
                                        if variable.before[const] == '-':
                                            change2.value = '+'
                                        elif variable.before[const] == '+':
                                            change2.value = '-'
                                        change.append(change2)
                                    change.append(change1)
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                removeScopes.append(
                                    variable.beforeScope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        for const in constantAdd:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], const) + r"$" + " from " + r"$" + variable.__str__(const, const) + r"$")
                                variable.value[const] += variable.value[constantAdd[i]]
                                if variable.value[const] == 0:
                                    if variable.power[const] == 0:
                                        variable.value[const] = 1
                                        variable.power[const] = 1
                                        change1 = Function()
                                        change1.scope = variable.scope[const]
                                        change1.power = variable.power[const]
                                        change1.value = variable.value[const]
                                        change.append(change1)
                                    else:
                                        removeScopes.append(
                                            variable.scope[const])
                                        removeScopes.append(
                                            variable.beforeScope[const])
                                else:
                                    change1 = Function()
                                    change1.scope = variable.scope[const]
                                    change1.power = variable.power[const]
                                    change1.value = variable.value[const]
                                    if variable.value[const] < 0 and variable.before[const] in ['-', '+']:
                                        change1.value = - \
                                            1 * change1.value
                                        variable.value[const] = - \
                                            1 * variable.value[const]
                                        change2 = Binary()
                                        change2.scope = variable.beforeScope[const]
                                        if variable.before[const] == '-':
                                            change2.value = '+'
                                        elif variable.before[const] == '+':
                                            change2.value = '-'
                                        change.append(change2)
                                    change.append(change1)
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                removeScopes.append(
                                    variable.beforeScope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        i += 1
                elif len(constant) == 0 and len(constantAdd) > 1:
                    i = 0
                    while i < len(constantAdd):
                        for j, const in enumerate(constantAdd):
                            if i != j:
                                if variable.power[constantAdd[i]] == variable.power[const]:
                                    comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], const) + r"$" + " from " + r"$" + variable.__str__(const, const) + r"$")
                                    variable.value[const] += variable.value[constantAdd[i]]
                                    if variable.value[const] == 0:
                                        if variable.power[const] == 0:
                                            variable.value[const] = 1
                                            variable.power[const] = 1
                                            change1 = Function()
                                            change1.scope = variable.scope[const]
                                            change1.power = variable.power[const]
                                            change1.value = variable.value[const]
                                            change.append(change1)
                                        else:
                                            removeScopes.append(
                                                variable.scope[const])
                                            removeScopes.append(
                                                variable.beforeScope[const])
                                    else:
                                        change1 = Function()
                                        change1.scope = variable.scope[const]
                                        change1.power = variable.power[const]
                                        change1.value = variable.value[const]
                                        if variable.value[const] < 0 and variable.before[const] in ['-', '+']:
                                            change1.value = - \
                                                1 * change1.value
                                            variable.value[const] = - \
                                                1 * variable.value[const]
                                            change2 = Binary
                                            change2.scope = variable.beforeScope[const]
                                            if variable.before[const] == '-':
                                                change2.value = '+'
                                            elif variable.before[const] == '+':
                                                change2.value = '-'
                                            change.append(change2)
                                        change.append(change1)
                                    removeScopes.append(
                                        variable.scope[constantAdd[i]])
                                    removeScopes.append(
                                        variable.beforeScope[constantAdd[i]])
                                    return variables, tokens, removeScopes, change, comments
                        i += 1

        elif isinstance(variable, Variable):
            if len(variable.power) > 1:
                constantAdd = []
                constant = []
                for j in range(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['-']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '+']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], constantAdd[i]) + r"$" + " from " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], const) + r"$")
                                if variable.before[const] == '+' or variable.before[const] == '':
                                    variable.coefficient[const] -= variable.coefficient[constantAdd[i]]
                                else:
                                    variable.coefficient[const] += variable.coefficient[constantAdd[i]]
                                if variable.coefficient[const] == 0:
                                    removeScopes.append(
                                        variable.scope[const])
                                    removeScopes.append(
                                        variable.beforeScope[const])
                                else:
                                    change1 = Function()
                                    change1.scope = variable.scope[const]
                                    change1.power = variable.power[const]
                                    change1.value = variable.value
                                    change1.coefficient = variable.coefficient[const]
                                    if variable.coefficient[const] < 0 and variable.before[const] in ['-', '+']:
                                        change1.coefficient = - \
                                            1 * change1.coefficient
                                        variable.coefficient[const] = - \
                                            1 * variable.coefficient[const]
                                        change2 = Binary()
                                        change2.scope = variable.beforeScope[const]
                                        if variable.before[const] == '-':
                                            change2.value = '+'
                                        elif variable.before[const] == '+':
                                            change2.value = '-'
                                        change.append(change2)
                                    change.append(change1)
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                removeScopes.append(
                                    variable.beforeScope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        for const in constantAdd:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], constantAdd[i]) + r"$" + " from " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], const) + r"$")
                                variable.coefficient[const] += variable.coefficient[constantAdd[i]]
                                if variable.coefficient[const] == 0:
                                    removeScopes.append(
                                        variable.scope[const])
                                    removeScopes.append(
                                        variable.beforeScope[const])
                                else:
                                    change1 = Function()
                                    change1.scope = variable.scope[const]
                                    change1.power = variable.power[const]
                                    change1.value = variable.value
                                    change1.coefficient = variable.coefficient[const]
                                    if variable.coefficient[const] < 0 and variable.before[const] in ['-', '+']:
                                        change1.coefficient = - \
                                            1 * change1.coefficient
                                        variable.coefficient[const] = - \
                                            1 * variable.coefficient[const]
                                        change2 = Binary()
                                        change2.scope = variable.beforeScope[const]
                                        if variable.before[const] == '-':
                                            change2.value = '+'
                                        elif variable.before[const] == '+':
                                            change2.value = '-'
                                        change.append(change2)
                                    change.append(change1)
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                removeScopes.append(
                                    variable.beforeScope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        i += 1
                elif len(constant) == 0 and len(constantAdd) > 1:
                    i = 0
                    while i < len(constantAdd):
                        for j, const in enumerate(constantAdd):
                            if i != j:
                                if variable.power[constantAdd[i]] == variable.power[const]:
                                    comments.append("Subtracting " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], constantAdd[i]) + r"$" + " from " + r"$" + variable.__str__(constantAdd[i], constantAdd[i], const) + r"$")
                                    variable.coefficient[const] += variable.coefficient[constantAdd[i]]
                                    if variable.coefficient[const] == 0:
                                        removeScopes.append(
                                            variable.scope[const])
                                        removeScopes.append(
                                            variable.beforeScope[const])
                                    else:
                                        change1 = Function()
                                        change1.scope = variable.scope[const]
                                        change1.power = variable.power[const]
                                        change1.value = variable.value
                                        change1.coefficient = variable.coefficient[const]
                                        if variable.coefficient[const] < 0 and variable.before[const] in ['-', '+']:
                                            change1.coefficient = - \
                                                1 * change1.coefficient
                                            variable.coefficient[const] = - \
                                                1 * \
                                                variable.coefficient[const]
                                            change2 = Binary()
                                            change2.scope = variable.beforeScope[const]
                                            if variable.before[const] == '-':
                                                change2.value = '+'
                                            elif variable.before[const] == '+':
                                                change2.value = '-'
                                            change.append(change2)
                                        change.append(change1)
                                    removeScopes.append(
                                        variable.scope[constantAdd[i]])
                                    removeScopes.append(
                                        variable.beforeScope[constantAdd[i]])
                                    return variables, tokens, removeScopes, change, comments
                        i += 1
        elif isinstance(variable, Expression):
            pass
    return variables, tokens, removeScopes, change, comments


def equationSubtraction(lVariables, lTokens, rVariables, rTokens):

    lRemoveScopes = []
    rRemoveScopes = []
    lChange = []
    rChange = []
    comments = []
    for variable in lVariables:
        if isinstance(variable, Constant):
            for j, _ in enumerate(variable.value):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if isinstance(variable2, Constant):
                            if variable2.power[0] == variable.power[0]:
                                for k, _ in enumerate(variable2.value):
                                    if variable2.before[k] in ['+', ''] and variable2.after[k] in ['-', '+', '']:
                                        comments.append(
                                            "Moving " + r"$" + variable2.before[k] + variable2.__str__() + r"$" + " to LHS")
                                        if variable.before[j] == '-':
                                            variable.value[j] += variable2.value[k]
                                        else:
                                            variable.value[j] -= variable2.value[k]
                                        if variable.value[j] == 0:
                                            if variable.power == 0:
                                                variable.value = 1
                                                variable.power = 1
                                                lChange1 = Function()
                                                lChange1.scope = variable.scope[j]
                                                lChange1.power = variable.power[j]
                                                lChange1.value = variable.value[j]
                                                lChange.append(lChange1)
                                            else:
                                                lRemoveScopes.append(
                                                    variable.scope[j])
                                                lRemoveScopes.append(
                                                    variable.beforeScope[j])
                                        else:
                                            lChange1 = Function()
                                            lChange1.scope = variable.scope[j]
                                            lChange1.power = variable.power[j]
                                            lChange1.value = variable.value[j]
                                            if variable.value[j] < 0 and variable.before[j] in ['-', '+']:
                                                lChange1.value = - \
                                                    1 * lChange1.value
                                                variable.value[j] = - \
                                                    1 * variable.value[j]
                                                lChange2 = Binary()
                                                lChange2.scope = variable.beforeScope[j]
                                                if variable.before[j] == '-':
                                                    lChange2.value = '+'
                                                elif variable.before[j] == '+':
                                                    lChange2.value = '-'
                                                lChange.append(lChange2)
                                            lChange.append(lChange1)

                                        rRemoveScopes.append(
                                            variable2.scope[k])
                                        rRemoveScopes.append(
                                            variable2.beforeScope[k])
                                        return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments
        elif isinstance(variable, Variable):
            for j, _ in enumerate(variable.power):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if isinstance(variable2, Variable):
                            if variable2.power[0] == variable.power[0] and variable2.value[0] == variable.value[0]:
                                for k, _ in enumerate(variable2.value):
                                    if variable2.before[k] in ['+', ''] and variable2.after[k] in ['-', '+', '']:
                                        comments.append("Moving " + r"$" + variable2.before[k] + variable2.__str__() + r"$" + " to LHS")
                                        if variable.before[j] == '-':
                                            variable.coefficient[j] += variable2.coefficient[k]
                                        else:
                                            variable.coefficient[j] -= variable2.coefficient[k]
                                        if variable.coefficient[j] == 0:
                                            lRemoveScopes.append(
                                                variable.scope[j])
                                            lRemoveScopes.append(
                                                variable.beforeScope[j])
                                        else:
                                            lChange1 = Function()
                                            lChange1.scope = variable.scope[j]
                                            lChange1.power = variable.power[j]
                                            lChange1.value = variable.value[j]
                                            lChange1.coefficient = variable.coefficient[j]
                                            if variable.coefficient[j] < 0 and variable.before[j] in ['-', '+']:
                                                lChange1.coefficient = - \
                                                    1 * lChange1.coefficient
                                                variable.coefficient[j] = - \
                                                    1 * \
                                                    variable.coefficient[j]
                                                lChange2 = Binary()
                                                lChange2.scope = variable.beforeScope[j]
                                                if variable.before[j] == '-':
                                                    lChange2.value = '+'
                                                elif variable.before[j] == '+':
                                                    lChange2.value = '-'
                                                lChange.append(lChange2)
                                            lChange.append(lChange1)

                                        rRemoveScopes.append(
                                            variable2.scope[k])
                                        rRemoveScopes.append(
                                            variable2.beforeScope[k])
                                        return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments
    return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, comments
