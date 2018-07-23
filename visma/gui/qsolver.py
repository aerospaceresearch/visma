from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

from visma.io.tokenize import removeSpaces, getTerms, normalize, tokenizeSymbols, removeUnary, getToken, getLHSandRHS
from visma.io.checks import checkEquation, checkTypes
from visma.io.parser import tokensToLatex
from visma.simplify.simplify import simplify, simplifyEquation


###########
# backend #
###########


def quickSimplify(input):
    # FIXME: Crashes for some cases. Find and fix.
    qSolution = ""
    cleanInput = removeSpaces(input)
    terms = getTerms(cleanInput)
    normalizedTerms = normalize(terms)
    symTokens = tokenizeSymbols(normalizedTerms)
    terms, symTokens = removeUnary(normalizedTerms, symTokens)
    if checkEquation(normalizedTerms, symTokens) is True and input != "":
        if symTokens[-1] is not False:
            tokens = getToken(normalizedTerms, symTokens)
            tokens = tokens.tokens
            lhs, rhs = getLHSandRHS(tokens)
            _, solutionType = checkTypes(
                lhs, rhs)
            if solutionType == 'expression':
                _, _, _, equationTokens, _ = simplify(tokens)
                qSolution = r'$ ' + '= \ '
            else:
                _, _, _, _, equationTokens, _ = simplifyEquation(lhs, rhs)
                qSolution = r'$ ' + '\Rightarrow \ '
            qSolution += tokensToLatex(equationTokens[-1]) + ' $'
            return qSolution
        else:
            log = "Invalid Expression"
            return log
    else:
        log = ""
        if input != "":
            _, log = checkEquation(normalizedTerms, symTokens)
        return log


#######
# GUI #
#######


def qSolveFigure(workspace):
    workspace.qSolveFigure = Figure()
    workspace.solcanvas = FigureCanvas(workspace.qSolveFigure)
    workspace.qSolveFigure.clear()

    stepslayout = QtWidgets.QVBoxLayout()
    stepslayout.addWidget(workspace.solcanvas)
    return stepslayout


def showQSolve(workspace):
    workspace.qSolveFigure.suptitle(workspace.qSol,
                                    horizontalalignment='center',
                                    verticalalignment='top')
    #                          size=qApp.font().pointSize()*1.5)
    workspace.solcanvas.draw()
