"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is aimed at first checking if quadratic roots can be found for the given equation, and then in the next step find the quadratic roots and display them.

Note: Please try to maintain proper documentation
Logic Description:
"""

from __future__ import division
import math
import copy
from visma.io.checks import evaluateConstant, availableVariables
from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens

from config.config import ROUNDOFF

# FIXME: Extend to polynomials of all degrees


def getRoots(coeffs):
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
    lTokens, rTokens, availableOperations, token_string, animation, comments = simplifyEquation(
        lTokens, rTokens)
    roots, var = findQuadraticRoots(lTokens, rTokens)
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
        sqrt.expression = constant
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
    if len(rTokens) == 0:
        zero = Zero()
        zero.scope = [tokLen + 1]
        tokenToStringBuilder.append(zero)
    else:
        tokenToStringBuilder.extend(rTokens)
    animation.append(copy.deepcopy(tokenToStringBuilder))
    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, [], token_string, animation, comments


def findQuadraticRoots(lTokens, rTokens):
    roots = []
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(
            lTokens, rTokens)
    coeffs = [0, 0, 0]
    for i, token in enumerate(lTokens):
        if isinstance(token, Constant):
            cons = evaluateConstant(token)
            if i != 0:
                if isinstance(lTokens[i - 1], Binary):
                    if lTokens[i - 1].value in ['-', '+']:
                        if lTokens[i - 1].value == '-':
                            cons *= -1
            if (i + 1) < len(lTokens):
                if lTokens[i + 1].__class__ not in ['*', '/']:
                    coeffs[0] += cons
                else:
                    return roots
            else:
                coeffs[0] += cons
        if isinstance(token, Variable):
            if len(token.value) == 1:
                var = token.coefficient
                if i != 0:
                    if isinstance(lTokens[i - 1], Binary):
                        if lTokens[i - 1].value in ['-', '+']:
                            if lTokens[i - 1].value == '-':
                                var *= -1
                if (i + 1) < len(lTokens):
                    if lTokens[i + 1].__class__ not in ['*', '/']:
                        if token.power[0] == 1 or token.power[0] == 2:
                            coeffs[int(token.power[0])] += var
                        else:
                            return roots
                    else:
                        return roots
                else:
                    if token.power[0] == 1 or token.power[0] == 2:
                        coeffs[int(token.power[0])] += var
                    else:
                        return roots
            else:
                return roots

    return getRoots(coeffs), availableVariables(lTokens)


if __name__ == '__main__':
    pass
