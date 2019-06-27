import copy
import math
from visma.io.checks import evaluateConstant, preprocessCheckPolynomial
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary
from visma.solvers.polynomial.quadratic import quadraticRoots
from visma.solvers.polynomial.cubic import cubicRoots
from visma.solvers.polynomial.quartic import quarticRoots


def rootFinder(lTokens, rTokens):
    lTokensTemp = copy.deepcopy(lTokens)
    rTokensTemp = copy.deepcopy(rTokens)
    _, polyDegree = preprocessCheckPolynomial(lTokensTemp, rTokensTemp)
    if polyDegree == 2:
        lTokens, rTokens, _, token_string, animation, comments = quadraticRoots(lTokens, rTokens)
    elif polyDegree == 3:
        lTokens, rTokens, _, token_string, animation, comments = cubicRoots(lTokens, rTokens)
    elif polyDegree == 4:
        lTokens, rTokens, _, token_string, animation, comments = quarticRoots(lTokens, rTokens)
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
                        if token.power[0] in [1, 2, 3, 4]:
                            coeffs[int(token.power[0])] += var
                        else:
                            return []
                    else:
                        return []
                else:
                    if token.power[0] in [1, 2, 3, 4]:
                        coeffs[int(token.power[0])] += var
                    else:
                        return []
            else:
                return []
    return coeffs


def squareRootComplex(value):
    a = value[0]
    b = value[1]
    root = 2*[0]
    root[0] = math.sqrt((a + math.sqrt(a*a + b*b))/2)
    root[1] = math.sqrt((math.sqrt(a*a + b*b) - a)/2)
    if b < 0:
        root[1] = -root[1]
    return root


def cubeRoot(value):
    if value >= 0:
        return value ** (1./3.)
    else:
        return (-(-value) ** (1./3.))
