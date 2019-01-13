from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.io.checks import checkTypes
from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.io.parser import tokensToString
from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.solvers.solve import solveFor
from visma.solvers.polynomial.roots import quadraticRoots
from visma.transform.factorization import factorize


def commandExec(command):
    operation = command.split('(', 1)[0]
    inputEquation = command.split('(', 1)[1][:-1]
    if ',' in inputEquation:
        varName = inputEquation.split(',')[1]
        inputEquation = inputEquation.split(',')[0]

    lhs = []
    rhs = []
    solutionType = ''
    lTokens = []
    rTokens = []
    equationTokens = []
    comments = []

    tokens = tokenizer(inputEquation)
    lhs, rhs = getLHSandRHS(tokens)
    lTokens = lhs
    rTokens = rhs
    _, solutionType = checkTypes(lhs, rhs)

    if operation == 'simplify':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = simplify(tokens)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = simplifyEquation(lTokens, rTokens)
    elif operation == 'addition':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = addition(
                tokens, True)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = additionEquation(
                lTokens, rTokens, True)
    elif operation == 'subtraction':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = subtraction(
                tokens, True)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = subtractionEquation(
                lTokens, rTokens, True)
    elif operation == 'multiplication':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = multiplication(
                tokens, True)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = multiplicationEquation(
                lTokens, rTokens, True)
    elif operation == 'division':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = division(
                tokens, True)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = divisionEquation(
                lTokens, rTokens, True)
    elif operation == 'simplify':
        if solutionType == 'expression':
            tokens, _, _, equationTokens, comments = simplify(tokens)
        else:
            lTokens, rTokens, _, _, equationTokens, comments = simplifyEquation(lTokens, rTokens)
    elif operation == 'factorize':
        tokens, _, _, equationTokens, comments = factorize(tokens)
    elif operation == 'find-roots':
        lTokens, rTokens, _, _, equationTokens, comments = quadraticRoots(lTokens, rTokens)
    elif operation == 'solve':
        lhs, rhs = getLHSandRHS(tokens)
        lTokens, rTokens, _, _, equationTokens, comments = solveFor(lTokens, rTokens, varName)
    elif operation == 'integrate':
        lhs, rhs = getLHSandRHS(tokens)
        lTokens, _, _, equationTokens, comments = integrate(lTokens, varName)
    elif operation == 'differentiate':
        lhs, rhs = getLHSandRHS(tokens)
        lTokens, _, _, equationTokens, comments = differentiate(lTokens, varName)
    printOnCLI(equationTokens, operation, comments)


def printOnCLI(equationTokens, operation, comments):
    equationString = []
    for x in equationTokens:
        equationString.append(tokensToString(x))
    commentsString = []
    for x in comments:
        for y in x:
            commentsString.append([y.translate({ord(c): None for c in '${\}'})])
    commentsString = [[]] + commentsString
    finalSteps = ""
    finalSteps = "INPUT: " + equationString[0] + "\n"
    finalSteps += "OPERATION: " + operation + "\n"
    finalSteps += "OUTPUT: " + equationString[-1] + 2*"\n"
    for i, _ in enumerate(equationString):
        finalSteps += equationString[i]
        if comments[i] != []:
            finalSteps += "\n" + "(" + str(commentsString[i][0]) + ")" + 2*"\n"
        else:
            finalSteps += 2*"\n"
    print(finalSteps)
