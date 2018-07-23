from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

import numpy as np
from visma.io.tokenize import getLHSandRHS
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.io.checks import isEquation

###########
# backend #
###########


def plotThis(equationTokens):

    # FIXME: Quite basic right now. Needs fix for multi-variables

    LHStok, RHStok = getLHSandRHS(equationTokens)

    varDict = {}
    delta = 0.1
    range = np.arange(-100, 100, delta)
    yrange = np.arange(-100, 100, delta)
    varDict['x'], varDict['y'] = np.meshgrid(range, yrange)

    LHS = 0
    coeff = 1
    for token in LHStok:
        if isinstance(token, Variable):
            LHS += coeff*token.coefficient
            for eachValue, eachPower in zip(token.value, token.power):
                LHS *= (varDict[eachValue]**eachPower)
        elif isinstance(token, Binary) and token.value == '-':
            coeff = -1
        elif isinstance(token, Constant):
            LHS += coeff*token.value
    RHS = varDict['y']
    if(isEquation(LHStok, RHStok)):
        RHS = 0

    return varDict['x'], varDict['y'], LHS, RHS


#######
# GUI #
#######


def plotFigure(workspace):
    workspace.figure = Figure()
    workspace.canvas = FigureCanvas(workspace.figure)

    # workspace.figure.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

    workspace.toolbar = NavigationCustomToolbar(workspace.canvas, workspace)
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(workspace.canvas)
    layout.addWidget(workspace.toolbar)
    return layout


def plot(workspace):
    ax = workspace.figure.add_subplot(111)
    ax.clear()
    x, y, LHS, RHS = plotThis(workspace.eqToks[-1])
    ax.contour(x, y, (LHS - RHS), [0])
    ax.grid()
    workspace.figure.set_tight_layout({"pad": 1})  # removes extra padding
    workspace.canvas.draw()
