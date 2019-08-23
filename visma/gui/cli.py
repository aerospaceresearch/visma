import copy
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout
from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.discreteMaths.combinatorics import factorial, combination, permutation
from visma.io.checks import checkTypes
from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.io.parser import resultStringCLI, resultMatrixString
from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.solvers.solve import solveFor
from visma.solvers.polynomial.roots import rootFinder
from visma.solvers.simulEqn import simulSolver
from visma.transform.factorization import factorize
from visma.matrix.structure import Matrix, SquareMat
from visma.matrix.operations import simplifyMatrix, addMatrix, subMatrix, multiplyMatrix
from visma.gui.plotter import plotFigure2D, plotFigure3D, plot


class App(QMainWindow):
    def __init__(self, tokens):
        super().__init__()
        self.setWindowTitle('Plots')
        self.setGeometry(300, 300, 450, 450)
        self.table_widget = PlotWindow(self, tokens)
        self.setCentralWidget(self.table_widget)
        self.show()


class PlotWindow(QWidget):
    def __init__(self, parent, tokens):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.tabPlot = QTabWidget()
        self.tabPlot.tab1 = QWidget()
        self.tabPlot.tab2 = QWidget()
        self.tabPlot.resize(300, 200)
        self.tabPlot.addTab(self.tabPlot.tab1, "2D-Plot")
        self.tabPlot.addTab(self.tabPlot.tab2, "3D-Plot")
        self.tabPlot.tab1.setLayout(plotFigure2D(self))
        self.tabPlot.tab2.setLayout(plotFigure3D(self))
        self.layout.addWidget(self.tabPlot)
        plot(self, tokens)


def commandExec(command):
    operation = command.split('(', 1)[0]
    inputEquation = command.split('(', 1)[1][:-1]
    matrix = False      # True when matrices operations are present in the code.
    if operation[0:4] == 'mat_':
        matrix = True

    if not matrix:
        """
        This part handles the cases when VisMa is NOT dealing with matrices.

        Boolean flags used in code below:
        simul -- {True} when VisMa is dealing with simultaneous equations & {False} in all other cases
        """
        varName = None
        if ',' in inputEquation:
            varName = inputEquation.split(',')[1]
            varName = "".join(varName.split())
            inputEquation = inputEquation.split(',')[0]

        simul = False   # True when simultaneous equation is present
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

        if operation == 'plot':
            app = QApplication(sys.argv)
            App(tokens)
            sys.exit(app.exec_())
        elif operation == 'simplify':
            if solutionType == 'expression':
                tokens, _, _, equationTokens, comments = simplify(tokens)
            else:
                lTokens, rTokens, _, _, equationTokens, comments = simplifyEquation(lTokens, rTokens)
        elif operation == 'addition':
            if solutionType == 'expression':
                tokens, _, _, equationTokens, comments = addition(tokens, True)
            else:
                lTokens, rTokens, _, _, equationTokens, comments = additionEquation(lTokens, rTokens, True)
        elif operation == 'subtraction':
            if solutionType == 'expression':
                tokens, _, _, equationTokens, comments = subtraction(tokens, True)
            else:
                lTokens, rTokens, _, _, equationTokens, comments = subtractionEquation(lTokens, rTokens, True)
        elif operation == 'multiplication':
            if solutionType == 'expression':
                tokens, _, _, equationTokens, comments = multiplication(tokens, True)
            else:
                lTokens, rTokens, _, _, equationTokens, comments = multiplicationEquation(lTokens, rTokens, True)
        elif operation == 'division':
            if solutionType == 'expression':
                tokens, _, _, equationTokens, comments = division(tokens, True)
            else:
                lTokens, rTokens, _, _, equationTokens, comments = divisionEquation(lTokens, rTokens, True)
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
        if operation != 'plot':
            # FIXME: when either plotting window or GUI window is opened from CLI and after it is closed entire CLI exits, it would be better if it is avoided
            final_string = resultStringCLI(equationTokens, operation, comments, solutionType, simul)
            print(final_string)
    else:
        """
        This part handles the cases when VisMa is dealing with matrices.

        Boolean flags used in code below:
        dualOperand -- {True} when the matrix operations require two operands (used in operations like addition, subtraction etc)
        nonMatrixResult -- {True} when the result after performing operations on the Matrix is not a Matrix (in operations like Determinant, Trace etc.)
        scalarOperations -- {True} when one of the operand in a scalar (used in operations like Scalar Addition, Scalar Subtraction etc.)
        """
        operation = operation[4:]
        dualOperand = False
        nonMatrixResult = False
        scalarOperations = False
        if ', ' in inputEquation:
            dualOperand = True
            [inputEquation1, inputEquation2] = inputEquation.split(', ')
            if '[' in inputEquation1:
                inputEquation1 = inputEquation1[1:][:-1]
                inputEquation1 = inputEquation1.split('; ')
                matrixOperand1 = []
                for row in inputEquation1:
                    row1 = row.split(' ')
                    for i, _ in enumerate(row1):
                        row1[i] = tokenizer(row1[i])
                    matrixOperand1.append(row1)
                Matrix1 = Matrix()
                Matrix1.value = matrixOperand1
                inputEquation2 = inputEquation2[1:][:-1]
                inputEquation2 = inputEquation2.split('; ')
                matrixOperand2 = []
                for row in inputEquation2:
                    row1 = row.split(' ')
                    for i, _ in enumerate(row1):
                        row1[i] = tokenizer(row1[i])
                    matrixOperand2.append(row1)
                Matrix2 = Matrix()
                Matrix2.value = matrixOperand2
                Matrix1_copy = copy.deepcopy(Matrix1)
                Matrix2_copy = copy.deepcopy(Matrix2)
            else:
                scalarOperations = True
                scalar = inputEquation1
                scalarTokens = scalar
                # scalarTokens = tokenizer(scalar)
                inputEquation2 = inputEquation2[1:][:-1]
                inputEquation2 = inputEquation2.split('; ')
                matrixOperand2 = []
                for row in inputEquation2:
                    row1 = row.split(' ')
                    for i, _ in enumerate(row1):
                        row1[i] = tokenizer(row1[i])
                    matrixOperand2.append(row1)
                Matrix2 = Matrix()
                Matrix2.value = matrixOperand2
                scalarTokens_copy = copy.deepcopy(scalarTokens)
                Matrix2_copy = copy.deepcopy(Matrix2)

        else:
            inputEquation = inputEquation[1:][:-1]
            inputEquation = inputEquation.split('; ')

            matrixOperand = []
            for row in inputEquation:
                row1 = row.split(' ')
                for i, _ in enumerate(row1):
                    row1[i] = tokenizer(row1[i])
                matrixOperand.append(row1)

            Matrix0 = Matrix()
            Matrix0.value = matrixOperand
            Matrix0_copy = copy.deepcopy(Matrix0)
        if operation == 'simplify':
            MatrixResult = simplifyMatrix(Matrix0)
        elif operation == 'add':
            MatrixResult = addMatrix(Matrix1, Matrix2)
        elif operation == 'sub':
            MatrixResult = subMatrix(Matrix1, Matrix2)
        elif operation == 'mult':
            MatrixResult = multiplyMatrix(Matrix1, Matrix2)
        elif operation == 'determinant':
            nonMatrixResult = True
            sqMatrix = SquareMat()
            sqMatrix.value = Matrix0.value
            result = sqMatrix.determinant()
        elif operation == 'trace':
            nonMatrixResult = True
            sqMatrix = SquareMat()
            sqMatrix.value = Matrix0.value
            result = sqMatrix.traceMat()
        elif operation == 'inverse':
            sqMatrix = SquareMat()
            sqMatrix.value = Matrix0.value
            MatrixResult = SquareMat()
            MatrixResult = sqMatrix.inverse()

        finalCLIstring = ''
        if dualOperand:
            if not scalarOperations:
                finalCLIstring = resultMatrixString(operation=operation, operand1=Matrix1_copy, operand2=Matrix2_copy, result=MatrixResult)
            else:
                finalCLIstring = resultMatrixString(operation=operation, operand1=scalarTokens_copy, operand2=Matrix2_copy, result=MatrixResult)
        else:
            if nonMatrixResult:
                finalCLIstring = resultMatrixString(operation=operation, operand1=Matrix0_copy, nonMatrixResult=True, result=result)
            else:
                finalCLIstring = resultMatrixString(operation=operation, operand1=Matrix0_copy, result=MatrixResult)
        print(finalCLIstring)
