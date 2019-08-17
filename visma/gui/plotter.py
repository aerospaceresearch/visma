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


def graphPlot(workspace, again, tokens):
    """Function for plotting graphs in 2D and 3D space

    2D graphs are plotted for expression in one variable and equations in two variables. 3D graphs are plotted for expressions in two variables and equations in three variables.

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        graphVars {list} -- variables to be plotted on the graph
        func {numpy.array(2D)/function(3D)} -- equation converted to compatible data type for plotting
        variables {list} -- variables in given equation
        again {bool} -- True when an equation can be plotted in 2D and 3D both else False

    Note:
        The func obtained from graphPlot() function is of different type for 2D and 3D plots. For 2D, func is a numpy array, and for 3D, func is a function.
    """
    if tokens is None:
        axisRange = workspace.axisRange
        tokens = workspace.eqToks[-1]
    else:
        axisRange = [10, 10, 10, 30]
    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(getVariables(LHStok, RHStok))
    dim = len(variables)
    if (dim == 1) or ((dim == 2) and eqType == "equation"):
        if again:
            variables.append('f(' + variables[0] + ')')
            graphVars, func = plotIn3D(LHStok, RHStok, variables, axisRange)
        else:
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
    xmin = -axisRange[0]
    xmax = axisRange[0]
    ymin = -axisRange[1]
    ymax = axisRange[1]
    xdelta = 0.01 * (xmax - xmin)
    ydelta = 0.01 * (ymax - ymin)
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
        axisRange {list} -- axis limits

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


def plotFigure2D(workspace):
    """GUI layout for plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        layout {QtWidgets.QVBoxLayout} -- contains matplot figure
    """
    workspace.figure2D = Figure()
    workspace.canvas2D = FigureCanvas(workspace.figure2D)
    # workspace.figure2D.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ()]

    workspace.toolbar2D = NavigationCustomToolbar(workspace.canvas2D, workspace)
    layout = QVBoxLayout()
    layout.addWidget(workspace.canvas2D)
    layout.addWidget(workspace.toolbar2D)
    return layout


def plotFigure3D(workspace):
    """GUI layout for plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        layout {QtWidgets.QVBoxLayout} -- contains matplot figure
    """
    workspace.figure3D = Figure()
    workspace.canvas3D = FigureCanvas(workspace.figure3D)
    # workspace.figure3D.patch.set_facecolor('white')

    class NavigationCustomToolbar(NavigationToolbar):
        toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ()]

    workspace.toolbar3D = NavigationCustomToolbar(workspace.canvas3D, workspace)
    layout = QVBoxLayout()
    layout.addWidget(workspace.canvas3D)
    layout.addWidget(workspace.toolbar3D)
    return layout


def renderPlot(workspace, graphVars, func, variables, tokens=None):
    """Renders plot for functions in 2D and 3D

    Maps points from the numpy arrays for variables in given equation on the 2D/3D plot figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
        graphVars {list} -- variables for plotting
        dim {int} -- dimenion of plot
        variables {list} -- variables in equation
    """
    if len(graphVars) == 2:
        X, Y = graphVars[0], graphVars[1]
        ax = workspace.figure2D.add_subplot(111)
        ax.clear()
        ax.contour(X, Y, func, [0])
        ax.grid()
        ax.set_xlabel(r'$' + variables[0] + '$')
        ax.set_ylabel(r'$' + variables[1] + '$')
        workspace.figure2D.set_tight_layout({"pad": 1})  # removes extra padding
        workspace.canvas2D.draw()
        workspace.tabPlot.setCurrentIndex(0)
    elif len(graphVars) == 3:
        xrange = graphVars[0]
        yrange = graphVars[1]
        zrange = graphVars[2]
        ax = Axes3D(workspace.figure3D)
        for z in zrange:
            X, Y = np.meshgrid(xrange, yrange)
            Z = func(X, Y, z)
            ax.contour(X, Y, Z + z, [z], zdir='z')
        for y in yrange:
            X, Z = np.meshgrid(xrange, zrange)
            Y = func(X, y, Z)
            ax.contour(X, Y + y, Z, [y], zdir='y')
        for x in xrange:
            Y, Z = np.meshgrid(yrange, zrange)
            X = func(x, Y, Z)
            ax.contour(X + x, Y, Z, [x], zdir='x')
        if tokens is None:
            axisRange = workspace.axisRange
        else:
            axisRange = [10, 10, 10, 30]
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
        workspace.canvas3D.draw()
        workspace.tabPlot.setCurrentIndex(1)


def plot(workspace, tokens=None):
    """When called from window.py it initiates rendering of equations.

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    from visma.io.tokenize import tokenizer

    workspace.figure2D.clear()
    workspace.figure3D.clear()
    if tokens is None:
        tokens = workspace.eqToks[-1]
    eqType = getTokensType(tokens)
    LHStok, RHStok = getLHSandRHS(tokens)
    variables = sorted(getVariables(LHStok, RHStok))
    dim = len(variables)
    graphVars, func, variables = graphPlot(workspace, False, tokens)
    renderPlot(workspace, graphVars, func, variables, tokens)
    if (dim == 1):
        var2, var3 = selectAdditionalVariable(variables[0])
        if tokens is None:
            workspace.eqToks[-1] += tokenizer("0" + var2 + "+" + "0" + var3)
        else:
            tokens += tokenizer("0" + var2 + "+" + "0" + var3)
    if (((dim == 2) or (dim == 1)) & (eqType == 'equation')):
        graphVars, func, variables = graphPlot(workspace, True, tokens)
        renderPlot(workspace, graphVars, func, variables, tokens)


def selectAdditionalVariable(var1):
    if var1 == 'z':
        var2 = 'a'
        var3 = 'b'
        return var2, var3
    if var1 == 'Z':
        var2 = 'A'
        var3 = 'B'
        return var2, var3
    var2 = chr(ord(var1) + 1)
    var3 = chr(ord(var1) + 2)
    return var2, var3


def refreshPlot(workspace):
    if workspace.resultOut is True and workspace.showPlotter is True:
        plot(workspace)


###############
# preferences #
###############
# TODO: Add status tips, Fix docstrings

def plotPref(workspace):

    prefLayout = QSplitter(Qt.Horizontal)

    workspace.xLimitValue = QLabel(
        "X-axis range: (-" + str(workspace.axisRange[0]) + ", " + str(workspace.axisRange[0]) + ")")
    workspace.yLimitValue = QLabel(
        "Y-axis range: (-" + str(workspace.axisRange[1]) + ", " + str(workspace.axisRange[1]) + ")")
    workspace.zLimitValue = QLabel(
        "Z-axis range: (-" + str(workspace.axisRange[2]) + ", " + str(workspace.axisRange[2]) + ")")

    def customSlider():
        limitSlider = QSlider(Qt.Horizontal)
        limitSlider.setMinimum(-3)
        limitSlider.setMaximum(3)
        limitSlider.setValue(1)
        limitSlider.setTickPosition(QSlider.TicksBothSides)
        limitSlider.setTickInterval(1)
        limitSlider.valueChanged.connect(lambda: valueChange(workspace))
        limitSlider.setStatusTip("Change axes limit")
        return limitSlider

    workspace.xLimitSlider = customSlider()
    workspace.yLimitSlider = customSlider()
    workspace.zLimitSlider = customSlider()

    workspace.meshDensityValue = QLabel(
        "Mesh Layers: " + str(workspace.axisRange[3]))
    workspace.meshDensityValue.setStatusTip("Increment for a denser mesh in 3D plot")
    workspace.meshDensity = QSpinBox()
    workspace.meshDensity.setFixedSize(200, 30)
    workspace.meshDensity.setRange(10, 75)
    workspace.meshDensity.setValue(30)
    workspace.meshDensity.valueChanged.connect(lambda: valueChange(workspace))
    workspace.meshDensity.setStatusTip("Incrementing mesh density may affect performance")

    refreshPlotterText = QLabel("Apply plotter settings")
    refreshPlotter = QPushButton('Apply')
    refreshPlotter.setFixedSize(200, 30)
    refreshPlotter.clicked.connect(lambda: refreshPlot(workspace))
    refreshPlotter.setStatusTip("Apply modified settings to plotter.")

    axisPref = QSplitter(Qt.Vertical)
    axisPref.addWidget(workspace.xLimitValue)
    axisPref.addWidget(workspace.xLimitSlider)
    axisPref.addWidget(workspace.yLimitValue)
    axisPref.addWidget(workspace.yLimitSlider)
    axisPref.addWidget(workspace.zLimitValue)
    axisPref.addWidget(workspace.zLimitSlider)

    plotSetPref = QSplitter(Qt.Vertical)
    plotSetPref.addWidget(workspace.meshDensityValue)
    plotSetPref.addWidget(workspace.meshDensity)
    plotSetPref.addWidget(refreshPlotterText)
    plotSetPref.addWidget(refreshPlotter)

    prefLayout.addWidget(plotSetPref)
    prefLayout.addWidget(axisPref)
    prefLayout.setFixedWidth(400)

    return prefLayout


def valueChange(workspace):

    xlimit = 10**workspace.xLimitSlider.value()
    ylimit = 10**workspace.yLimitSlider.value()
    zlimit = 10**workspace.zLimitSlider.value()
    meshLayers = workspace.meshDensity.value()
    workspace.axisRange = [xlimit, ylimit, zlimit, meshLayers]

    workspace.xLimitValue.setText(
        "X-axis range: (-" + str(workspace.axisRange[0]) + ", " + str(workspace.axisRange[0]) + ")")
    workspace.yLimitValue.setText(
        "Y-axis range: (-" + str(workspace.axisRange[1]) + ", " + str(workspace.axisRange[1]) + ")")
    workspace.zLimitValue.setText(
        "Z-axis range: (-" + str(workspace.axisRange[2]) + ", " + str(workspace.axisRange[2]) + ")")
    workspace.meshDensityValue.setText(
        "Mesh Layers: " + str(workspace.axisRange[3]))
