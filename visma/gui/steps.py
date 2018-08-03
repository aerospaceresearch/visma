from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

#######
# GUI #
#######


def stepsFigure(workspace):
    """GUI layout for step-by-step solution

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        stepslayout {QtWidgets.QVBoxLayout} -- step-by-step solution layout
    """
    workspace.stepsfigure = Figure()
    workspace.stepscanvas = FigureCanvas(workspace.stepsfigure)
    workspace.stepsfigure.clear()

    stepslayout = QtWidgets.QVBoxLayout()
    stepslayout.addWidget(workspace.stepscanvas)
    return stepslayout


def showSteps(workspace):
    """Renders step-by-step solution in matplotlib figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    workspace.stepsfigure.suptitle(workspace.output, y=0.98,
                                   horizontalalignment='center',
                                   verticalalignment='top')
    #                              size=qApp.font().pointSize()*1)
    workspace.stepscanvas.draw()
