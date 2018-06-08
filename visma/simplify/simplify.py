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
from visma.functions.structure import Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.io.checks import is_equation, get_level_variables, getOperationsEquation, getOperationsExpression
from visma.io.parser import tokensToString
from visma.simplify.addsub import addition, addition_equation, subtraction, subtraction_equation
from visma.simplify.muldiv import multiplication, multiplication_equation, multiply_expressions, division, division_equation


def move_rTokens_to_lTokens(lTokens, rTokens):
    if len(lTokens) == 0 and len(rTokens) > 0:
        return rTokens, lTokens
    elif is_equation(lTokens, rTokens):
        return lTokens, rTokens
    elif len(lTokens) != 0:
        for i, token in enumerate(rTokens):
            if i == 0 and token.__class__ != Binary:
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


def simplify_equation(lToks, rToks):
    lTokens = copy.deepcopy(lToks)
    rTokens = copy.deepcopy(rToks)
    animation = []
    comments = [[]]
    lVariables = []
    lVariables.extend(get_level_variables(lTokens))
    rVariables = []
    rVariables.extend(get_level_variables(rTokens))
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
    availableOperations = getOperationsEquation(
        lVariables, lTokens, rVariables, rTokens)
    while len(availableOperations) > 0:
        if '/' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = division_equation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '*' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = multiplication_equation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '+' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = addition_equation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)
        elif '-' in availableOperations:
            lTokens, rTokens, availableOperations, token_string, anim, com = subtraction_equation(
                lTokens, rTokens)
            animation.pop(len(animation) - 1)
            animation.extend(anim)
            comments.extend(com)

        lVariables = get_level_variables(lTokens)
        rVariables = get_level_variables(rTokens)
        availableOperations = getOperationsEquation(
            lVariables, lTokens, rVariables, rTokens)

    moved = False
    if len(rTokens) > 0:
        moved = True
        lTokens, rTokens = move_rTokens_to_lTokens(lTokens, rTokens)
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
    if moved:
        animation.append(copy.deepcopy(tokenToStringBuilder))
        comments.append(['Moving the rest of variables/constants to LHS'])

    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def simplify(tokens):
    tokens_orig = copy.deepcopy(tokens)
    animation = [tokens_orig]
    variables = []
    comments = [[]]
    variables.extend(get_level_variables(tokens))
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
    token_string = tokensToString(tokens)
    return tokens, availableOperations, token_string, animation, comments


def define_scope_variable(variable, scope):
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


def define_scope_constant(constant, scope):
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


def define_scope(tokens, scope=None):
    if scope is None:
        scope = []
    i = 0
    for token in tokens:
        local_scope = copy.deepcopy(scope)
        local_scope.extend(i)
        token.scope = local_scope
        if isinstance(token, Variable):
            token = define_scope_variable(token, copy.deepcopy(local_scope))
        elif isinstance(token, Constant):
            token = define_scope_constant(token, copy.deepcopy(local_scope))
        elif isinstance(token, Expression):
            token.tokens = define_scope(token.tokens, local_scope)
        elif isinstance(token, Binary):
            pass
        i += 1
    return tokens


if __name__ == '__main__':

    multiply_expressions({'tokens': [{'coefficient': 1, 'scope': [0, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [0, 1], 'type': Binary, 'value': '-'}, {'scope': [0, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [0], 'coefficient': 1, 'type': Expression}, {
                         'tokens': [{'coefficient': 1, 'scope': [1, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1, 1], 'type': Binary, 'value': '+'}, {'scope': [1, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [1], 'coefficient': 1, 'type': Expression})
