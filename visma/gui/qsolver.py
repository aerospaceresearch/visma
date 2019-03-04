from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

from visma.io.tokenize import removeSpaces, getTerms, normalize, tokenizeSymbols, removeUnary, getToken, getLHSandRHS
from visma.io.checks import checkEquation, checkTypes
from visma.io.parser import tokensToLatex
# from visma.gui.plotter import plot
from visma.simplify.simplify import simplify, simplifyEquation


def quickSimplify(workSpace):
    """Dynamic simplifier for simplifying expression as it is being typed

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        qSolution/log {string} -- quick solution or error log
        enableInteraction {bool} -- if False disables 'visma'(interaction) button
    """
    # FIXME: Crashes for some cases. Find and fix.
    qSolution = ""
    input = workSpace.textedit.toPlainText()
    cleanInput = removeSpaces(input)
    terms = getTerms(cleanInput)
    normalizedTerms = normalize(terms)
    symTokens = tokenizeSymbols(normalizedTerms)
    normalizedTerms, symTokens = removeUnary(normalizedTerms, symTokens)
    if checkEquation(normalizedTerms, symTokens) is True and input != "":
        if symTokens and symTokens[-1] is not False:
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
            # workSpace.eqToks = equationTokens
            # plot(workSpace)
            return qSolution, True
        elif symTokens:
            log = "Invalid Expression"
            return log, False
        else:
            log = ""
            return log, False
    else:
        log = ""
        if input != "":
            _, log = checkEquation(normalizedTerms, symTokens)
        return log, False


#######
# GUI #
#######


def qSolveFigure(workSpace):
    """GUI layout for quick simplifier

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        qSolLayout {QtWidgets.QVBoxLayout} -- quick simplifier layout
    """

    bg = workSpace.palette().window().color()
    bgColor = (bg.redF(), bg.greenF(), bg.blueF())
    workSpace.qSolveFigure = Figure(edgecolor=bgColor, facecolor=bgColor)
    workSpace.solcanvas = FigureCanvas(workSpace.qSolveFigure)
    workSpace.qSolveFigure.clear()
    qSolLayout = QtWidgets.QVBoxLayout()
    qSolLayout.addWidget(workSpace.solcanvas)

    return qSolLayout


def renderQuickSol(workSpace, showQSolver):
    """Renders quick solution in matplotlib figure

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout
    """
    if showQSolver is True:
        quickSolution = workSpace.qSol
    else:
        quickSolution = ""
    workSpace.qSolveFigure.suptitle(quickSolution, x=0.01,
                                    horizontalalignment='left',
                                    verticalalignment='top')
    #                               size=qApp.font().pointSize()*1.5)
    workSpace.solcanvas.draw()
