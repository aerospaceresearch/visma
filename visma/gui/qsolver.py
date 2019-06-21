from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

from visma.io.tokenize import removeSpaces, getTerms, normalize, tokenizeSymbols, removeUnary, getToken, getLHSandRHS
from visma.io.checks import checkEquation, checkTypes
from visma.io.parser import tokensToLatex
# from visma.gui.plotter import plot
from visma.simplify.simplify import simplify, simplifyEquation
from visma.gui import logger


def quickSimplify(workspace):
    """Dynamic simplifier for simplifying expression as it is being typed

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        qSolution/log {string} -- quick solution or error log
        enableInteraction {bool} -- if False disables 'visma'(interaction) button
    """
    # FIXME: Crashes for some cases. Find and fix.
    logger.setLogName('qsolver')
    logger.setLevel(0)
    qSolution = ""
    strIn = workspace.textedit.toPlainText()
    cleanInput = removeSpaces(strIn)
    if ';' in cleanInput:
        return "", True, True
    terms = getTerms(cleanInput)
    normalizedTerms = normalize(terms)
    symTokens = tokenizeSymbols(normalizedTerms)
    normalizedTerms, symTokens = removeUnary(normalizedTerms, symTokens)
    if checkEquation(normalizedTerms, symTokens) is True and strIn != "":
        if symTokens and symTokens[-1] is not False:
            tokens = getToken(normalizedTerms, symTokens)
            tokens = tokens.tokens
            lhs, rhs = getLHSandRHS(tokens)
            _, solutionType = checkTypes(lhs, rhs)
            lhs, rhs = getLHSandRHS(tokens)
            if solutionType == 'expression':
                _, _, _, equationTokens, _ = simplify(tokens)
                qSolution = r'$ ' + '= \ '
            else:
                _, _, _, _, equationTokens, _ = simplifyEquation(lhs, rhs)
                qSolution = r'$ ' + '\Rightarrow \ '
            qSolution += tokensToLatex(equationTokens[-1]) + ' $'
            # workspace.eqToks = equationTokens
            # plot(workspace)
            return qSolution, True, False
        elif symTokens:
            log = "Invalid Expression"
            workspace.logBox.append(logger.error(log))
            return log, False, _
        else:
            log = ""
            workspace.logBox.append(logger.error(log))
            return log, False, _
    else:
        log = ""
        if strIn != "":
            _, log = checkEquation(normalizedTerms, symTokens)
            workspace.logBox.append(logger.error(log))
        return log, False, _


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


def renderQuickSol(workspace, log, showQSolver):
    """Renders quick solution in matplotlib figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    if showQSolver is True:
        quickSolution = log
    else:
        quickSolution = ""
    workspace.qSolveFigure.suptitle(quickSolution, x=0.01,
                                    horizontalalignment='left',
                                    verticalalignment='top')
    #                               size=qApp.font().pointSize()*1.5)
    workspace.solcanvas.draw()
