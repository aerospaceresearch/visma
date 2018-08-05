import numpy as np

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSlider, QSpinBox, QPushButton

from visma.io.checks import getVariables, getTokensType
from visma.io.tokenize import getLHSandRHS
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.functions.structure import FuncOp
from visma.functions.variable import Variable


def graphPlot(workspace):
    """Function for plotting graphs in 2D and 3D space

    2D graphs are plotted for expression in one variable and equations in two variables. 3D graphs are plotted for expressions in two variables and equations in three variables.

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        graphVars {list} -- variables to be plotted on the graph
        func {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
        variables {list} -- variables in given equation

    Note:
        The func obtained from graphPlot() funtion is of different type for 2D and 3D plots. For 2D func is a numpy array and for 3D func is a function.
    """
    tokens = workspace.eqToks[-1]
    axisRange = workspace.axisRange
    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(getVariables(LHStok, RHStok))
    dim = len(variables)
    if (dim == 1 and eqType == "expression") or (dim == 2 and eqType == "equation"):
        graphVars, func = plotIn2D(LHStok, RHStok, variables, axisRange)
        if dim == 1:
            variables.append('f(' + variables[0] + ')')
    elif (dim == 2 and eqType == "expression") or (dim == 3 and eqType == "equation"):
        graphVars, func = plotIn3D(LHStok, RHStok, variables, axisRange)
        if dim == 2:
            variables.append('f(' + variables[0] + ',' + variables[1] + ')')
    else:
        return [], None, None
    return graphVars, func, variables


def plotIn2D(LHStok, RHStok, variables, axisRange):
    """Returns function array for 2D plots

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        variables {list} -- variables in equation

    Returns:
        graphVars {list} -- variables for plotting
        func {numpy.array} -- equation to be plotted in 2D
    """
    xmin = -axisRange[0]
    xmax = axisRange[0]
    ymin = -axisRange[1]
    ymax = axisRange[1]
    xdelta = 0.01*(xmax-xmin)
    ydelta = 0.01*(ymax-ymin)
    xrange = np.arange(xmin, xmax, xdelta)
    yrange = np.arange(ymin, ymax, ydelta)
    graphVars = np.meshgrid(xrange, yrange)
    function = getFunction(LHStok, RHStok, variables, graphVars, 2)
    return graphVars, function


def plotIn3D(LHStok, RHStok, variables, axisRange):
    """Returns function for 3D plots

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        variables {list} -- variables in equation

    Returns:
        graphVars {list} -- variables for plotting
        func {function} -- equation to be plotted in 3D
    """

    xmin = -axisRange[0]
    xmax = axisRange[0]
    ymin = -axisRange[1]
    ymax = axisRange[1]
    zmin = -axisRange[2]
    zmax = axisRange[2]
    meshLayers = axisRange[3]
    xrange = np.linspace(xmin, xmax, meshLayers)
    yrange = np.linspace(ymin, ymax, meshLayers)
    zrange = np.linspace(zmin, zmax, meshLayers)
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
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ()]

    workspace.toolbar = NavigationCustomToolbar(workspace.canvas, workspace)
    layout = QVBoxLayout()
    layout.addWidget(workspace.canvas)
    layout.addWidget(workspace.toolbar)
    return layout


def plot(workspace):
    """Renders plot for functions in 2D and 3D

    Maps points from the numpy arrays for variables in given equation on the 2D/3D plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    graphVars, func, variables = graphPlot(workspace)
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
        axisRange = workspace.axisRange
        xmin = -axisRange[0]
        xmax = axisRange[0]
        ymin = -axisRange[1]
        ymax = axisRange[1]
        zmin = -axisRange[2]
        zmax = axisRange[2]
        ax.set_xlim3d(xmin, xmax)
        ax.set_ylim3d(ymin, ymax)
        ax.set_zlim3d(zmin, zmax)
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        ax.set_zlabel(r'$' + variables[2] + '$')
    workspace.canvas.draw()


def refreshPlot(workspace):
    if workspace.resultOut is True and workspace.showPlotter is True:
        plot(workspace)


###############
# preferences #
###############
# TODO: Add status tips, Fix docstrings

def plotPref(workspace):

    prefLayout = QVBoxLayout()

    workspace.xLimitValue = QLabel("X-axis range: (-" + str(workspace.axisRange[0]) + ", " + str(workspace.axisRange[0]) + ")")
    workspace.yLimitValue = QLabel("Y-axis range: (-" + str(workspace.axisRange[1]) + ", " + str(workspace.axisRange[1]) + ")")
    workspace.zLimitValue = QLabel("Z-axis range: (-" + str(workspace.axisRange[2]) + ", " + str(workspace.axisRange[2]) + ")")

    def customSlider():
        limitSlider = QSlider(Qt.Horizontal)
        limitSlider.setMinimum(-3)
        limitSlider.setMaximum(3)
        limitSlider.setValue(1)
        limitSlider.setTickPosition(QSlider.TicksBothSides)
        limitSlider.setTickInterval(1)
        limitSlider.valueChanged.connect(lambda: valueChange(workspace))
        return limitSlider

    workspace.xLimitSlider = customSlider()
    workspace.yLimitSlider = customSlider()
    workspace.zLimitSlider = customSlider()

    workspace.meshDensityValue = QLabel("Mesh Layers: " + str(workspace.axisRange[3]))
    workspace.meshDensity = QSpinBox()
    workspace.meshDensity.setRange(10, 50)
    workspace.meshDensity.setValue(25)
    workspace.meshDensity.valueChanged.connect(lambda: valueChange(workspace))
    workspace.note = QLabel("*Increment above value for a more dense mesh.")

    refreshPlotter = QPushButton('Apply')
    refreshPlotter.clicked.connect(lambda: refreshPlot(workspace))

    prefLayout.addWidget(workspace.xLimitValue)
    prefLayout.addWidget(workspace.xLimitSlider)
    prefLayout.addWidget(workspace.yLimitValue)
    prefLayout.addWidget(workspace.yLimitSlider)
    prefLayout.addWidget(workspace.zLimitValue)
    prefLayout.addWidget(workspace.zLimitSlider)
    prefLayout.addWidget(workspace.meshDensityValue)
    prefLayout.addWidget(workspace.meshDensity)
    prefLayout.addWidget(workspace.note)
    prefLayout.addWidget(refreshPlotter)

    return prefLayout


def valueChange(workspace):

    xlimit = 10**workspace.xLimitSlider.value()
    ylimit = 10**workspace.yLimitSlider.value()
    zlimit = 10**workspace.zLimitSlider.value()
    meshLayers = workspace.meshDensity.value()
    workspace.axisRange = [xlimit, ylimit, zlimit, meshLayers]

    workspace.xLimitValue.setText("X-axis range: (-" + str(workspace.axisRange[0]) + ", " + str(workspace.axisRange[0]) + ")")
    workspace.yLimitValue.setText("Y-axis range: (-" + str(workspace.axisRange[1]) + ", " + str(workspace.axisRange[1]) + ")")
    workspace.zLimitValue.setText("Z-axis range: (-" + str(workspace.axisRange[2]) + ", " + str(workspace.axisRange[2]) + ")")
    workspace.meshDensityValue.setText("Mesh Layers: " + str(workspace.axisRange[3]))
