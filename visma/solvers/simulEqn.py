from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens
from visma.io.parser import tokensToString
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.matrix.special import cramerMatrices
from visma.io.checks import getVariables


def coeffCalculator(LandR_tokens, variables):
    '''Finds coefficients of x, y and z and the constant term when solving for 3 simulaneous equations.

    Arguments:
        LandR_tokens -- 3 x 2 list -- each row contains left and right tokens of certain equation.

    Returns:
        coefficients -- 3 X 4 list -- each each row contains coefficients for x, y, z and constant term respectively.
    '''
    # TODO: Currently implemented taking with fixed variables x, y and z. To be implemented with different variables like u, v  and w.
    coefficients = []
    coefficients = [[0] * 4 for _ in range(3)]
    for i, LandR_token in enumerate(LandR_tokens):
        lTokens = LandR_token[0]
        rTokens = LandR_token[1]
        if len(rTokens) > 0:
            lTokens, rTokens = moveRTokensToLTokens(
                lTokens, rTokens
            )
        for _, token in enumerate(lTokens):
            if isinstance(token, Variable):
                if token.value == [variables[0]]:
                    coefficients[i][0] = token.coefficient
                elif token.value == [variables[1]]:
                    coefficients[i][1] = token.coefficient
                elif token.value == [variables[2]]:
                    coefficients[i][2] = token.coefficient
            if isinstance(token, Constant):
                coefficients[i][3] = token.value

    return coefficients


def getResult(matD, matDx, matDy, matDz, variables, comments, animation, solveFor):
    '''Calculates values of x, y and z

    Arguments:
        matD {visma.matrix.structure.Matrix.SquareMat} -- Matrix Token
        matD {visma.matrix.structure.Matrix.SquareMat} -- Matrix Token
        matD {visma.matrix.structure.Matrix.SquareMat} -- Matrix Token
        matD {visma.matrix.structure.Matrix.SquareMat} -- Matrix Token
        comments {list} -- list of comments
        animation {list} -- equation tokens for step by step

    Returns:
        comments {list} -- list of comments
        animations {list} -- list of step by step tokens
        trivial {bool} -- Indicates if trivial solutions exist or not
    '''
    x = 0
    y = 0
    z = 0
    trivial = True
    detD = float(tokensToString(matD.determinant()))
    detDx = float(tokensToString(matDx.determinant()))
    detDy = float(tokensToString(matDy.determinant()))
    detDz = float(tokensToString(matDz.determinant()))
    comments += [['Determinant value of first Crammer Matrix D = ' + str(detD)]]
    animation += [[]]
    comments += [['Determinant value of second Cramer Matrix Dx = ' + str(detDx)]]
    animation += [[]]
    comments += [['Determinant value of third Cramer Matrix Dy = ' + str(detDy)]]
    animation += [[]]
    comments += [['Determinant value of fourth Cramer Matrix Dz = ' + str(detDz)]]
    animation += [[]]
    if detD == 0:
        trivial = False
    if trivial:
        x = detDx/detD
        y = detDy/detD
        z = detDz/detD
    resultStr = ''
    if trivial:
        if solveFor == variables[0]:
            resultStr = str(variables[0]) + ' = ' + str(x)
            comments += [[]]
            animation += [tokenizer(resultStr)]
        elif solveFor == variables[1]:
            resultStr = str(variables[1]) + ' = ' + str(y)
            comments += [[]]
            animation += [tokenizer(resultStr)]
        elif solveFor == variables[2]:
            resultStr = str(variables[2]) + ' = ' + str(z)
            comments += [[]]
            animation += [tokenizer(resultStr)]
    elif not trivial:
        comments += [['There is no trivial solution to the the provided set of equations as D = 0']]
        animation += [[]]
    return comments, animation, trivial


def simulSolver(eqTok1, eqTok2, eqTok3, solveFor):
    '''
    Main driver function in simulEqn.py

    Arguments:
        eqTok1 {lsit} -- list of tokens of first equation
        eqTok2 {lsit} -- list of tokens of second equation
        eqTok3 {lsit} -- list of tokens of third equation
        solveFor -- string/character -- variable for which equation is being solved.

    Returns:
        tokenLastString {string} -- last step in string form
        animations {list} -- list of step by step tokens
        comments {list} -- list of comments
    '''
    animation = []
    comments = []

    variables = []   # List of variables with respect to which equation can be solved.
    eqnTokens = [eqTok1, eqTok2, eqTok3]   # Stores list of strings for 3 equations.
    LandR_tokens = []   # ith entry stores L & R tokens for ith eqations.

    for _, tokens in enumerate(eqnTokens):
        lTokens, rTokens = getLHSandRHS(tokens)
        variablesEach = getVariables(lTokens, rTokens)
        variables.extend(variablesEach)
        LandR_tokens.append([lTokens, rTokens])
    variables = list(dict.fromkeys(variables))
    variables.sort()    # List of all the variables in all 3 equation in sorted order

    for i, tokens in enumerate(LandR_tokens):
        lTokens, rTokens, _, _, animationEach, commentsEach = simplifyEquation(tokens[0], tokens[1])
        animationEach = [[]] + animationEach
        if i == 0:
            commentsEach = [['Simplifying the ' + str(i + 1) + 'st ' + 'equation']] + commentsEach
        if i == 1:
            commentsEach = [['Simplifying the ' + str(i + 1) + 'nd ' + 'equation']] + commentsEach
        elif i == 2:
            commentsEach = [['Simplifying the ' + str(i + 1) + 'rd  ' + 'equation']] + commentsEach
        animation.extend(animationEach)
        comments.extend(commentsEach)
        LandR_tokens[i] = [lTokens, rTokens]

    coefficients = coeffCalculator(LandR_tokens, variables)   # (as of now) its a 3 by 4 matrix; each row has coeff of x, y, z and constant term.
    matD, matDx, matDy, matDz = cramerMatrices(coefficients)
    comments, animation, trivial = getResult(matD, matDx, matDy, matDz, variables, comments, animation, solveFor)
    if trivial:
        lastTokenString = tokensToString(animation[-1])
    else:
        lastTokenString = 'No Trivial Solution'
    return lastTokenString, animation, comments
