from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.io.checks import checkTypes
from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.io.parser import resultStringCLI
from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.solvers.solve import solveFor
from visma.solvers.polynomial.roots import quadraticRoots
from visma.solvers.simulEqn import simulSolver
from visma.transform.factorization import factorize


def commandExec(command):
    operation = command.split('(', 1)[0]
    inputEquation = command.split('(', 1)[1][:-1]

    varName = None
    if ',' in inputEquation:
        varName = inputEquation.split(',')[1]
        varName = "".join(varName.split())
        inputEquation = inputEquation.split(',')[0]

    simul = False
    if ';' in inputEquation:
        simul = True
        afterSplit = inputEquation.split(';')
        eqStr1 = afterSplit[0]
        eqStr2 = afterSplit[1]
        eqStr3 = afterSplit[2]

    lhs = []
    rhs = []
    solutionType = ''
    lTokens = []
    rTokens = []
    equationTokens = []
    comments = []
    if simul:
        tokens = [tokenizer(eqStr1), tokenizer(eqStr2), tokenizer(eqStr3)]
    else:
        tokens = tokenizer(inputEquation)
        if '=' in inputEquation:
            lhs, rhs = getLHSandRHS(tokens)
            lTokens = lhs
            rTokens = rhs
            _, solutionType = checkTypes(lhs, rhs)
        else:
            solutionType = 'expression'
            lhs, rhs = getLHSandRHS(tokens)
            lTokens = lhs
            rTokens = rhs

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
    elif operation == 'factorize':
        tokens, _, _, equationTokens, comments = factorize(tokens)
    elif operation == 'find-roots':
        lTokens, rTokens, _, _, equationTokens, comments = quadraticRoots(lTokens, rTokens)
    elif operation == 'solve':
        if simul:
            if varName is not None:
                _, equationTokens, comments = simulSolver(tokens[0], tokens[1], tokens[2], varName)
            else:
                _, equationTokens, comments = simulSolver(tokens[0], tokens[1], tokens[2])
            solutionType = equationTokens
        else:
            lhs, rhs = getLHSandRHS(tokens)
            lTokens, rTokens, _, _, equationTokens, comments = solveFor(lTokens, rTokens, varName)
    elif operation == 'integrate':
        lhs, rhs = getLHSandRHS(tokens)
        lTokens, _, _, equationTokens, comments = integrate(lTokens, varName)
    elif operation == 'differentiate':
        lhs, rhs = getLHSandRHS(tokens)
        lTokens, _, _, equationTokens, comments = differentiate(lTokens, varName)
    final_string = resultStringCLI(equationTokens, operation, comments, solutionType, simul)
    print(final_string)
