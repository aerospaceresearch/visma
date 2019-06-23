"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is aimed at first checking if quadratic roots can be found for the given equation, and then in the next step find the quadratic roots and display them.

Note: Please try to maintain proper documentation
Logic Description:
"""

import math
import copy
from visma.io.checks import getVariables
from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens

from visma.config.values import ROUNDOFF

# FIXME: Extend to polynomials of all degrees


def getRoots(coeffs):
    '''Applies Quadratic Formula (https://en.wikipedia.org/wiki/Quadratic_formula) on the coefficients
    of the quadratic equation

    Arguments:
        coeffs {list} -- list of coefficients of the quadratic equation

    Returns:
        roots {list} -- list of roots of quadratic equation
    '''
    roots = []
    if len(coeffs) == 3:
        d = (coeffs[1] * coeffs[1]) - (4 * coeffs[0] * coeffs[2])
        if d == 0:
            roots.append(-(coeffs[1] / (2 * coeffs[2])))
        elif d > 0:
            d = math.sqrt(d)
            roots.append(-(coeffs[1] + d) / (2 * coeffs[2]))
            roots.append(-(coeffs[1] - d) / (2 * coeffs[2]))
        else:
            imaginary = [-(coeffs[1] / (2 * coeffs[2])), -1,
                         (math.sqrt(-d)) / (2 * coeffs[2])]
            roots = imaginary
    return roots


def quadraticRoots(lTokens, rTokens):
    '''Used to get quadratic roots of an equation
    (Main driver function in module)

    Argument:
        lTokens {list} -- list of LHS tokens
        rTokens {list} -- list of RHS tokens

    Returns:
        lTokens {list} -- list of LHS tokens
        rTokens {list} -- list of RHS tokens
        {empty list}
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    '''
    from visma.solvers.polynomial.roots import getCoefficients

    lTokens, rTokens, _, token_string, animation, comments = simplifyEquation(
        lTokens, rTokens)
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
    coeffs = getCoefficients(lTokens, rTokens, 2)
    var = getVariables(lTokens)
    roots = getRoots(coeffs)
    if len(roots) == 1:
        tokens = []
        expression = Expression()
        expression.coefficient = 1
        expression.power = 2
        variable = Variable()
        variable.value = var
        variable.power = [1]
        variable.coefficient = 1
        tokens.append(variable)
        binary = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary.value = '+'
        else:
            binary.value = '-'
        tokens.append(binary)
        constant = Constant()
        constant.value = round(roots[0], ROUNDOFF)
        constant.power = 1
        tokens.append(constant)
        expression.tokens = tokens
        lTokens = [expression]

    elif len(roots) == 2:
        tokens = []
        expression = Expression()
        expression.coefficient = 1
        expression.power = 1
        variable = Variable()
        variable.value = var
        variable.power = [1]
        variable.coefficient = 1
        tokens.append(variable)
        binary = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary.value = '+'
        else:
            binary.value = '-'
        tokens.append(binary)
        constant = Constant()
        constant.value = round(roots[0], ROUNDOFF)
        constant.power = 1
        tokens.append(constant)
        expression.tokens = tokens

        tokens2 = []
        expression2 = Expression()
        expression2.coefficient = 1
        expression2.power = 1
        variable2 = Variable()
        variable2.value = var
        variable2.power = [1]
        variable2.coefficient = 1
        tokens2.append(variable)
        binary2 = Binary()
        if roots[1] < 0:
            roots[1] *= -1
            binary2.value = '+'
        else:
            binary2.value = '-'
        tokens2.append(binary2)
        constant2 = Constant()
        constant2.value = round(roots[1], ROUNDOFF)
        constant2.power = 1
        tokens2.append(constant2)
        expression2.tokens = tokens2

        binary3 = Binary()
        binary3.value = '*'
        lTokens = [expression, binary3, expression2]

    elif len(roots) == 3:
        sqrtPow = Constant()
        sqrtPow.value = 2
        sqrtPow.power = 1

        binary4 = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary4.value = '+'
        else:
            binary4.value = '-'

        constant3 = Constant()
        constant3.value = round(roots[0], ROUNDOFF)
        constant3.power = 1

        binary5 = Binary()
        binary5.value = '*'

        constant2 = Constant()
        constant2.value = round(roots[2], ROUNDOFF)
        constant2.power = 1

        tokens = []
        expression = Expression()
        expression.coefficient = 1
        expression.power = 1
        variable = Variable()
        variable.value = var
        variable.power = [1]
        variable.coefficient = 1
        tokens.append(variable)
        tokens.append(binary4)
        tokens.append(constant3)
        binary = Binary()
        binary.value = '+'
        tokens.append(binary)
        tokens.append(constant2)
        tokens.append(binary5)
        constant = Constant()
        constant.value = round(roots[1], ROUNDOFF)
        constant.power = 1
        sqrt = Sqrt()
        sqrt.power = sqrtPow
        sqrt.operand = constant
        tokens.append(sqrt)
        expression.tokens = tokens

        tokens2 = []
        expression2 = Expression()
        expression2.coefficient = 1
        expression2.power = 1
        variable2 = Variable()
        variable2.value = var
        variable2.power = [1]
        variable2.coefficient = 1
        tokens2.append(variable)
        tokens2.append(binary4)
        tokens2.append(constant3)
        binary2 = Binary()
        binary2.value = '-'
        tokens2.append(binary2)
        tokens2.append(constant2)
        tokens2.append(binary5)
        tokens2.append(sqrt)
        expression2.tokens = tokens2

        binary3 = Binary()
        binary3.value = '*'
        lTokens = [expression, binary3, expression2]

    zero = Zero()
    rTokens = [zero]
    comments.append([])
    tokenToStringBuilder = copy.deepcopy(lTokens)
    tokLen = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [tokLen]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    tokenToStringBuilder.extend(rTokens)
    animation.append(copy.deepcopy(tokenToStringBuilder))
    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, [], token_string, animation, comments
