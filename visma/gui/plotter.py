import numpy as np

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSlider, QSpinBox, QPushButton, QSplitter

from visma.io.checks import getVariables, getTokensType
from visma.io.tokenize import getLHSandRHS
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.functions.structure import FuncOp
from visma.functions.variable import Variable


def graphPlot(workSpace):
    """Function for plotting graphs in 2D and 3D space

    2D graphs are plotted for expression in one variable and equations in two variables. 3D graphs are plotted for expressions in two variables and equations in three variables.

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        graphVars {list} -- variables to be plotted on the graph
        func {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
        variables {list} -- variables in given equation

    Note:
        The func obtained from graphPlot() function is of different type for 2D and 3D plots. For 2D, func is a numpy array, and for 3D, func is a function.
    """
    tokens = workSpace.eqToks[-1]
    axisRange = workSpace.axisRange
    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(getVariables(LHStok, RHStok))
    dim = len(variables)
    if (dim == 1 and eqType == "expression") or ((dim == 2) and eqType == "equation"):
        graphVars, func = plotIn2D(LHStok, RHStok, variables, axisRange)
        if dim == 1:
            variables.append('f(' + variables[0] + ')')
    elif (dim == 2 and eqType == "expression") or ((dim == 3) and eqType == "equation"):
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
        axisRange {list} -- axis limits

    Returns:
        graphVars {list} -- variables for plotting
        func {numpy.array} -- equation to be plotted in 2D
    """
    xMin = -axisRange[0]
    xMax = axisRange[0]
    yMin = -axisRange[1]
    yMax = axisRange[1]
    xDelta = 0.01 * (xMax - xMin)
    yDelta = 0.01 * (yMax - yMin)
    xRange = np.arange(xMin, xMax, xDelta)
    yRange = np.arange(yMin, yMax, yDelta)
    graphVars = np.meshgrid(xRange, yRange)
    function = getFunction(LHStok, RHStok, variables, graphVars, 2)
    return graphVars, function


def plotIn3D(LHStok, RHStok, variables, axisRange):
    """Returns function for 3D plots

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        variables {list} -- variables in equation
        axisRange {list} -- axis limits

    Returns:
        graphVars {list} -- variables for plotting
        func {function} -- equation to be plotted in 3D
    """

    xMin = -axisRange[0]
    xMax = axisRange[0]
    yMin = -axisRange[1]
    yMax = axisRange[1]
    zMin = -axisRange[2]
    zMax = axisRange[2]
    meshLayers = axisRange[3]
    xRange = np.linspace(xMin, xMax, meshLayers)
    yRange = np.linspace(yMin, yMax, meshLayers)
    zRange = np.linspace(zMin, zMax, meshLayers)
    graphVars = [xRange, yRange, zRange]

    def func(x, y, z):
        tempGraphVars = [x, y, z]   # Changed GraphVars to tempGraphVars for readability.
        return getFunction(LHStok, RHStok, variables, tempGraphVars, 3)

    return graphVars, func


def getFunction(LHStok, RHStok, eqnVars, graphVars, dim):
    """Returns function for plotting

    Arguments:
        LHStok {list} -- expression tokens
        RHStok {list} -- expression tokens
        eqnVars {list} -- variables in equation
        graphVars {list} -- variables for plotting
        dim {int} -- dimension of plot

    Returns:
        (LHS - RHS) {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
    """


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
            expr += coeff * token.coefficient * varProduct
        elif isinstance(token, Constant):
            expr += coeff * token.value
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


def plotFigure2D(workSpace):
    """GUI layout for plot figure

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        layout {QtWidgets.QVBoxLayout} -- contains matplot figure
    """
    workSpace.figure2D = Figure()
    workSpace.canvas2D = FigureCanvas(workSpace.figure2D)
    # workSpace.figure2D.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolItems = [t for t in NavigationToolbar.toolitems if t[0] in ()]

    workSpace.toolbar2D = NavigationCustomToolbar(workSpace.canvas2D, workSpace)
    layout = QVBoxLayout()
    layout.addWidget(workSpace.canvas2D)
    layout.addWidget(workSpace.toolbar2D)
    return layout


def plotFigure3D(workSpace):
    """GUI layout for plot figure

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        layout {QtWidgets.QVBoxLayout} -- contains matplot figure
    """
    workSpace.figure3D = Figure()
    workSpace.canvas3D = FigureCanvas(workSpace.figure3D)
    # workSpace.figure3D.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolItems = [t for t in NavigationToolbar.toolitems if t[0] in ()]

    workSpace.toolbar3D = NavigationCustomToolbar(workSpace.canvas3D, workSpace)
    layout = QVBoxLayout()
    layout.addWidget(workSpace.canvas3D)
    layout.addWidget(workSpace.toolbar3D)
    return layout


def plot(workSpace):
    """Renders plot for functions in 2D and 3D

    Maps points from the numpy arrays for variables in given equation on the 2D/3D plot figure

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout
    """
    workSpace.figure2D.clear()
    workSpace.figure3D.clear()
    graphVars, func, variables = graphPlot(workSpace)
    if len(graphVars) == 2:
        X, Y = graphVars[0], graphVars[1]
        ax = workSpace.figure2D.add_subplot(111)
        ax.clear()
        ax.contour(X, Y, func, [0])
        ax.grid()
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        workSpace.figure2D.set_tight_layout({"pad": 1})  # removes extra padding
        workSpace.canvas2D.draw()
        workSpace.tabPlot.setCurrentIndex(0)
    elif len(graphVars) == 3:
        xRange = graphVars[0]
        yRange = graphVars[1]
        zRange = graphVars[2]
        ax = Axes3D(workSpace.figure3D)
        for z in zRange:
            X, Y = np.meshgrid(xRange, yRange)
            Z = func(X, Y, z)
            ax.contour(X, Y, Z + z, [z], zdir='z')
        for y in yRange:
            X, Z = np.meshgrid(xRange, zRange)
            Y = func(X, y, Z)
            ax.contour(X, Y + y, Z, [y], zdir='y')
        for x in xRange:
            Y, Z = np.meshgrid(yRange, zRange)
            X = func(x, Y, Z)
            ax.contour(X + x, Y, Z, [x], zdir='x')
        axisRange = workSpace.axisRange
        xMin = -axisRange[0]
        xMax = axisRange[0]
        yMin = -axisRange[1]
        yMax = axisRange[1]
        zMin = -axisRange[2]
        zMax = axisRange[2]
        ax.set_xlim3d(xMin, xMax)
        ax.set_ylim3d(yMin, yMax)
        ax.set_zlim3d(zMin, zMax)
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        ax.set_zlabel(r'$' + variables[2] + '$')
        workSpace.canvas3D.draw()
        workSpace.tabPlot.setCurrentIndex(1)


def refreshPlot(workSpace):
    if workSpace.resultOut is True and workSpace.showPlotter is True:
        plot(workSpace)


###############
# preferences #
###############
# TODO: Add status tips, Fix docstrings

def plotPref(workSpace):

    prefLayout = QSplitter(Qt.Horizontal)

    workSpace.xLimitValue = QLabel(
        "X-axis range: (-" + str(workSpace.axisRange[0]) + ", " + str(workSpace.axisRange[0]) + ")")
    workSpace.yLimitValue = QLabel(
        "Y-axis range: (-" + str(workSpace.axisRange[1]) + ", " + str(workSpace.axisRange[1]) + ")")
    workSpace.zLimitValue = QLabel(
        "Z-axis range: (-" + str(workSpace.axisRange[2]) + ", " + str(workSpace.axisRange[2]) + ")")

    def customSlider():
        limitSlider = QSlider(Qt.Horizontal)
        limitSlider.setMinimum(-3)
        limitSlider.setMaximum(3)
        limitSlider.setValue(1)
        limitSlider.setTickPosition(QSlider.TicksBothSides)
        limitSlider.setTickInterval(1)
        limitSlider.valueChanged.connect(lambda: valueChange(workSpace))
        limitSlider.setStatusTip("Change axes limit")
        return limitSlider

    workSpace.xLimitSlider = customSlider()
    workSpace.yLimitSlider = customSlider()
    workSpace.zLimitSlider = customSlider()

    workSpace.meshDensityValue = QLabel(
        "Mesh Layers: " + str(workSpace.axisRange[3]))
    workSpace.meshDensityValue.setStatusTip("Increment for a denser mesh in 3D plot")
    workSpace.meshDensity = QSpinBox()
    workSpace.meshDensity.setFixedSize(200, 30)
    workSpace.meshDensity.setRange(10, 75)
    workSpace.meshDensity.setValue(30)
    workSpace.meshDensity.valueChanged.connect(lambda: valueChange(workSpace))
    workSpace.meshDensity.setStatusTip("Incrementing mesh density may affect performance")

    refreshPlotterText = QLabel("Apply plotter settings")
    refreshPlotter = QPushButton('Apply')
    refreshPlotter.setFixedSize(200, 30)
    refreshPlotter.clicked.connect(lambda: refreshPlot(workSpace))
    refreshPlotter.setStatusTip("Apply modified settings to plotter.")

    axisPref = QSplitter(Qt.Vertical)
    axisPref.addWidget(workSpace.xLimitValue)
    axisPref.addWidget(workSpace.xLimitSlider)
    axisPref.addWidget(workSpace.yLimitValue)
    axisPref.addWidget(workSpace.yLimitSlider)
    axisPref.addWidget(workSpace.zLimitValue)
    axisPref.addWidget(workSpace.zLimitSlider)

    plotSetPref = QSplitter(Qt.Vertical)
    plotSetPref.addWidget(workSpace.meshDensityValue)
    plotSetPref.addWidget(workSpace.meshDensity)
    plotSetPref.addWidget(refreshPlotterText)
    plotSetPref.addWidget(refreshPlotter)

    prefLayout.addWidget(plotSetPref)
    prefLayout.addWidget(axisPref)
    prefLayout.setFixedWidth(400)

    return prefLayout


def valueChange(workSpace):

    xLimit = 10**workSpace.xLimitSlider.value()
    yLimit = 10**workSpace.yLimitSlider.value()
    zLimit = 10**workSpace.zLimitSlider.value()
    meshLayers = workSpace.meshDensity.value()
    workSpace.axisRange = [xLimit, yLimit, zLimit, meshLayers]

    workSpace.xLimitValue.setText(
        "X-axis range: (-" + str(workSpace.axisRange[0]) + ", " + str(workSpace.axisRange[0]) + ")")
    workSpace.yLimitValue.setText(
        "Y-axis range: (-" + str(workSpace.axisRange[1]) + ", " + str(workSpace.axisRange[1]) + ")")
    workSpace.zLimitValue.setText(
        "Z-axis range: (-" + str(workSpace.axisRange[2]) + ", " + str(workSpace.axisRange[2]) + ")")
    workSpace.meshDensityValue.setText(
        "Mesh Layers: " + str(workSpace.axisRange[3]))
