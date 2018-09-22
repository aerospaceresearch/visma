from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

from visma.io.tokenize import removeSpaces, getTerms, normalize, tokenizeSymbols, removeUnary, getToken, getLHSandRHS
from visma.io.checks import checkEquation, checkTypes
from visma.io.parser import tokensToLatex
# from visma.gui.plotter import plot
from visma.simplify.simplify import simplify, simplifyEquation


def quickSimplify(workspace):
    """Dynamic simplifier for simplifying expression as it is being typed

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        qSolution/log {string} -- quick solution or error log
    """
    # FIXME: Crashes for some cases. Find and fix.
    qSolution = ""
    input = workspace.textedit.toPlainText()
    cleanInput = removeSpaces(input)
    terms = getTerms(cleanInput)
    normalizedTerms = normalize(terms)
    symTokens = tokenizeSymbols(normalizedTerms)
    normalizedTerms, symTokens = removeUnary(normalizedTerms, symTokens)
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
            # workspace.eqToks = equationTokens
            # plot(workspace)
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
    """GUI layout for quick simplifier

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        qSolLayout {QtWidgets.QVBoxLayout} -- quick simplifier layout
    """

    bg = workspace.palette().window().color()
    bgcolor = (bg.redF(), bg.greenF(), bg.blueF())
    workspace.qSolveFigure = Figure(edgecolor=bgcolor, facecolor=bgcolor)
    workspace.solcanvas = FigureCanvas(workspace.qSolveFigure)
    workspace.qSolveFigure.clear()
    qSolLayout = QtWidgets.QVBoxLayout()
    qSolLayout.addWidget(workspace.solcanvas)

    return qSolLayout


def showQSolve(workspace, showQuickSim):
    """Renders quick solution in matplotlib figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    if showQuickSim is True:
        quickSolution = workspace.qSol
    else:
        quickSolution = ""
    workspace.qSolveFigure.suptitle(quickSolution, x=0.01,
                                    horizontalalignment='left',
                                    verticalalignment='top')
    #                               size=qApp.font().pointSize()*1.5)
    workspace.solcanvas.draw()
