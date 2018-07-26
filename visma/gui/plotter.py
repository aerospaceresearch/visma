import numpy as np

from visma.io.tokenize import getLHSandRHS
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.io.checks import findWRTVariable, whichInputType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

###########
# backend #
###########


def graphPlot(tokens):

    eqType = whichInputType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(findWRTVariable(LHStok, RHStok))
    dim = len(variables)
    if (dim == 1 and eqType == "expression") or (dim == 2 and eqType == "equation"):
        X, Y, LHS, RHS = plot2D(LHStok, RHStok, variables, eqType)
        Z = None
        return X, Y, Z, LHS, RHS
    elif (dim == 2 and eqType == "expression") or (dim == 3 and eqType == "equation"):
        X, Y, Z, LHS, RHS = plot3D(LHStok, RHStok, variables, eqType)
        return X, Y, Z, LHS, RHS


def plot2D(LHStok, RHStok, variables, type):

    # FIXME: Quite basic right now. Needs fix for multi-variables

    graphVars = [None]*2
    delta = 0.1
    xRange = np.arange(-10, 10, delta)
    yRange = np.arange(-10, 10, delta)
    graphVars[0], graphVars[1] = np.meshgrid(xRange, yRange)

    LHS = 0
    coeff = 1
    for token in LHStok:
        if isinstance(token, Variable):
            LHS += coeff*token.coefficient
            for val, pow in zip(token.value, token.power):
                LHS *= graphVars[variables.index(val)]**pow
        elif isinstance(token, Binary) and token.value == '-':
            coeff = -1
        elif isinstance(token, Binary) and token.value == '+':
            coeff = 1
        elif isinstance(token, Constant):
            LHS += coeff*token.value
    if type == "equation":
        RHS = 0
        coeff = 1
        for token in RHStok:
            if isinstance(token, Variable):
                RHS += coeff*token.coefficient
                for val, pow in zip(token.value, token.power):
                    RHS *= graphVars[variables.index(val)]**pow
            elif isinstance(token, Binary) and token.value == '-':
                coeff = -1
            elif isinstance(token, Binary) and token.value == '+':
                coeff = 1
            elif isinstance(token, Constant):
                RHS += coeff*token.value
    elif type == "expression":
        RHS = graphVars[1]

    return graphVars[0], graphVars[1], LHS, RHS


def plot3D():
    pass


#######
# GUI #
#######


def plotFigure(workspace):
    workspace.figure = Figure()
    workspace.canvas = FigureCanvas(workspace.figure)

    # workspace.figure.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom')]

    workspace.toolbar = NavigationCustomToolbar(workspace.canvas, workspace)
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(workspace.canvas)
    layout.addWidget(workspace.toolbar)
    return layout


def plot(workspace):

    X, Y, Z, LHS, RHS = graphPlot(workspace.eqToks[-1])
    if Z is None:
        ax = workspace.figure.add_subplot(111)
        ax.clear()
        ax.contour(X, Y, (LHS - RHS), [0])
        ax.grid()
        workspace.figure.set_tight_layout({"pad": 1})  # removes extra padding
        workspace.canvas.draw()
