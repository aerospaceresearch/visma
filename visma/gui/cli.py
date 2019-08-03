from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.discreteMaths.combinatorics import factorial, combination, permutation
from visma.io.checks import checkTypes
from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.io.parser import resultStringCLI
from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.solvers.solve import solveFor
from visma.solvers.polynomial.roots import rootFinder
from visma.solvers.simulEqn import simulSolver
from visma.transform.factorization import factorize
from visma.matrix.structure import Matrix, SquareMat


def commandExec(command):
    operation = command.split('(', 1)[0]
    inputEquation = command.split('(', 1)[1][:-1]
    matrix = False
    if operation[0:4] == 'mat_':
        matrix = True

    if not matrix:
        varName = None
        if ',' in inputEquation:
            varName = inputEquation.split(',')[1]
            varName = "".join(varName.split())
            inputEquation = inputEquation.split(',')[0]

        simul = False
        if (inputEquation.count(';') == 2) and (operation == 'solve'):
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
            lTokens, rTokens, _, _, equationTokens, comments = rootFinder(lTokens, rTokens)
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
        elif operation == 'factorial':
            tokens, _, _, equationTokens, comments = factorial(tokens)
        elif operation == 'combination':
            n = tokenizer(inputEquation)
            r = tokenizer(varName)
            tokens, _, _, equationTokens, comments = combination(n, r)
        elif operation == 'permutation':
            n = tokenizer(inputEquation)
            r = tokenizer(varName)
            tokens, _, _, equationTokens, comments = permutation(n, r)
        elif operation == 'integrate':
            lhs, rhs = getLHSandRHS(tokens)
            lTokens, _, _, equationTokens, comments = integrate(lTokens, varName)
        elif operation == 'differentiate':
            lhs, rhs = getLHSandRHS(tokens)
            lTokens, _, _, equationTokens, comments = differentiate(lTokens, varName)
        final_string = resultStringCLI(equationTokens, operation, comments, solutionType, simul)
        print(final_string)
    else:
        operation = operation[4:]
        inputEquation = "[1 2 3; 12 12 33; 12 311 11]"
        inputEquation = inputEquation[1:][:-1]
        inputEquation = inputEquation.split('; ')
        matrixOperand = []
        for row in inputEquation:
            row1 = row.split(' ')
            for i, _ in enumerate(row1):
                row1[i] = tokenizer(row1[i])
            matrixOperand.append(row1)
        if operation == 'simplify':
            operandMatrix = Matrix(value=matrixOperand)
            operandMatrix = SquareMat(value=matrixOperand)
            print(operandMatrix.determinant)            