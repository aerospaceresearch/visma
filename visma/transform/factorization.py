from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Plus, Minus, Multiply
from visma.simplify.simplify import simplify
from visma.utils.integers import gcd, factors
from visma.utils.polynomials import syntheticDivision


def factorize(tokens):

    tokens, availableOperations, token_string, animation, comments = simplify(tokens)

    tokens, animNew, commentsNew = (factorizeTokens(tokens))

    animation.extend(animNew)
    comments.append(commentsNew)
    token_string = tokensToString(tokens)

    return tokens, availableOperations, token_string, animation, comments


def factorizeTokens(tokens):

    coeffs, var = getPolyCoeffs(tokens)
    gcf, roots, polynomial = factor(coeffs)
    if roots != []:
        tokens = []
        comment = "The real roots of the above polynomial are "
        for root in roots:
            comment += r"$" + str(root) + r"\ ,\ " + r"$"
        if gcf != 1:
            tokens.append(Constant(float(gcf)))
            tokens.append(Multiply())
        for root in roots:
            expression = Expression()
            expression.tokens.append(Variable(1, var, 1))
            if root > 0:
                expression.tokens.append(Minus())
                expression.tokens.append(Constant(float(root)))
            elif root < 0:
                expression.tokens.append(Plus())
                expression.tokens.append(Constant(float(-root)))
            tokens.append(expression)
            tokens.append(Multiply())
        if polynomial != [1]:
            expression = Expression()
            degree = len(polynomial) - 1
            for i, coeff in enumerate(polynomial):
                if i == degree:
                    if coeff > 0:
                        expression.tokens.append(Plus())
                        expression.tokens.append(Constant(float(coeff)))
                    elif coeff < 0:
                        expression.tokens.append(Minus())
                        expression.tokens.append(Constant(float(-coeff)))
                elif coeff > 0:
                    expression.tokens.append(Plus())
                    expression.tokens.append(Variable(coeff, var, degree - i))
                elif coeff < 0:
                    expression.tokens.append(Minus())
                    expression.tokens.append(Variable(-coeff, var, degree - i))
            if isinstance(expression.tokens[0], Plus):
                expression.tokens.pop(0)
            tokens.append(expression)
        else:
            tokens.pop()
    else:
        comment = None
    animation = [tokens]
    comments = [comment]
    return tokens, animation, comments


def getPolyCoeffs(tokens):
    degree = 0
    for token in tokens:
        if isinstance(token, Variable) and token.power[0] > degree:
            degree = token.power[0]
            var = token.value[0]

    coeffs = [0]*int(degree + 1)
    for i, token in enumerate(tokens):
        if isinstance(token, Variable):
            coeffs[int(degree - token.power[0])] = int(token.coefficient)
            if tokens[i-1].value == '-':
                coeffs[int(degree - token.power[0])] *= -1
        elif isinstance(token, Constant):
            coeffs[int(degree)] = int(token.value)
            if tokens[i-1].value == '-':
                coeffs[int(degree)] *= -1
    return coeffs, var


def factor(coefficients):
    gcf = gcd(coefficients)
    coefficients = [coefficient / gcf for coefficient in coefficients]
    polynomial = coefficients
    roots = []
    while extractRoots(polynomial) is not False:
        root, quotient = extractRoots(polynomial)
        roots.append(root)
        polynomial = quotient
    polynomial = [int(term) for term in polynomial]
    roots.sort()
    return gcf, roots, polynomial


def extractRoots(coefficients):
    factorsLeading = factors(coefficients[0])
    factorsConstant = factors(coefficients[-1])
    roots = possibleRoots(factorsConstant, factorsLeading)
    for root in roots:
        quotient, remainder = syntheticDivision(coefficients, root)
        if remainder == 0:
            return root, quotient
    return False


def possibleRoots(listA, listB):
    roots = []
    listA = [float(i) for i in listA]
    listB = [float(i) for i in listB]
    for i in listA:
        for j in listB:
            roots.extend([i / j, -i / j])
    roots = removeDuplicates(roots)
    return roots


def removeDuplicates(extraRoots):
    roots = []
    for x in extraRoots:
        if x not in roots:
            roots.append(x)
    return roots
