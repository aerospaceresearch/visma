from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.simplify.simplify import simplifyEquation, moveRTokensToLTokens
from visma.io.parser import tokensToString
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.matrix.structure import SquareMat
from visma.matrix.special import cramerMatrices


def coeffCalculator(LandR_tokens):
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
                if token.value == ['x']:
                    coefficients[i][0] = token.coefficient
                elif token.value == ['y']:
                    coefficients[i][1] = token.coefficient
                elif token.value == ['z']:
                    coefficients[i][2] = token.coefficient
            if isinstance(token, Constant):
                coefficients[i][3] = token.value

    return coefficients


def getResult(matD, matDx, matDy, matDz):
    '''Calculates values of x, y and z'''
    x = 0
    y = 0
    z = 0
    trivial = True
    detD = float(tokensToString(matD.determinant()))
    detDx = float(tokensToString(matDx.determinant()))
    detDy = float(tokensToString(matDy.determinant()))
    detDz = float(tokensToString(matDz.determinant()))
    if detD == 0:
        trivial = False
    if trivial:
        x = detDx/detD
        y = detDy/detD
        z = detDz/detD
    return trivial, x, y, z


def simulSolver(eqStr1, eqStr2, eqStr3, solveFor):
    '''
    Main driver function in simulEqn.py

    Arguments:
    eqStr{i} -- i = 1, 2, 3 -- equation strings of equations inputted by user.
    solveFor -- string/character -- variable for which equation is being solved.

    Returns:
    outputString -- Either value of variable to be solved for OR
                    Prompt indicating non trivial solution
    '''
    eqnStrs = [eqStr1, eqStr2, eqStr3]   # Stores list of strings for 3 equations.
    eqnTokens = [tokenizer(eqn) for eqn in eqnStrs]   # Stores lisk of tokens for each equation.
    LandR_tokens = []   # ith entry stores L & R tokens for ith eqations.
    for _, tokens in enumerate(eqnTokens):
        lTokens, rTokens = getLHSandRHS(tokens)
        LandR_tokens.append([lTokens, rTokens])
    for i, tokens in enumerate(LandR_tokens):
        lTokens, rTokens, _, _, _, _ = simplifyEquation(tokens[0], tokens[1])
        LandR_tokens[i] = [lTokens, rTokens]
    coefficients = coeffCalculator(LandR_tokens)   # (as of now) its a 3 by 4 matrix; each row has coeff of x, y, z and constant term.
    matD, matDx, matDy, matDz = cramerMatrices(coefficients)
    trivial, x, y, z = getResult(matD, matDx, matDy, matDz)
    if trivial:
        if solveFor == 'x':
            return ('x = ' + str(x))
        elif solveFor == 'y':
            return ('y = ' + str(y))
        elif solveFor == 'z':
            return ('z = ' + str(z))
    else:
        return 'No Trivial Solution'
