import math
import copy
from operator import itemgetter
from visma.io.checks import getVariables
from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Plus, Minus, Sqrt
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens
from visma.config.values import ROUNDOFF
from visma.solvers.polynomial.cubic import getRootsCubic


def getRootsQuartic(coeffs):
    from visma.solvers.polynomial.roots import squareRootComplex
    roots = []
    a = coeffs[4]
    b = coeffs[3]
    c = coeffs[2]
    d = coeffs[1]
    e = coeffs[0]

    f = c - (3*(b**2)/8)
    g = d + (b**3)/8 - (b*c/2)
    h = e - (3*(b**4)/256) + ((b**2)*c/16) - (b*d/4)

    reducedCubicEquation = [-(g*g)/64, (f*f - 4*h)/16, (f/2), 1]
    rootsReducedCubic, _, _ = getRootsCubic(reducedCubicEquation)
    for i in range(3):
        rootsReducedCubic[i][0] = round(rootsReducedCubic[i][0], ROUNDOFF)
        rootsReducedCubic[i][1] = round(rootsReducedCubic[i][1], ROUNDOFF)
    if (rootsReducedCubic[0][1] == 0 and rootsReducedCubic[1][1] == 0 and rootsReducedCubic[2][1] == 0):
        #   Imaginary part doesn't exists in reduced Cubic equation
        if (rootsReducedCubic[0][0] >= 0 and rootsReducedCubic[1][0] >= 0 and rootsReducedCubic[2][0] >= 0):
            rootsReducedCubicSorted = sorted(rootsReducedCubic, key=itemgetter(0))
            p = math.sqrt(rootsReducedCubicSorted[1][0])
            q = math.sqrt(rootsReducedCubicSorted[2][0])
            r = -g/(8*p*q)
            s = b/(4*a)
            valueRealX1 = p + q + r - s
            valueImaginaryX1 = 0
            roots.append([valueRealX1, valueImaginaryX1])

            valueRealX2 = p - q - r - s
            valueImaginaryX2 = 0
            roots.append([valueRealX2, valueImaginaryX2])

            valueRealX3 = - p + q - r - s
            valueImaginaryX3 = 0
            roots.append([valueRealX3, valueImaginaryX3])

            valueRealX4 = - p - q + r - s
            valueImaginaryX4 = 0
            roots.append([valueRealX4, valueImaginaryX4])
        else:
            rootsReducedCubicSorted = []
            for x in rootsReducedCubic:
                if x[0] < 0:
                    rootsReducedCubicSorted.append(x)
            for x in rootsReducedCubic:
                if x[0] > 0:
                    rootsReducedCubicSorted.append(x)
            p = [0, math.sqrt(abs(rootsReducedCubicSorted[0][0]))]
            q = [0, math.sqrt(abs(rootsReducedCubicSorted[1][0]))]
            pq = -1 * p[1] * q[1]
            r = -g/(8*pq)
            s = b/(4*a)

            valueRealX1 = r - s
            valueImaginaryX1 = p[1] + q[1]
            roots.append([valueRealX1, valueImaginaryX1])

            valueRealX2 = - r - s
            valueImaginaryX2 = p[1] - q[1]
            roots.append([valueRealX2, valueImaginaryX2])

            valueRealX3 = - r - s
            valueImaginaryX3 = - p[1] + q[1]
            roots.append([valueRealX3, valueImaginaryX3])

            valueRealX4 = r - s
            valueImaginaryX4 = - p[1] - q[1]
            roots.append([valueRealX4, valueImaginaryX4])
    else:
        #   Imaginary part exists in reduced Cubic equation
        rootsReducedCubicSorted = []
        for x in rootsReducedCubic:
            if x[1] != 0:
                rootsReducedCubicSorted.append(x)
        for x in rootsReducedCubic:
            if x[1] == 0:
                rootsReducedCubicSorted.append(x)
        p = squareRootComplex(rootsReducedCubicSorted[0])
        q = squareRootComplex(rootsReducedCubicSorted[1])
        if p[1] > 0 and p[0] < 0:
            p, q = q, p
        pq = p[0]*p[0] + p[1]*p[1]
        r = -g/(8*pq)
        s = b/(4*a)

        valueRealX1 = 2*p[0] + r - s
        valueImaginaryX1 = 0
        roots.append([valueRealX1, valueImaginaryX1])

        valueRealX2 = - r - s
        valueImaginaryX2 = 2*p[1]
        roots.append([valueRealX2, valueImaginaryX2])

        valueRealX3 = - r - s
        valueImaginaryX3 = -2*p[1]
        roots.append([valueRealX3, valueImaginaryX3])

        valueRealX4 = -2*p[0] + r - s
        valueImaginaryX4 = 0
        roots.append([valueRealX4, valueImaginaryX4])
    return roots


def quarticRoots(lTokens, rTokens):
    from visma.solvers.polynomial.roots import getCoefficients

    lTokens, rTokens, _, _, _, _ = simplifyEquation(lTokens, rTokens)
    if len(rTokens) > 0:
        lTokens, rTokens = moveRTokensToLTokens(lTokens, rTokens)
    coeffs = getCoefficients(lTokens, rTokens, 4)
    for i, lTok in enumerate(lTokens):
        if not isinstance(lTok, Binary):
            lTokens[i] /= Constant(coeffs[4])
    for i, rTok in enumerate(rTokens):
        if not isinstance(rTok, Binary):
            rTokens[i] /= Constant(coeffs[4])
    coeffs = getCoefficients(lTokens, rTokens, 4)
    roots = getRootsQuartic(coeffs)
    var = getVariables(lTokens)
    lTokens = []
    rTokens = []
    for _, root in enumerate(roots):
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
    rTokens = [Zero()]
    lTokens.pop()
    tokenToStringBuilder = copy.deepcopy(lTokens)
    tokLen = len(lTokens)
    equalTo = Binary()
    equalTo.scope = [tokLen]
    equalTo.value = '='
    tokenToStringBuilder.append(equalTo)
    tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)
    return lTokens, rTokens, [], token_string, [], []
