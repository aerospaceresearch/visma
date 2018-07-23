from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets

#######
# GUI #
#######


def stepsFigure(workspace):
    workspace.stepsfigure = Figure()
    workspace.stepscanvas = FigureCanvas(workspace.stepsfigure)
    workspace.stepsfigure.clear()

    stepslayout = QtWidgets.QVBoxLayout()
    stepslayout.addWidget(workspace.stepscanvas)
    return stepslayout


def showSteps(workspace):
    workspace.stepsfigure.suptitle(workspace.output, y=0.98,
                                   horizontalalignment='center',
                                   verticalalignment='top')
    #                              size=qApp.font().pointSize()*1)
    workspace.stepscanvas.draw()
