"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module hosts the functions used for finding roots of a  quartic equation
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


def getRootsQuadratic(coeffs):
    '''Applies Quadratic Formula (https://en.wikipedia.org/wiki/Quadratic_formula) on the coefficients
    of the quadratic equation

    Arguments:
        coeffs {list} -- list of coefficients of the quadratic equation

    Returns:
        roots {list} -- list of roots of quadratic equation
    '''
    animations = []
    comments = []
    roots = []
    if len(coeffs) == 3:
        d = (coeffs[1] * coeffs[1]) - (4 * coeffs[0] * coeffs[2])
        if d == 0:
            roots.append(-(coeffs[1] / (2 * coeffs[2])))
            animations += [[]]
            comments += [['Value of discriminant is: ' + str(d) + ' thus, Only one roots']]
        elif d > 0:
            comments += [['Value of discriminant is: ' + str(d) + ' thus, two (real) roots']]
            d = math.sqrt(d)
            roots.append(-(coeffs[1] + d) / (2 * coeffs[2]))
            roots.append(-(coeffs[1] - d) / (2 * coeffs[2]))
            animations += [[]]
        else:
            imaginary = [-(coeffs[1] / (2 * coeffs[2])), -1,
                         (math.sqrt(-d)) / (2 * coeffs[2])]
            roots = imaginary
            animations += [[]]
            comments += [['Value of discriminant is: ' + str(d) + ' thus, two (imaginary) roots']]
    return roots, animations, comments


def quadraticRoots(lTokens, rTokens):
    '''Used to get quadratic roots of an equation

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

    animations = []
    comments = []
    lTokens, rTokens, _, token_string, animNew1, commentNew1 = simplifyEquation(lTokens, rTokens)
    animations.extend(animNew1)
    comments.extend(commentNew1)
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
    coeffs = getCoefficients(lTokens, rTokens, 2)
    var = getVariables(lTokens)
    roots, animNew2, commentNew2 = getRootsQuadratic(coeffs)
    animations.extend(animNew2)
    comments.extend(commentNew2)
    if len(roots) == 1:
        tokens = []
        expression = Expression(coefficient=1, power=2)
        variable = Variable(1, var[0], 1)
        tokens.append(variable)
        binary = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary.value = '+'
        else:
            binary.value = '-'
        tokens.append(binary)
        constant = Constant(round(roots[0], ROUNDOFF), 1)
        tokens.append(constant)
        expression.tokens = tokens
        lTokens = [expression]

    elif len(roots) == 2:
        tokens = []
        expression = Expression(coefficient=1, power=1)
        variable = Variable(1, var[0], 1)
        tokens.append(variable)
        binary = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary.value = '+'
        else:
            binary.value = '-'
        tokens.append(binary)
        constant = Constant(round(roots[0], ROUNDOFF), 1)
        tokens.append(constant)
        expression.tokens = tokens

        tokens2 = []
        expression2 = Expression(coefficient=1, power=1)
        tokens2.append(variable)
        binary2 = Binary()
        if roots[1] < 0:
            roots[1] *= -1
            binary2.value = '+'
        else:
            binary2.value = '-'
        tokens2.append(binary2)
        constant2 = Constant(round(roots[1], ROUNDOFF), 1)
        tokens2.append(constant2)
        expression2.tokens = tokens2

        binary3 = Binary()
        binary3.value = '*'
        lTokens = [expression, binary3, expression2]

    elif len(roots) == 3:
        binary4 = Binary()
        if roots[0] < 0:
            roots[0] *= -1
            binary4.value = '+'
        else:
            binary4.value = '-'

        constant3 = Constant(round(roots[0], ROUNDOFF), 1)

        binary5 = Binary()
        binary5.value = '*'

        constant2 = Constant(round(roots[2], ROUNDOFF), 1)

        tokens = []
        expression = Expression(coefficient=1, power=1)
        variable = Variable(1, var[0], 1)
        tokens.extend([variable, binary4, constant3])
        binary = Binary()
        binary.value = '+'
        tokens.extend([binary, constant2, binary5])
        constant = Constant(round(roots[1], ROUNDOFF), 1)
        sqrt = Sqrt(Constant(2, 1), constant)
        tokens.append(sqrt)
        expression.tokens = tokens

        tokens2 = []
        expression2 = Expression(coefficient=1, power=1)
        variable2 = Variable(1, var[0], 1)
        tokens2.extend([variable2, binary4, constant3])
        binary2 = Binary()
        binary2.value = '-'
        tokens2.extend([binary2, constant2, binary5, sqrt])
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
    animations.append(copy.deepcopy(tokenToStringBuilder))
    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, [], token_string, animations, comments
