import numpy as np

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

from visma.io.checks import getVariables, getTokensType
from visma.io.tokenize import getLHSandRHS
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.functions.structure import FuncOp
from visma.functions.variable import Variable


def graphPlot(tokens):
    """Function for plotting graphs in 2D and 3D space

    2D graphs are plotted for expression in one variable and equations in two variables. 3D graphs are plotted for expressions in two variables and equations in three variables.

    Arguments:
        tokens {list} -- list of function tokens

    Returns:
        graphVars {list} -- variables to be plotted on the graph
        func {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
        variables {list} -- variables in given equation

    Note:
        The func obtained from graphPlot() funtion is of different type for 2D and 3D plots. For 2D func is a numpy array and for 3D func is a function.
    """

    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(getVariables(LHStok, RHStok))
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
    """Returns function array for 2D plots

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        variables {list} -- variables in equation

    Returns:
        graphVars {list} -- variables for plotting
        func {numpy.array} -- equation to be plotted in 3D
    """

    delta = 0.1
    xrange = np.arange(-10, 10, delta)
    yrange = np.arange(-10, 10, delta)
    graphVars = np.meshgrid(xrange, yrange)
    function = getFunction(LHStok, RHStok, variables, graphVars, 2)
    return graphVars, function


def plotIn3D(LHStok, RHStok, variables):
    """Returns function for 3D plots

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        variables {list} -- variables in equation

    Returns:
        graphVars {list} -- variables for plotting
        func {function} -- equation to be plotted in 3D
    """

    xmin, xmax, ymin, ymax, zmin, zmax = (-10, 10)*3
    xrange = np.linspace(xmin, xmax, 25)
    yrange = np.linspace(ymin, ymax, 25)
    zrange = np.linspace(zmin, zmax, 25)
    graphVars = [xrange, yrange, zrange]

    def func(x, y, z):
        graphVars = [x, y, z]
        return getFunction(LHStok, RHStok, variables, graphVars, 3)

    return graphVars, func


def getFunction(LHStok, RHStok, eqnVars, graphVars, dim):
    """Returns function for plotting

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        eqnVars {list} -- variables in equation
        graphVars {list} -- variables for plotting
        dim {int} -- dimenion of plot

    Returns:
        (LHS - RHS) {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
    """
    for token in LHStok:
        LHS = getFuncExpr(LHStok, eqnVars, graphVars)
    if len(eqnVars) == dim:
        RHS = getFuncExpr(RHStok, eqnVars, graphVars)
    elif len(eqnVars) == dim - 1:
        RHS = graphVars[-1]
    return LHS - RHS


def getFuncExpr(exprTok, eqnVars, graphVars):
    """Allocates variables in equation to graph variables to give final function compatible for plotting

    Arguments:
        exprTok {list} -- expression tokens
        eqnVars {list} -- variables in equation
        graphVars {list} -- variables for plotting

    Returns:
        expr {numpy.array(2D)/function(3D)} -- expression converted to compatible data type for plotting
    """
    expr = 0
    coeff = 1
    for token in exprTok:
        if isinstance(token, Variable):
            varProduct = 1
            for value, power in zip(token.value, token.power):
                varProduct *= graphVars[eqnVars.index(value)]**power
            expr += coeff*token.coefficient*varProduct
        elif isinstance(token, Constant):
            expr += coeff*token.value
        elif isinstance(token, FuncOp):
            pass
        elif isinstance(token, Binary) and token.value == '-':
            coeff = -1
        elif isinstance(token, Binary) and token.value == '+':
            coeff = 1
    return expr


#######
# GUI #
#######


def plotFigure(workspace):
    """GUI layout for plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        layout {QtWidgets.QVBoxLayout} -- contains matplot figure
    """
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
    """Renders plot for functions in 2D and 3D

    Maps points from the numpy arrays for variables in given equation on the 2D/3D plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
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
