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

import math
import copy
from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.io.tokenize import is_number, get_num


def get_variable_string(variable, power):
    string = ""
    for j, val in enumerate(variable):
        string += "(" + val + ")"
        if power[j] != 1:
            string += "^(" + str(power[j]) + ")"
    return string


def is_equation(lTokens, rTokens):
    if len(lTokens) > 0 and len(rTokens) == 1:
        if rTokens[0].__class__ == Constant:
            if rTokens[0].value == 0:
                return True
    return False


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
            if token.__class__ == Binary:
                if token.value in ['+', '-']:
                    if token.value == '-':
                        token.value = '+'
                    else:
                        token.value = '-'
            elif token.__class__ == Constant:
                if token.value < 0:
                    if lTokens[-1].__class__ == Binary:
                        if lTokens[-1].value == '-':
                            token.value *= -1
                            lTokens[-1].value = '+'
                        elif lTokens[-1].value == '+':
                            token.value *= -1
                            lTokens[-1].value = '-'
            elif token.__class__ == Variable:
                if token.coefficient < 0:
                    if lTokens[-1].__class__ == Binary:
                        if lTokens[-1].value == '-':
                            token.coefficient *= -1
                            lTokens[-1].value = '+'
                        elif lTokens[-1].value == '+':
                            token.coefficient *= -1
                            lTokens[-1].value = '-'
            lTokens.append(token)
    rTokens = []
    return lTokens, rTokens


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
        self.availableOperations.extend(get_available_operations_equations(self.lVariables, self.lTokens, self.rVariables, self.rTokens))
        # print self.availableOperations


def find_solve_for(lTokens, rTokens=None, variables=None):
    if rTokens is None:
        rTokens = []
    if variables is None:
        variables = []
    for token in lTokens:
        if token.__class__ == Variable:
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif token.__class__ == Expression:
            variables.extend(find_solve_for(token.tokens))

    for token in rTokens:
        if token.__class__ == Variable:
            for val in token.value:
                if val not in variables:
                    variables.append(val)
        elif token.__class__ == Expression:
            variables.extend(find_solve_for(token.tokens, [], variables))
    return variables


class ExpressionCompatibility(object):
    """docstring for ExpressionCompatibility"""

    def __init__(self, tokens):
        super(ExpressionCompatibility, self).__init__()
        self.tokens = tokens
        self.variables = []
        self.variables.extend(get_level_variables(self.tokens))
        self.availableOperations = get_available_operations(self.variables, self.tokens)


def check_solve_for(lTokens, rTokens):
    for token in lTokens:
        if token.__class__ == Variable:
            return True
        elif token.__class__ == Expression:
            if check_solve_for(token.tokens):
                return True

    for token in rTokens:
        if token.__class__ == Variable:
            return True
        elif token.__class__ == Expression:
            if check_solve_for(token.tokens):
                return True


def tokens_to_string(tokens):
    token_string = ''
    for token in tokens:
        if token.__class__ == Constant:
            if isinstance(token.value, list):
                for j, val in token.value:
                    if token['power'][j] != 1:
                        token_string += (str(val) + '^(' + str(token.power[j]) + ') ')
                    else:
                        token_string += str(val)
            elif is_number(token.value):
                if token.power != 1:
                    token_string += (str(token.value) + '^(' + str(token.power) + ') ')
                else:
                    token_string += str(token.value)
        elif token.__class__ == Variable:
            if token.coefficient == 1:
                pass
            elif token.coefficient == -1:
                token_string += ' -'
            else:
                token_string += str(token.coefficient)
            for j, val in enumerate(token.value):
                if token.power[j] != 1:
                    token_string += (str(val) + '^(' + str(token.power[j]) + ') ')
                else:
                    token_string += str(val)
        elif token.__class__ == Binary:
            token_string += ' ' + str(token.value) + ' '
        elif token.__class__ == Expression:
            token_string += ' ( '
            token_string += tokens_to_string(token.tokens)
            token_string += ' ) '
            if token.power != 1:
                token_string += '^(' + str(token.power) + ') '
        elif token.__class__ == Sqrt:
            token_string += 'sqrt['
            if token.power.__class__ == Constant:
                token_string += tokens_to_string([token.power])
            elif token.power.__class__ == Variable:
                token_string += tokens_to_string([token.power])
            elif token.power.__class__ == Expression:
                token_string += tokens_to_string(token.power.tokens)
            token_string += ']('
            if token.expression.__class__ == Constant:
                token_string += tokens_to_string([token.expression])
            elif token.expression.__class__ == Variable:
                token_string += tokens_to_string([token.expression])
            elif token.expression.__class__ == Expression:
                token_string += tokens_to_string(token.expression.tokens)

            token_string += ') '
    return token_string


def test():
    tokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [5.0], 'value': ['x']}, {'scope': [
        1], 'type': 'binary', 'value': '-'}, {'coefficient': 1, 'scope': [2], 'type': 'variable', 'power': [4.0], 'value': ['x']}]
    # tokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'value': 6.0, 'power': 1}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'value': 3.0, 'power': 1}, {'scope': [5], 'type': 'binary', 'value': '+'}, {'scope': [6], 'type': 'constant', 'value': 2.0, 'power': 1}, {'scope': [7], 'type': 'binary', 'value': '-'}, {'coefficient': 2.0, 'scope': [8], 'type': 'variable', 'power': [1], 'value': ['x']}]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
    print(variables, availableOperations)
    # var, tok, rem, change = expression_subtraction(variables, tokens)
    # print tokens_to_string(change_token(remove_token(tok, rem), [change]))
    # print tokens_to_string(remove_token(tok, rem))


def remove_token(tokens, scope, scope_times=0):
    for remScope in scope:
        for i, token in enumerate(tokens):
            if token.__class__ == Constant or token.__class__ == Variable:
                if token.scope == remScope:
                    tokens.pop(i)
                    break
            elif token.__class__ == Binary:
                if token.scope == remScope:
                    tokens.pop(i)
                    break
            elif token.__class__ == Expression:
                if scope_times + 1 == len(remScope):
                    if token.scope == remScope:
                        tokens.pop(i)
                        break
                elif token.scope == remScope[0:(scope_times + 1)]:
                    token.tokens = remove_token(
                        token.tokens, scope, scope_times + 1)
                    break

    return tokens


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
    availableOperations = get_available_operations_equations(
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
        availableOperations = get_available_operations_equations(
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

    token_string = tokens_to_string(tokenToStringBuilder)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def simplify(tokens):
    tokens_orig = copy.deepcopy(tokens)
    animation = [tokens_orig]
    variables = []
    comments = [[]]
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
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
    token_string = tokens_to_string(tokens)
    return tokens, availableOperations, token_string, animation, comments


def addition_equation(lToks, rToks, direct=False):
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
    availableOperations = get_available_operations(lVariables, lTokens)
    while '+' in availableOperations:
        var, tok, rem, change, com = expression_addition(lVariables, lTokens)
        lTokens = change_token(remove_token(tok, rem), change)
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
        availableOperations = get_available_operations(lVariables, lTokens)

    availableOperations = get_available_operations(rVariables, rTokens)
    while '+' in availableOperations:
        var, tok, rem, change, com = expression_addition(rVariables, rTokens)
        rTokens = change_token(remove_token(tok, rem), change)
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
        availableOperations = get_available_operations(rVariables, rTokens)

    availableOperations = get_available_operations_equations(
        lVariables, lTokens, rVariables, rTokens)
    while '+' in availableOperations:
        lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, com = equation_addition(
            lVariables, lTokens, rVariables, rTokens)
        rTokens = change_token(remove_token(rTokens, rRemoveScopes), rChange)
        lTokens = change_token(remove_token(lTokens, lRemoveScopes), lChange)
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
        rVariables = get_level_variables(rTokens)
        availableOperations = get_available_operations_equations(
            lVariables, lTokens, rVariables, rTokens)

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
    token_string = tokens_to_string(tokenToStringBuilder)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def addition(tokens, direct=False):
    animation = [copy.deepcopy(tokens)]
    variables = []
    comments = []
    if direct:
        comments = [[]]
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
    while '+' in availableOperations:
        var, tok, rem, change, com = expression_addition(variables, tokens)
        tokens = change_token(remove_token(tok, rem), change)
        animation.append(copy.deepcopy(tokens))
        comments.append(com)
        variables = get_level_variables(tokens)
        availableOperations = get_available_operations(variables, tokens)
    token_string = tokens_to_string(tokens)
    return tokens, availableOperations, token_string, animation, comments


def subtraction_equation(lToks, rToks, direct=False):
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
    availableOperations = get_available_operations(lVariables, lTokens)
    while '-' in availableOperations:
        var, tok, rem, change, com = expression_subtraction(
            lVariables, lTokens)
        lTokens = change_token(remove_token(tok, rem), change)
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
        availableOperations = get_available_operations(lVariables, lTokens)

    availableOperations = get_available_operations(rVariables, rTokens)
    while '-' in availableOperations:
        var, tok, rem, change, com = expression_subtraction(
            rVariables, rTokens)
        rTokens = change_token(remove_token(tok, rem), change)
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
        availableOperations = get_available_operations(rVariables, rTokens)

    availableOperations = get_available_operations_equations(
        lVariables, lTokens, rVariables, rTokens)
    while '-' in availableOperations:
        lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange, com = equation_subtraction(
            lVariables, lTokens, rVariables, rTokens)
        rTokens = change_token(remove_token(rTokens, rRemoveScopes), rChange)
        lTokens = change_token(remove_token(lTokens, lRemoveScopes), lChange)
        comments.append(com)
        animBuilder = copy.deepcopy(lTokens)
        l = len(lTokens)
        equalTo = Binary()
        equalTo.scope = [l]
        equalTo.value = '='
        animBuilder.append(equalTo)
        if len(rTokens) == 0:
            zero = Zero()
            zero.value = 0
            zero.power = 1
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = get_level_variables(lTokens)
        rVariables = get_level_variables(rTokens)
        availableOperations = get_available_operations_equations(
            lVariables, lTokens, rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    l = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Constant()
        zero.scope = [l + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokens_to_string(tokenToStringBuilder)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def subtraction(tokens, direct=False):
    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
    while '-' in availableOperations:
        var, tok, rem, change, com = expression_subtraction(variables, tokens)
        tokens = change_token(remove_token(tok, rem), change)
        animation.append(copy.deepcopy(tokens))
        comments.append(com)
        variables = get_level_variables(tokens)
        availableOperations = get_available_operations(variables, tokens)
    token_string = tokens_to_string(tokens)
    return tokens, availableOperations, token_string, animation, comments


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
        zero.value = 0
        zero.power = 1
        zero.scope = [l + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(get_level_variables(lTokens))
    rVariables = []
    rVariables.extend(get_level_variables(rTokens))
    availableOperations = get_available_operations(lVariables, lTokens)
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
            zero = Constant()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = get_level_variables(lTokens)
        availableOperations = get_available_operations(lVariables, lTokens)

    availableOperations = get_available_operations(rVariables, rTokens)
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
            zero.value = 0
            zero.power = 1
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = get_level_variables(rTokens)
        availableOperations = get_available_operations(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    l = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Constant()
        zero.scope = [l + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokens_to_string(tokenToStringBuilder)
    lVariables = get_level_variables(lTokens)
    rVariables = get_level_variables(rTokens)
    availableOperations = get_available_operations_equations(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def division(tokens, direct=False):
    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
    while '/' in availableOperations:
        var, tok, rem, com = expression_division(variables, tokens)
        tokens = remove_token(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = get_level_variables(tokens)
        availableOperations = get_available_operations(variables, tokens)
    token_string = tokens_to_string(tokens)
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
        zero.value = 0
        zero.power = 1
        zero.scope = [l + 1]
        animBuilder.append(zero)
    else:
        animBuilder.extend(rToks)
    animation.append(copy.deepcopy(animBuilder))
    lVariables = []
    lVariables.extend(get_level_variables(lTokens))
    rVariables = []
    rVariables.extend(get_level_variables(rTokens))
    availableOperations = get_available_operations(lVariables, lTokens)
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
            zero = Constant()
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        lVariables = get_level_variables(lTokens)
        availableOperations = get_available_operations(lVariables, lTokens)

    availableOperations = get_available_operations(rVariables, rTokens)
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
            zero.value = 0
            zero.power = 1
            zero.scope = [l + 1]
            animBuilder.append(zero)
        else:
            animBuilder.extend(rTokens)
        animation.append(copy.deepcopy(animBuilder))
        rVariables = get_level_variables(rTokens)
        availableOperations = get_available_operations(rVariables, rTokens)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    l = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [l]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    if len(rTokens) == 0:
        zero = Constant()
        zero.scope = [l + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    token_string = tokens_to_string(tokenToStringBuilder)
    lVariables = get_level_variables(lTokens)
    rVariables = get_level_variables(rTokens)
    availableOperations = get_available_operations_equations(
        lVariables, lTokens, rVariables, rTokens)
    return lTokens, rTokens, availableOperations, token_string, animation, comments


def multiplication(tokens, direct=False):
    animation = [copy.deepcopy(tokens)]
    comments = []
    if direct:
        comments = [[]]
    variables = []
    variables.extend(get_level_variables(tokens))
    availableOperations = get_available_operations(variables, tokens)
    while '*' in availableOperations:
        var, tok, rem, com = expression_multiplication(variables, tokens)
        tokens = remove_token(tok, rem)
        comments.append(com)
        animation.append(copy.deepcopy(tokens))
        variables = get_level_variables(tokens)
        availableOperations = get_available_operations(variables, tokens)
    token_string = tokens_to_string(tokens)
    return tokens, availableOperations, token_string, animation, comments


def change_token(tokens, variables, scope_times=0):
    if len(variables) != 0:
        if variables[0].scope is not None:
            for changeVariable in variables:
                for i, token in enumerate(tokens):
                    if token.__class__ == Constant:
                        if token.scope == changeVariable.scope:
                            if changeVariable.coefficient is not None:
                                token.coefficient = changeVariable.coefficient
                            token.power = changeVariable.power
                            token.value = changeVariable.value
                            break
                    elif token.__class__ == Variable:
                        if token.scope == changeVariable.scope:
                            token.coefficient = changeVariable.coefficient
                            token.power = changeVariable.power
                            token.value = changeVariable.value
                            break
                    elif token.__class__ == Binary:
                        if token.scope == changeVariable.scope:
                            token.value = changeVariable.value
                    elif token.__class__ == Expression:
                        if scope_times + 1 == len(changeVariable.scope):
                            if token.scope == changeVariable.scope:
                                break
                        elif token.scope == changeVariable.scope[0:(scope_times + 1)]:
                            token.tokens = change_token(
                                token.tokens, token.scope, scope_times + 1)
                            break
    return tokens


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
        if token.__class__ == Variable:
            token = define_scope_variable(token, copy.deepcopy(local_scope))
        elif token.__class__ == Constant:
            token = define_scope_constant(token, copy.deepcopy(local_scope))
        elif token.__class__ == Expression:
            token.tokens = define_scope(token.tokens, local_scope)
        elif token.__class__ == Binary:
            pass
        i += 1
    return tokens


def equation_addition(lVariables, lTokens, rVariables, rTokens):
    lRemoveScopes = []
    rRemoveScopes = []
    lChange = []
    rChange = []
    comments = []
    for variable in lVariables:
        if variable.__class__ == Constant:
            for j, val in enumerate(variable.value):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if variable2.__class__ == Constant:
                            if variable2.power[0] == variable.power[0]:
                                for k, val2 in enumerate(variable2.value):
                                    if (variable2.before[k] == '-' or (variable2.before[k] == '' and variable2.value[k] < 0)) and variable2.after[k] in ['-', '+', '']:
                                        comments.append(
                                            "Moving " + variable2.before[k] + str(variable2.value[k]) + " to LHS")
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

        elif variable.__class__ == Variable:
            for j, pow1 in enumerate(variable.power):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if variable2.__class__ == Variable:
                            if variable2.power[0] == variable.power[0]:
                                for k, pow2 in enumerate(variable2.value):
                                    if variable2.before[k] == '-' and variable2.after[k] in ['-', '+', '']:
                                        comments.append("Moving " + variable2.before[k] + str(variable2.coefficient[k]) + get_variable_string(
                                            variable2.value[k], variable2.power[k]) + " to LHS")
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


def expression_addition(variables, tokens):
    removeScopes = []
    change = []
    comments = []
    for i, variable in enumerate(variables):
        if variable.__class__ == Constant:
            if len(variable.value) > 1:
                constantAdd = []
                constant = []
                for j in xrange(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '-']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Adding " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                    variable.power[const]) + ") and " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
                                if variable.before[const] == '-':
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
                                # TODO: Re-evaluate variable and tokens
                                return variables, tokens, removeScopes, change, comments
                        for const in constantAdd:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Adding " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                    variable.power[const]) + ") and " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
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
                                    comments.append("Adding " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                        variable.power[const]) + ") and " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
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

        elif variable.__class__ == Variable:
            if len(variable.power) > 1:
                constantAdd = []
                constant = []
                for j in xrange(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['+']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '-']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Adding " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " and " + str(
                                    variable.coefficient[const]) + get_variable_string(variable.value, variable.power[const]))
                                if variable.before[const] == '-':
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
                                    variable.beforeScope[constantAdd[i]])
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        for const in constantAdd:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Adding " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " and " + str(
                                    variable.coefficient[const]) + get_variable_string(variable.value, variable.power[const]))
                                if variable.before[const] == '-':
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
                                    variable.beforeScope[constantAdd[i]])
                                removeScopes.append(
                                    variable.scope[constantAdd[i]])
                                return variables, tokens, removeScopes, change, comments
                        i += 1
                elif len(constant) == 0 and len(constantAdd) > 1:
                    i = 0
                    while i < len(constantAdd):
                        for j, const in enumerate(constantAdd):
                            if i != j:
                                if variable.power[constantAdd[i]] == variable.power[const]:
                                    comments.append("Adding " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " and " + str(
                                        variable.coefficient[const]) + get_variable_string(variable.value, variable.power[const]))
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

        elif variable.__class__ == Expression:
            pass

    return variables, tokens, removeScopes, change, comments


def equation_subtraction(lVariables, lTokens, rVariables, rTokens):
    lRemoveScopes = []
    rRemoveScopes = []
    lChange = []
    rChange = []
    comments = []
    for variable in lVariables:
        if variable.__class__ == Constant:
            for j, val in enumerate(variable.value):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if variable2.__class__ == Constant:
                            if variable2.power[0] == variable.power[0]:
                                for k, val2 in enumerate(variable2.value):
                                    if variable2.before[k] in ['+', ''] and variable2.after[k] in ['-', '+', '']:
                                        comments.append(
                                            "Moving " + variable2.before[k] + str(variable2.value[k]) + " to LHS")
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
        elif variable.__class__ == Variable:
            for j, pow1 in enumerate(variable.power):
                if variable.before[j] in ['-', '+', ''] and variable.after[j] in ['+', '-', '']:
                    for variable2 in rVariables:
                        if variable2.__class__ == Variable:
                            if variable2.power[0] == variable.power[0]:
                                for k, pow2 in enumerate(variable2.value):
                                    if variable2.before[k] in ['+', ''] and variable2.after[k] in ['-', '+', '']:
                                        comments.append("Moving " + variable2.before[k] + str(variable2.coefficient[k]) + get_variable_string(
                                            variable2.value[k], variable2.power[k]) + " to LHS")
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


def expression_subtraction(variables, tokens):
    removeScopes = []
    change = []
    comments = []
    for i, variable in enumerate(variables):
        if variable.__class__ == Constant:
            if len(variable.value) > 1:
                constantAdd = []
                constant = []
                for j in xrange(len(variable.value)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['-']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '+']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                    variable.power[const]) + ") from " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
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
                                comments.append("Subtracting " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                    variable.power[const]) + ") from " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
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
                                    comments.append("Subtracting " + str(variable.value[constantAdd[i]]) + "^(" + str(
                                        variable.power[const]) + ") from " + str(variable.value[const]) + "^(" + str(variable.power[const]) + ") ")
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

        elif variable.__class__ == Variable:
            if len(variable.power) > 1:
                constantAdd = []
                constant = []
                for j in xrange(len(variable.power)):
                    if variable.after[j] in ['+', '-', ''] and variable.before[j] in ['-']:
                        constantAdd.append(j)
                    elif variable.after[j] in ['+', '-', ''] and variable.before[j] in ['', '+']:
                        constant.append(j)
                if len(constant) > 0 and len(constantAdd) > 0:
                    i = 0
                    while i < len(constantAdd):
                        for const in constant:
                            if variable.power[constantAdd[i]] == variable.power[const]:
                                comments.append("Subtracting " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " from " + str(
                                    variable.coefficient[const]) + get_variable_string(variable.value, variable.power[constantAdd[i]]))
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
                                comments.append("Subtracting " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " from " + str(
                                    variable.coefficient[const]) + get_variable_string(variable.value, variable.power[constantAdd[i]]))
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
                                    comments.append("Subtracting " + str(variable.coefficient[constantAdd[i]]) + get_variable_string(variable.value, variable.power[constantAdd[i]]) + " from " + str(
                                        variable.coefficient[const]) + get_variable_string(variable.value, variable.power[constantAdd[i]]))
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
        elif variable.__class__ == Expression:
            pass
    return variables, tokens, removeScopes, change, comments


def multiply_variables(variable1, variable2, coeff):
    variable = {}
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
    constant = {}
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
    variable1 = {}
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
        if token.__class__ == Variable:
            tokens.append(multiply_variables(
                variable, token, expression.coefficient))
        elif token.__class__ == Constant:
            tokens.append(multiply_variable_constant(
                token, variable, expression.coefficient))
        elif token.__class__ == Expression:
            tokens.append(multiply_expression_variable(
                variable, token, expression.coefficient))
        elif token.__class__ == 'binary':
            tokens.append(token)
    return tokens


def multiply_select(token1, token2, coeff=1):
    if token1.__class__ == Variable and token2.__class__ == Variable:
        return multiply_variables(token1, token2, coeff)
    elif token1.__class__ == Variable and token2.__class__ == Constant:
        return multiply_variable_constant(token2, token1, coeff)
    elif token1.__class__ == Constant and token2.__class__ == Variable:
        return multiply_variable_constant(token1, token2, coeff)
    elif token1.__class__ == Constant and token2.__class__ == Constant:
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
            if tokens1[i - 1].__class__ == Binary:
                if tokens1[i - 1].value == '+':
                    op *= 1
                elif tokens1[i - 1].value == '-':
                    op *= -1
        if token1.__class__ == Variable or token1.__class__ == Constant:
            for j, token2 in enumerate(tokens2):
                # print token2.value
                op2 = op
                if token2.__class__ == Variable or token2.__class__ == Constant:
                    if j == 0 and i == 0:
                        pass
                    else:
                        if j != 0:
                            if tokens2[j - 1].__class__ == Binary:
                                if tokens2[j - 1].value == '+':
                                    op2 *= 1
                                elif tokens2[j - 1].value == '-':
                                    op2 *= -1
                        binary = {}
                        binary.__class__ = Binary
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
        if token.__class__ == Binary:
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
                    if tokens[i + 1].__class__ == Constant and tokens[i - 1].__class__ == Constant:
                        comments.append("Multiplying " + str(tokens[i - 1].value) + "^(" + str(
                            tokens[i - 1].power + ")") + " and " + str(tokens[i + 1].value) + "^(" + str(tokens[i + 1].power) + ") ")
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

                    elif tokens[i + 1].__class__ == Variable and tokens[i - 1].__class__ == Variable:
                        comments.append("Multiplying " + str(tokens[i - 1].coefficient) + get_variable_string(tokens[i - 1].value, tokens[i - 1].power) + " and " + str(
                            tokens[i + 1].coefficient) + get_variable_string(tokens[i + 1].value, tokens[i + 1].power))
                        for j, var in enumerate(tokens[i + 1].value):
                            found = False
                            for k, var2 in enumerate(tokens[i - 1].value):
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

                    elif (tokens[i + 1].__class__ == Variable and tokens[i - 1].__class__ == Constant):
                        comments.append("Multiplying " + str(tokens[i - 1].value) + "^(" + str(tokens[i - 1].power) + ") and " + str(
                            tokens[i + 1].coefficient) + get_variable_string(tokens[i + 1].value, tokens[i + 1].power))
                        tokens[i + 1].coefficient *= evaluate_constant(tokens[i - 1])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i - 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (tokens[i - 1].__class__ == Variable and tokens[i + 1].__class__ == Constant):
                        comments.append("Multiplying " + str(tokens[i - 1].coefficient) + get_variable_string(
                            tokens[i - 1].value, tokens[i - 1].power) + " and " + str(tokens[i + 1].value) + "^(" + str(tokens[i + 1].power) + ") ")
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
    constant = {}
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
    variable1 = {}
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
        if token.__class__ == Variable:
            tokens.append(division_variables(
                token, variable, expression.coefficient))
        elif token.__class__ == Constant:
            tokens.append(division_constant_variable(
                token, variable, expression.coefficient))
        elif token.__class__ == Expression:
            tokens.append(division_expression_variable(
                variable, token, expression.coefficient))
        elif token.__class__ == Binary:
            tokens.append(token)
    return tokens


def division_variable_expression(variable, expression, coeff):
    pass


def division_select(token1, token2, coeff=1):
    if token1.__class__ == Variable and token2.__class__ == Variable:
        return division_variables(token1, token2, coeff)
    elif token1.__class__ == Variable and token2.__class__ == Constant:
        return division_variable_constant(token2, token1, coeff)
    elif token1.__class__ == Constant and token2.__class__ == Variable:
        return division_variable_constant(token1, token2, coeff)
    elif token1.__class__ == Constant and token2.__class__ == Constant:
        return division_constants(token1, token2, coeff)


def division_expressions(expression1, expression2):
    pass


def expression_division(variables, tokens):
    removeScopes = []
    comments = []
    for i, token in enumerate(tokens):
        if token.__class__ == Binary:
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
                    if tokens[i + 1].__class__ == Constant and tokens[i - 1].__class__ == Constant:
                        comments.append("Dividing " + str(tokens[i - 1].value) + "^(" + str(tokens[i - 1].power) + ") by " + str(
                            tokens[i + 1].value) + "^(" + str(tokens[i + 1].power) + ") ")
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

                    elif tokens[i + 1].__class__ == Variable and tokens[i - 1].__class__ == Variable:
                        comments.append("Dividing " + str(tokens[i - 1].coefficient) + get_variable_string(tokens[i - 1].value, tokens[i - 1].power) + " by " + str(
                            tokens[i + 1].coefficient) + get_variable_string(tokens[i + 1].value, tokens[i + 1].power))
                        for j, var in enumerate(tokens[i + 1].value):
                            found = False
                            for k, var2 in enumerate(tokens[i - 1].value):
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

                    elif (tokens[i + 1].__class__ == Variable and tokens[i - 1].__class__ == Constant):
                        comments.append("Dividing " + str(tokens[i - 1].value) + "^(" + str(tokens[i - 1].power) + ") by " + str(
                            tokens[i + 1].coefficient) + get_variable_string(tokens[i + 1].value, tokens[i + 1].power))
                        val = evaluate_constant(tokens[i - 1])
                        scope = tokens[i - 1].scope
                        tokens[i - 1] = {}
                        tokens[i - 1].value = tokens[i + 1].value
                        tokens[i - 1].coefficient = val / \
                            tokens[i + 1].coefficient
                        tokens[i - 1].power = []
                        tokens[i - 1].__class__ = Variable
                        tokens[i - 1].scope = scope
                        for pows in tokens[i + 1].power:
                            tokens[i - 1].power.append(-pows)

                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments

                    elif (tokens[i - 1].__class__ == Variable and tokens[i + 1].__class__ == Constant):
                        comments.append("Dividing " + str(tokens[i - 1].coefficient) + get_variable_string(
                            tokens[i - 1].value, tokens[i - 1].power) + " by " + str(tokens[i + 1].value) + "^(" + str(tokens[i + 1].power) + ") ")
                        tokens[i - 1].coefficient /= evaluate_constant(tokens[i + 1])
                        removeScopes.append(tokens[i].scope)
                        removeScopes.append(tokens[i + 1].scope)
                        return variables, tokens, removeScopes, comments
    return variables, tokens, removeScopes, comments


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


def get_available_operations_equations(lVariables, lTokens, rVariables, rTokens):
    operations = []
    for i, token in enumerate(lTokens):
        if token.__class__ == Binary:
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
        if token.__class__ == Binary:
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
        if variable.__class__ == Constant:
            rCount = 0
            for variable2 in rVariables:
                if variable2.__class__ == Constant:
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
                    if variable2.__class__ == Constant:
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

        elif variable.__class__ == Variable:
            rCount = 0
            for variable2 in rVariables:
                if variable2.__class__ == Variable:
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
                    if variable2.__class__ == Variable:
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

        elif variable.__class__ == Expression:
            ops = get_available_operations(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)

    for i, variable in enumerate(rVariables):
        if variable.__class__ == Constant:
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
        elif variable.__class__ == Variable:
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

        elif variable.__class__ == Expression:
            ops = get_available_operations(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)

    return operations


def get_available_operations(variables, tokens):
    operations = []
    for i, token in enumerate(tokens):
        if token.__class__ == Binary:
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
        if variable.__class__ == Constant:
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
        elif variable.__class__ == Variable:
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

        elif variable.__class__ == Expression:
            ops = get_available_operations(
                variable.value, variable.tokens)
            for op in ops:
                if op not in operations:
                    operations.append(op)
    return operations


def get_level_variables(tokens):
    variables = []
    for i, term in enumerate(tokens):
        if term.__class__ == Variable:
            skip = False
            for var in variables:
                if var.value == term.value:
                    if var.power[0] == term.power:
                        var.power.append(term.power)
                        var.scope.append(term.scope)
                        var.coefficient.append(term.coefficient)
                        if i != 0 and tokens[i - 1].__class__ == Binary:
                            var.before.append(tokens[i - 1].value)
                            var.beforeScope.append(tokens[i - 1].scope)
                        else:
                            var.before.append('')
                            var.beforeScope.append('')
                        if i + 1 < len(tokens) and tokens[i + 1].__class__ == Binary:
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
                if i != 0 and tokens[i - 1].__class__ == Binary:
                    variable.before.append(tokens[i - 1].value)
                    variable.beforeScope.append(tokens[i - 1].scope)
                else:
                    variable.before.append('')
                    variable.beforeScope.append('')
                if i + 1 < len(tokens) and tokens[i + 1].__class__ == Binary:
                    variable.after.append(tokens[i + 1].value)
                    variable.afterScope.append(tokens[i + 1].scope)
                else:
                    variable.after.append('')
                    variable.afterScope.append('')
                variables.append(variable)
        elif term.__class__ == Constant:
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
                        if i != 0 and tokens[i - 1].__class__ == Binary:
                            var.before.append(tokens[i - 1].value)
                            var.beforeScope.append(tokens[i - 1].scope)
                        else:
                            var.before.append('')
                            var.beforeScope.append('')
                        if i + 1 < len(tokens) and tokens[i + 1].__class__ == Binary:
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
                if i != 0 and tokens[i - 1].__class__ == Binary:
                    variable.before.append(tokens[i - 1].value)
                    variable.beforeScope.append(tokens[i - 1].scope)
                else:
                    variable.before.append('')
                    variable.beforeScope.append('')
                if i + 1 < len(tokens) and tokens[i + 1].__class__ == Binary:
                    variable.after.append(tokens[i + 1].value)
                    variable.afterScope.append(tokens[i + 1].scope)
                else:
                    variable.after.append('')
                    variable.afterScope.append('')
                variables.append(variable)
        elif term.__class__ == Expression:
            var = get_level_variables(term.tokens)
            retType, val = extract_expression(var)
            if retType == "expression":
                variable = {}
                variable.__class__ = Expression
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
                    if v.__class__ == Variable:
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
                    elif v.__class__ == Constant:
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
                    elif v.__class__ == Expression:
                        variables.append(v)

    return variables


def extract_expression(variable):
    if len(variable) == 1:
        if variable[0].__class__ == Expression:
            retType, variable = extract_expression(variable[0].value)
        elif variable[0].__class__ == Constant:
            return "constant", variable[0]
        elif variable[0].__class__ == Variable:
            return "variable", variable[0]
    else:
        if not eval_expressions(variable):
            return "expression", get_level_variables(variable)
        else:
            return "mixed", get_level_variables(variable)


def eval_expressions(variables):
    var = []
    varPowers = []
    for i, variable in enumerate(variables):
        if variable.__class__ == Expression:
            if eval_expressions(variable.tokens):
                return False
        elif variable.__class__ == Variable:
            prev = False
            nxt = False
            # CHECKME: Undefined i and tokens. Which tokens ?
            if i != 0:
                if variable[i - 1].__class__ == Binary:
                    if variable[i - 1].value in ['-', '+']:
                        prev = True
                else:
                    print(variable[i - 1])
            else:
                prev = True

            if i + 1 < len(variable):
                if variable[i + 1].__class__ == Binary:
                    if variable[i + 1].value in ['-', '+']:
                        nxt = True
                else:
                    print(variable[i + 1])
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
        elif variable.__class__ == Constant:
            prev = False
            nxt = False
            if i != 0:
                if variable[i - 1].__class__ == Binary:
                    if variable[i - 1].value in ['-', '+']:
                        prev = True
                else:
                    print(variable[i - 1])
            else:
                prev = True

            if i + 1 < len(variable):
                if variable[i + 1].__class__ == Binary:
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
        if variable.__class__ == Binary:
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


def check_types(lTokens=None, rTokens=None):

    from visma.solvers.polynomial.roots import preprocess_check_quadratic_roots

    if lTokens is None:
        lTokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'power': 1, 'value': 6}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'power': 1, 'value': 3}, {'scope': [5], 'type': 'binary', 'value': '-'}, {'coefficient': 2, 'scope': [6], 'type': 'variable', 'power': [1], 'value': ['x']}]
    if rTokens is None:
        rTokens = []

    if len(rTokens) != 0:
        equationCompatibile = EquationCompatibility(lTokens, rTokens)
        availableOperations = equationCompatibile.availableOperations

        if preprocess_check_quadratic_roots(copy.deepcopy(lTokens), copy.deepcopy(rTokens)):
            availableOperations.append("find roots")
        return availableOperations, "equation"
    else:
        expressionCompatible = ExpressionCompatibility(lTokens)
        return expressionCompatible.availableOperations, "expression"


if __name__ == '__main__':
            # check_types()
            # test()

    multiply_expressions({'tokens': [{'coefficient': 1, 'scope': [0, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [0, 1], 'type': Binary, 'value': '-'}, {'scope': [0, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [0], 'coefficient': 1, 'type': Expression}, {
                         'tokens': [{'coefficient': 1, 'scope': [1, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1, 1], 'type': Binary, 'value': '+'}, {'scope': [1, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [1], 'coefficient': 1, 'type': Expression})
