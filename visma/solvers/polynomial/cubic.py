import math
import copy
from visma.io.checks import getVariables
from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Plus, Minus, Sqrt
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens
from visma.config.values import ROUNDOFF


def getRootsCubic(coeffs):
    """ Applies an implementation of Cardano's Method (https://en.wikipedia.org/wiki/Cubic_function) on the coefficients
        of the cubic equation
    """
    from visma.solvers.polynomial.roots import cubeRoot
    roots = []
    animations = []
    comments = []
    a = coeffs[3]
    b = coeffs[2]
    c = coeffs[1]
    d = coeffs[0]

    f = ((3*c/a) - (b**2/a**2))/3
    g = ((2*(b**3)/(a**3)) - (9*b*c/(a**2)) + (27*d/a))/27
    h = ((g**2)/4) + ((f**3)/27)
    animations += [[]]
    comments += [['Value of determinants [f, g, h] are ' + str(f) + ', ' + str(g) + ', ' + str(h)]]
    if h <= 0:
        if h == 0 and g == 0 and f == 0:
            # All three (real) roots exist and are equal
            animations += [[]]
            comments += [['Hence, three equal real roots exist.']]
            res = cubeRoot(d/a)
            valueX1 = [-res, 0]
            valueX2 = [-res, 0]
            valueX3 = [-res, 0]
            roots.append(valueX1)
        else:
            # All three (real) roots exist
            animations += [[]]
            comments += [['Hence, three equal non-equal real roots exist.']]
            i = (((g**2)/4) - h) ** (1./2.)
            j = cubeRoot(i)
            k = math.acos(-g/(2*i))
            L = j * (-1)
            M = math.cos(k/3)
            N = math.sqrt(3) * (math.sin(k/3))
            P = -(b/(3*a))
            valueX1 = [2*j*(math.cos(k/3)) - (b/(3*a)), 0]
            valueX2 = [L*(M + N) + P, 0]
            valueX3 = [L*(M - N) + P, 0]
            roots.extend([valueX1, valueX2, valueX3])
    else:
        # Only one (real) root exists
        animations += [[]]
        comments += [['Hence, one real root exists']]
        R = -(g/2) + h ** (1./2.)
        S = cubeRoot(R)
        T = -(g/2) - (h ** (1./2.))
        U = cubeRoot(T)
        valueX1 = [(S + U) - (b/(3*a)), 0]

        valueRealX2 = -(S + U)/2 - (b/(3*a))
        valueImagX2 = (S - U)*(3 ** (1./2.))/2
        valueX2 = [valueRealX2, valueImagX2]

        valueRealX3 = -(S + U)/2 - (b/(3*a))
        valueImagX3 = -(S - U)*(3 ** (1./2.))/2
        valueX3 = [valueRealX3, valueImagX3]
        roots.extend([valueX1, valueX2, valueX3])

    return roots, animations, comments


def cubicRoots(lTokens, rTokens):
    from visma.solvers.polynomial.roots import getCoefficients

    animations = []
    comments = []
    lTokens, rTokens, _, token_string, animNew1, commentNew1 = simplifyEquation(lTokens, rTokens)
    animations.extend(animNew1)
    comments.extend(commentNew1)
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
    coeffs = getCoefficients(lTokens, rTokens, 3)
    var = getVariables(lTokens)
    roots, animNew2, commentNew2 = getRootsCubic(coeffs)
    animations.extend(animNew2)
    comments.extend(commentNew2)
    tokens1 = []
    expression1 = Expression()
    expression1.coefficient = 1
    expression1.power = 3
    variable = Variable()
    variable.value = var
    variable.power = [1]
    variable.coefficient = 1
    tokens1.append(variable)
    if roots[0][1] == 0:
        binary = Binary()
        if roots[0][0] < 0:
            roots[0][0] *= -1
            binary.value = '+'
        else:
            binary.value = '-'
        tokens1.append(binary)
        constant = Constant()
        constant.value = round(roots[0][0], ROUNDOFF)
        constant.power = 1
    tokens1.append(constant)

    expression1.tokens = tokens1
    lTokens = [expression1, Binary('*')]

    if len(roots) > 1:
        expression1.power = 1
        for _, root in enumerate(roots[1:]):
            tokens2 = []
            expression2 = Expression()
            expression2.coefficient = 1
            expression2.power = 1
            variable = Variable()
            variable.value = var
            variable.power = [1]
            variable.coefficient = 1
            tokens2.append(variable)
            binary = Binary()
            if root[1] == 0:
                if root[0] < 0:
                    root[0] *= -1
                    binary.value = '+'
                else:
                    binary.value = '-'
                tokens2.append(binary)
                constant = Constant()
                constant.value = round(root[0], ROUNDOFF)
                constant.power = 1
                tokens2.append(constant)
            else:
                binary.value = '-'
                tokens2.append(binary)
                expressionResult = Expression()
                expressionResult.power = 1
                expressionResult.coefficient = 1
                tokensResult = []
                real = Constant()
                real.value = round(root[0], ROUNDOFF)
                real.power = 1
                tokensResult.append(real)
                imaginary = Constant()
                imaginary.value = round(root[1], ROUNDOFF)
                imaginary.power = 1
                if imaginary.value < 0:
                    tokensResult.append(Minus())
                    imaginary.value = abs(imaginary.value)
                    tokensResult.append(imaginary)
                else:
                    tokensResult.append(Plus())
                    tokensResult.append(imaginary)
                sqrtPow = Constant(2, 1)
                sqrt = Sqrt()
                sqrt.power = sqrtPow
                sqrt.operand = Constant(-1)
                tokensResult.append(Binary('*'))
                tokensResult.append(sqrt)
                expressionResult.tokens = tokensResult
                tokens2.append(expressionResult)
            expression2.tokens = tokens2
            lTokens.extend([expression2, Binary('*')])
    lTokens.pop()
    rTokens = [Zero()]
    tokenToStringBuilder = copy.deepcopy(lTokens)
    tokLen = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [tokLen]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    animations.append(copy.deepcopy(tokenToStringBuilder))
    comments.append([])
    return lTokens, rTokens, [], token_string, animations, comments
