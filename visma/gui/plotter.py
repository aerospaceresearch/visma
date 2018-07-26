import numpy as np

from visma.io.tokenize import getLHSandRHS
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.io.checks import findWRTVariable, getTokensType

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

###########
# backend #
###########


def graphPlot(tokens):

    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(findWRTVariable(LHStok, RHStok))
    dim = len(variables)
    if (dim == 1 and eqType == "expression") or (dim == 2 and eqType == "equation"):
        graphVars, func = plot2D(LHStok, RHStok, variables, eqType)
    elif (dim == 2 and eqType == "expression") or (dim == 3 and eqType == "equation"):
        graphVars, func = plot3D(LHStok, RHStok, variables, eqType)
    else:
        return [], None, None
    return graphVars, func


def plot2D(LHStok, RHStok, variables, type):

    delta = 0.1
    xrange = np.arange(-10, 10, delta)
    yrange = np.arange(-10, 10, delta)
    graphVars = np.meshgrid(xrange, yrange)
    LHS = 0
    coeff = 1
    for token in LHStok:
        if isinstance(token, Variable):
            vals = 1
            for val, pow in zip(token.value, token.power):
                vals *= graphVars[variables.index(val)]**pow
            LHS += coeff*token.coefficient*vals
        elif isinstance(token, Binary) and token.value == '-':
            coeff = -1
        elif isinstance(token, Binary) and token.value == '+':
            coeff = 1
        elif isinstance(token, Constant):
            LHS += coeff*token.value
    if len(variables) == 2:
        RHS = 0
        coeff = 1
        for token in RHStok:
            if isinstance(token, Variable):
                vals = 1
                for val, pow in zip(token.value, token.power):
                    vals *= graphVars[variables.index(val)]**pow
                RHS += coeff*token.coefficient*vals
            elif isinstance(token, Binary) and token.value == '-':
                coeff = -1
            elif isinstance(token, Binary) and token.value == '+':
                coeff = 1
            elif isinstance(token, Constant):
                RHS += coeff*token.value
    elif len(variables) == 1:
        RHS = graphVars[-1]
    return graphVars, LHS - RHS


def plot3D(LHStok, RHStok, variables, type):

    xmin, xmax, ymin, ymax, zmin, zmax = (-10, 10)*3
    xrange = np.linspace(xmin, xmax, 30)
    yrange = np.linspace(xmin, xmax, 30)
    zrange = np.linspace(xmin, xmax, 30)
    graphVars = [xrange, yrange, zrange]
    func = getFunction(LHStok, RHStok, variables)

    return graphVars, func


def getFunction(LHStok, RHStok, variables):

    def func(x, y, z):
        funcVars = [x, y, z]
        LHS = 0
        coeff = 1
        for token in LHStok:
            if isinstance(token, Variable):
                vals = 1
                for val, pow in zip(token.value, token.power):
                    vals *= funcVars[variables.index(val)]**pow
                LHS += coeff*token.coefficient*vals
            elif isinstance(token, Binary) and token.value == '-':
                coeff = -1
            elif isinstance(token, Binary) and token.value == '+':
                coeff = 1
            elif isinstance(token, Constant):
                LHS += coeff*token.value
        if len(variables) == 3:
            RHS = 0
            coeff = 1
            for token in RHStok:
                if isinstance(token, Variable):
                    vals = 1
                    for val, pow in zip(token.value, token.power):
                        vals *= funcVars[variables.index(val)]**pow
                    RHS += coeff*token.coefficient*vals
                elif isinstance(token, Binary) and token.value == '-':
                    coeff = -1
                elif isinstance(token, Binary) and token.value == '+':
                    coeff = 1
                elif isinstance(token, Constant):
                    RHS += coeff*token.value
        elif len(variables) == 2:
            RHS = funcVars[-1]
        return LHS - RHS

    return func

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

    graphVars, func = graphPlot(workspace.eqToks[-1])
    if len(graphVars) == 2:
        X, Y = graphVars[0], graphVars[1]
        ax = workspace.figure.add_subplot(111)
        ax.clear()
        ax.contour(X, Y, func, [0])
        ax.grid()
        workspace.figure.set_tight_layout({"pad": 1})  # removes extra padding
        workspace.canvas.draw()
    elif len(graphVars) == 3:
        xrange = graphVars[0]
        yrange = graphVars[1]
        zrange = graphVars[2]
        ax = workspace.figure.add_subplot(111, projection='3d')
        for z in zrange:
            X, Y = np.meshgrid(xrange, yrange)
            Z = func(X, Y, z)
            ax.contour(X, Y, Z+z, [z], zdir='z')
        for y in yrange:
            X, Z = np.meshgrid(xrange, zrange)
            Y = func(X, y, Z)
            ax.contour(X, Y+y, Z, [y], zdir='y')
        for x in xrange:
            Y, Z = np.meshgrid(yrange, zrange)
            X = func(x, Y, Z)
            ax.contour(X+x, Y, Z, [x], zdir='x')
        xmin, xmax, ymin, ymax, zmin, zmax = (-10, 10)*3
        ax.set_xlim3d(xmin, xmax)
        ax.set_ylim3d(ymin, ymax)
        ax.set_zlim3d(zmin, zmax)
        workspace.canvas.draw()
    else:
        ax = workspace.figure.add_subplot(111)
        ax.clear()
