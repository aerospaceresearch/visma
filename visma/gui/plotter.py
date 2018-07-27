import numpy as np

from visma.io.tokenize import getLHSandRHS
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.io.checks import findWRTVariable, getTokensType

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
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
        graphVars, func = plotIn2D(LHStok, RHStok, variables)
        if dim == 1:
            variables.append('f(' + variables[0] + ')')
    elif (dim == 2 and eqType == "expression") or (dim == 3 and eqType == "equation"):
        graphVars, func = plotIn3D(LHStok, RHStok, variables)
        if dim == 2:
            variables.append('f(' + variables[0] + ',' + variables[1] + ')')
    else:
        return [], None, None
    return graphVars, func, variables


def plotIn2D(LHStok, RHStok, variables):

    delta = 0.1
    xrange = np.arange(-10, 10, delta)
    yrange = np.arange(-10, 10, delta)
    graphVars = np.meshgrid(xrange, yrange)
    LHS = 0
    coeff = 1
    for token in LHStok:
        if isinstance(token, Variable):
            varProduct = 1
            for value, power in zip(token.value, token.power):
                varProduct *= graphVars[variables.index(value)]**power
            LHS += coeff*token.coefficient*varProduct
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
                varProduct = 1
                for value, power in zip(token.value, token.power):
                    varProduct *= graphVars[variables.index(value)]**power
                RHS += coeff*token.coefficient*varProduct
            elif isinstance(token, Binary) and token.value == '-':
                coeff = -1
            elif isinstance(token, Binary) and token.value == '+':
                coeff = 1
            elif isinstance(token, Constant):
                RHS += coeff*token.value
    elif len(variables) == 1:
        RHS = graphVars[-1]
    return graphVars, LHS - RHS


def plotIn3D(LHStok, RHStok, variables):

    xmin, xmax, ymin, ymax, zmin, zmax = (-10, 10)*3
    xrange = np.linspace(xmin, xmax, 25)
    yrange = np.linspace(ymin, ymax, 25)
    zrange = np.linspace(zmin, zmax, 25)
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
                varProduct = 1
                for value, power in zip(token.value, token.power):
                    varProduct *= funcVars[variables.index(value)]**power
                LHS += coeff*token.coefficient*varProduct
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
                    varProduct = 1
                    for value, power in zip(token.value, token.power):
                        varProduct *= funcVars[variables.index(value)]**power
                    RHS += coeff*token.coefficient*varProduct
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

    graphVars, func, variables = graphPlot(workspace.eqToks[-1])
    workspace.figure.clf()
    if len(graphVars) == 2:
        X, Y = graphVars[0], graphVars[1]
        ax = workspace.figure.add_subplot(111)
        ax.clear()
        ax.contour(X, Y, func, [0])
        ax.grid()
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        workspace.figure.set_tight_layout({"pad": 1})  # removes extra padding
    elif len(graphVars) == 3:
        xrange = graphVars[0]
        yrange = graphVars[1]
        zrange = graphVars[2]
        ax = Axes3D(workspace.figure)
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
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        ax.set_zlabel(r'$' + variables[2] + '$')
    workspace.canvas.draw()
