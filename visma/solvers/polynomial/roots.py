import copy
from visma.io.checks import evaluateConstant
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens
from visma.solvers.polynomial.quadratic import quadraticRoots
from visma.solvers.polynomial.cubic import cubicRoots


def rootFinder(lTokens, rTokens):
    lTokensTemp = copy.deepcopy(lTokens)
    rTokensTemp = copy.deepcopy(rTokens)
    degree = getDegree(lTokensTemp, rTokensTemp)
    if degree == 2:
        lTokens, rTokens, _, token_string, animation, comments = quadraticRoots(lTokens, rTokens)
    elif degree == 3:
        lTokens, rTokens, _, token_string, animation, comments = cubicRoots(lTokens, rTokens)
    return lTokens, rTokens, [], token_string, animation, comments


def getCoefficients(lTokens, rTokens, degree):

    coeffs = [0] * (degree + 1)
    for i, token in enumerate(lTokens):
        if isinstance(token, Constant):
            cons = evaluateConstant(token)
            if i != 0:
                if isinstance(lTokens[i - 1], Binary):
                    if lTokens[i - 1].value in ['-', '+']:
                        if lTokens[i - 1].value == '-':
                            cons *= -1
            if (i + 1) < len(lTokens):
                if lTokens[i + 1].value not in ['*', '/']:
                    coeffs[0] += cons
                else:
                    return []
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
                    if lTokens[i + 1].value not in ['*', '/']:
                        if token.power[0] == 1 or token.power[0] == 2 or token.power[0] == 3:
                            coeffs[int(token.power[0])] += var
                        else:
                            return []
                    else:
                        return []
                else:
                    if token.power[0] == 1 or token.power[0] == 2 or token.power[0] == 3:
                        coeffs[int(token.power[0])] += var
                    else:
                        return []
            else:
                return []
    return coeffs


def getDegree(lTokens, rTokens):
    lTokens, rTokens, _, _, _, _ = simplifyEquation(lTokens, rTokens)
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
    degree = 0
    for token in lTokens:
        if isinstance(token, Variable):
            degree = max([degree, token.power[0]])
    return degree


def cubeRoot(value):
    if value >= 0:
        return value ** (1./3.)
    else:
        return (-(-value) ** (1./3.))
