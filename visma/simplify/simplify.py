"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module aims to create a sort of middleware module to call other modules which can handle/solve different types of equations and expressions.
This module is also responsible for performing tasks like simplification of equations/expressions, and individual functions like, addition, subtraction, multiplication and division in an equation/expression.
Communicates with polynomial roots module, to check if roots of the equation can be found.
Note: Please try to maintain proper documentation
Logic Description:
"""

import copy
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.functions.trigonometry import Trigonometric
from visma.io.checks import isEquation, getLevelVariables, getOperationsEquation, getOperationsExpression, postSimplification
from visma.io.parser import tokensToString
from visma.io.tokenize import tokenizer
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.functions.structure import Expression


def moveRTokensToLTokens(lTokens, rTokens):
    """Moves tokens in RHS to LHS

    Arguments:
        ltokens {list} -- LHS tokens list
        rtokens {list} -- RHS tokens list

    Returns:
        ltokens {list} -- LHS tokens list
        rtokens {list} -- RHS tokens list
    """
    if len(lTokens) == 0 and len(rTokens) > 0:
        return rTokens, lTokens
    elif isEquation(lTokens, rTokens):
        return lTokens, rTokens
    elif len(lTokens) != 0:
        for i, token in enumerate(rTokens):
            if i == 0 and not isinstance(token, Binary):
                binary = Binary()
                binary.value = '-'
                binary.scope = copy.copy(token.scope)
                binary.scope[-1] -= 1
                lTokens.append(binary)
            if isinstance(token, Binary):
                if token.value in ['+', '-']:
                    if token.value == '-':
                        token.value = '+'
                    else:
                        token.value = '-'
            elif isinstance(token, Constant):
                if token.value < 0:
                    if isinstance(lTokens[-1], Binary):
                        if lTokens[-1].value == '-':
                            token.value *= -1
                            lTokens[-1].value = '+'
                        elif lTokens[-1].value == '+':
                            token.value *= -1
                            lTokens[-1].value = '-'
            elif isinstance(token, Variable):
                if token.coefficient < 0:
                    if isinstance(lTokens[-1], Binary):
                        if lTokens[-1].value == '-':
                            token.coefficient *= -1
                            lTokens[-1].value = '+'
                        elif lTokens[-1].value == '+':
                            token.coefficient *= -1
                            lTokens[-1].value = '-'
            lTokens.append(token)
    rTokens = []
    return lTokens, rTokens


def equationAnimationBuilder(lTokens, rTokens):
    """Given LHS & RHS tokens for an equation it builds the tokens of complete equation

    Arguments:
        lTokens {list} -- Tokens of LHS
        rTokens {list} -- Tokens of RHS

    Returns:
        animBulder {list} -- list of tokens of complete equation
    """
    animBuilder = []
    lToks = copy.deepcopy(lTokens)
    rToks = copy.deepcopy(rTokens)
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
    return animBuilder


def simplifyEquation(lToks, rToks):
    """Simplifies given equation tokens

    Arguments:
        lToks {list} -- LHS tokens list
        rToks {list} -- RHS tokens list

    Returns:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        availableOperations {list} -- list of operations
        token_string {string} -- simplified result in string
        animation {list} -- list of equation simplification progress
        comments {list} -- list of solution steps
    """
    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    animation = []
    comments = []
    comments += [[]]
    animation.append(equationAnimationBuilder(lTokens, rTokens))
    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    expressionPresent = False
    for toks in lTokens:
        if isinstance(toks, Expression):
            expressionPresent = True
    if expressionPresent:
        lTokens, _, _, _, _ = expressionSimplification(lTokens, [], lTokens)
        comments += [['Opening brackets in the LHS']]
        animation.append(equationAnimationBuilder(lTokens, rTokens))
    expressionPresent = False
    for toks in rTokens:
        if isinstance(toks, Expression):
            expressionPresent = True
    if expressionPresent:
        rTokens, _, _, _, _ = expressionSimplification(rTokens, [], rTokens)
        comments += [['Opening brackets in the RHS']]
        animation.append(equationAnimationBuilder(lTokens, rTokens))
    lVariables = []
    lVariables.extend(getLevelVariables(lTokens))
    rVariables = []
    rVariables.extend(getLevelVariables(rTokens))
    availableOperations = getOperationsEquation(lVariables, lTokens, rVariables, rTokens)
    while len(availableOperations) > 0:
        if '/' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = divisionEquation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '*' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = multiplicationEquation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '+' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = additionEquation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '-' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = subtractionEquation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        lVariables = getLevelVariables(lTokens)
        rVariables = getLevelVariables(rTokens)
        availableOperations = getOperationsEquation(lVariables, lTokens, rVariables, rTokens)
    moved = False
    if len(rTokens) > 0:
        moved = True
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
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
    if moved:
        animation.append(copy.deepcopy(tokenToStringBuilder))
        comments.append(['Moving the rest of variables/constants to LHS'])
    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def simplify(tokens):
    """
    Main simplify function which is called from driver modules

    Arguments:
        tokens {list} -- list of tokens

    Returns:
        tokens {list} -- list of simplified
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process

    """
    tokens_orig = copy.deepcopy(tokens)
    animation = [tokens_orig]
    comments = [[]]
    tokens, availableOperations, token_string, anim1, comment1 = expressionSimplification(tokens_orig, [], tokens)
    animation.extend(anim1)
    comments.extend(comment1)
    return tokens, availableOperations, token_string, animation, comments


def expressionSimplification(tokens_now, scope, tokens1):
    '''Makes an input equation free from Expressions, i.e. solving each Expression recursively to convert them in other tokens.

    Arguments:
        tokens_now {list} -- list of original tokens as function gets called recursively
        scope {list} -- integers (bounds) indicating which Expression we are currently solving
        tokens1 {list} -- list of current tokens as function gets called recursively

    Returns:
        simToks {list} -- list of simplified tokens of each Expression
        availableOperations {list} -- list of operations which can be performed on a equation token
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    '''
    animation = []
    comments = []
    pfTokens = []
    i = 0
    while(i < len(tokens1)):
        if (i + 1 < len(tokens1)):
            if isinstance(tokens1[i], Binary) and tokens1[i].value == '^':
                if isinstance(tokens1[i - 1], Expression):
                    tokens1[i - 1].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i - 1].tokens)
                if isinstance(tokens1[i + 1], Expression):
                    tokens1[i + 1].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i + 1].tokens)
                    if len(tokens1[i + 1].tokens) == 1 and isinstance(tokens1[i + 1].tokens[0], Constant):
                        tokens1[i + 1] = Constant(tokens1[i + 1].tokens[0].calculate(), 1, 1)
            if (isinstance(tokens1[i], Binary) and tokens1[i].value == '^') and isinstance(tokens1[i + 1], Constant):
                if float(tokens1[i + 1].calculate()).is_integer():
                    rep = int(tokens1[i + 1].calculate())
                    for _ in range(rep - 1):
                        pfTokens.extend([Binary('*'), tokens1[i - 1]])
                    i += 1
                else:
                    pfTokens.append(tokens1[i])
            else:
                pfTokens.append(tokens1[i])
        else:
            pfTokens.append(tokens1[i])
        i += 1
    tokens1 = copy.deepcopy(pfTokens)
    animation.append(pfTokens)
    comments.append(['Expanding the powers of expressions'])
    mulFlag = True
    expressionMultiplication = False
    # Check for the case: {Non-Expression} * {Expression}
    for _ in range(50):
        for i, _ in enumerate(tokens1):
            mulFlag = False
            if isinstance(tokens1[i], Expression):
                if (i > 1):
                    if (tokens1[i - 1].value == '*'):
                        scope.append(i)
                        tokens1[i].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i].tokens)
                        if isinstance(tokens1[i - 2], Expression):
                            scope.append(i - 2)
                            tokens1[i - 2].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i - 2].tokens)
                        a = tokens1[i - 2]
                        b = tokens1[i]
                        c = a * b
                        mulFlag = True
                        expressionMultiplication = True
                        if isinstance(c, Expression):
                            scope.append(i)
                            c.tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, c.tokens)
                        tokens1[i] = c
                        del tokens1[i - 1]
                        del tokens1[i - 2]
                        break
    trigonometricError = False
    # Check for the case: {Expression} * {Non-Expression}
    if not trigonometricError:
        for _ in range(50):
            for i, _ in enumerate(tokens1):
                mulFlag = False
                if isinstance(tokens1[i], Expression):
                    if i + 2 < len(tokens1):
                        if (tokens1[i + 1].value == '*'):
                            scope.append(i)
                            tokens1[i].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i].tokens)
                            if isinstance(tokens1[i + 2], Expression):
                                scope.append(i + 2)
                                tokens1[i + 2].tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i + 2].tokens)
                            a = tokens1[i + 2]
                            b = tokens1[i]
                            trigonometricError = False
                            for ec in b.tokens:
                                if isinstance(ec, Trigonometric):
                                    trigonometricError = True
                                    break
                            if not trigonometricError:
                                c = a * b
                                mulFlag = True
                                expressionMultiplication = True
                                if isinstance(c, Expression):
                                    scope.append(i)
                                    c.tokens, _, _, _, _ = expressionSimplification(tokens_now, scope, c.tokens)
                                tokens1[i] = c
                                del tokens1[i + 1]
                                del tokens1[i + 1]
                                break
            if not mulFlag:
                break
    if expressionMultiplication:
        animation.append(tokens1)
        comments.append(['Multiplying expressions'])
    # TODO: Implement verbose multiplication steps.
    simToks = []
    expressionPresent = False
    for i, _ in enumerate(tokens1):
        if isinstance(tokens1[i], Expression):
            expressionPresent = True
            scope.append(i)
            newToks, _, _, _, _ = expressionSimplification(tokens_now, scope, tokens1[i].tokens)
            if not simToks:
                simToks.extend(newToks)
            elif (simToks[len(simToks) - 1].value == '+'):
                if isinstance(newToks[0], Constant):
                    if (newToks[0].value < 0):
                        simToks.pop()
                simToks.extend(newToks)
            elif (simToks[len(simToks) - 1].value == '-'):
                for _, x in enumerate(newToks):
                    if x.value == '+':
                        x.value = '-'
                    elif x.value == '-':
                        x.value = '+'
                if (isinstance(newToks[0], Constant)):
                    if (newToks[0].value < 0):
                        simToks[-1].value = '+'
                        newToks[0].value = abs(newToks[0].value)
                elif (isinstance(newToks[0], Variable)):
                    if (newToks[0].coefficient < 0):
                        simToks[-1].value = '+'
                        newToks[0].coefficient = abs(newToks[0].coefficient)
                simToks.extend(newToks)
        else:
            simToks.extend([tokens1[i]])
    simToks = tokenizer(tokensToString(simToks))
    if expressionPresent:
        animation += [simToks]
        comments += [['Opening up all the brackets']]

    # TODO: Implement Trigonometric functions in the simplify module.
    trigonometricError = False
    for tk in simToks:
        if isinstance(tk, Trigonometric):
            trigonometricError = True
            break
    if not trigonometricError:
        if scope == []:
            simToks, availableOperations, token_string, animExtra, commentExtra = simplifification(simToks)
            animExtra.pop(0)
            animation += animExtra
            comments += commentExtra
        else:
            availableOperations = ''
            token_string = ''
    else:
        availableOperations = []
        token_string = tokensToString(simToks)
    # TODO: Implement verbose steps in simplification of Expressions (steps shown can be varied depending on length of expression)
    if scope != []:
        scope.pop()
    return simToks, availableOperations, token_string, animation, comments


def simplifification(tokens):
    """Simplifies given expression tokens

    Arguments:
        tokens {list} -- tokens list

    Returns:
        tokens {list} -- tokens list
        availableOperations {list} -- list of operations
        token_string {string} -- simplified result in string
        animation {list} -- list of equation simplification progress
        comments {list} -- list of solution steps
    """
    tokens_orig = copy.deepcopy(tokens)
    animation = [tokens_orig]
    variables = []
    comments = []
    variables.extend(getLevelVariables(tokens))
    availableOperations = getOperationsExpression(variables, tokens)
    while len(availableOperations) > 0:
        if '/' in availableOperations:
            tokens_temp = copy.deepcopy(tokens)
            tokens, availableOperations, token_string, anim, com = division(
                tokens_temp)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '*' in availableOperations:
            tokens_temp = copy.deepcopy(tokens)
            tokens, availableOperations, token_string, anim, com = multiplication(
                tokens_temp)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '+' in availableOperations:
            tokens_temp = copy.deepcopy(tokens)
            tokens, availableOperations, token_string, anim, com = addition(
                tokens_temp)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '-' in availableOperations:
            tokens_temp = copy.deepcopy(tokens)
            tokens, availableOperations, token_string, anim, com = subtraction(
                tokens_temp)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
    tokens, animation = postSimplification(tokens, animation)
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


'''
def defineScopeVariable(variable, scope):
    token = copy.deepcopy(variable)
    local_scope = copy.deepcopy(scope)
    if isinstance(token.value, list):
        for j, val in enumerate(token.value):
            if val.__class__ in [Binary, Variable, Constant, Expression]:
                local_scope_value = copy.deepcopy(local_scope)
                local_scope_value.extend(-1)
                local_scope_value.extend(j)
                val.scope = local_scope_value

    if isinstance(token.power, list):
        for j, val in enumerate(token.value):
            if val.__class__ in [Binary, Variable, Constant, Expression]:
                local_scope_value = copy.deepcopy(local_scope)
                local_scope_value.extend(-2)
                local_scope_value.extend(j)
                val.scope = local_scope_value

    return token


def defineScopeConstant(constant, scope):
    token = copy.deepcopy(constant)
    local_scope = copy.deepcopy(scope)
    if isinstance(token.value, list):
        for j, val in enumerate(token.value):
            if val.__class__ in [Binary, Variable, Constant, Expression]:
                local_scope_value = copy.deepcopy(local_scope)
                local_scope_value.extend(-1)
                local_scope_value.extend(j)
                val.scope = local_scope_value

    if isinstance(token.power, list):
        for j, val in enumerate(token.value):
            if val.__class__ in [Binary, Variable, Constant, Expression]:
                local_scope_value = copy.deepcopy(local_scope)
                local_scope_value.extend(-2)
                local_scope_value.extend(j)
                val.scope = local_scope_value
    return token


def defineScope(tokens, scope=None):
    if scope is None:
        scope = []
    i = 0
    for token in tokens:
        local_scope = copy.deepcopy(scope)
        local_scope.extend(i)
        token.scope = local_scope
        if isinstance(token, Variable):
            token = defineScopeVariable(token, copy.deepcopy(local_scope))
        elif isinstance(token, Constant):
            token = defineScopeConstant(token, copy.deepcopy(local_scope))
        elif isinstance(token, Expression):
            token.tokens = defineScope(token.tokens, local_scope)
        elif isinstance(token, Binary):
            pass
        i += 1
    return tokens
'''
