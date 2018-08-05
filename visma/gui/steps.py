from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, qApp, QLabel, QDoubleSpinBox

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

    stepslayout = QVBoxLayout()
    stepslayout.addWidget(workspace.stepscanvas)
    return stepslayout


def showSteps(workspace):
    """Renders step-by-step solution in matplotlib figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    workspace.stepsfigure.suptitle(workspace.output, y=0.98,
                                   horizontalalignment='center',
                                   verticalalignment='top', size=qApp.font().pointSize()*workspace.fontPointSize)
    workspace.stepscanvas.draw()


###############
# preferences #
###############


def stepsPref(workspace):

    prefLayout = QVBoxLayout()
    workspace.sizeChangeText = QLabel("Font Size: " + str(round(workspace.fontPointSize, 1)) + "x")
    workspace.sizeChangeBox = QDoubleSpinBox()
    workspace.sizeChangeBox.setRange(0.1, 10)
    workspace.sizeChangeBox.setValue(1)
    workspace.sizeChangeBox.setSingleStep(0.1)
    workspace.sizeChangeBox.setSuffix('x')
    prefLayout.addWidget(workspace.sizeChangeText)
    prefLayout.addWidget(workspace.sizeChangeBox)
    workspace.sizeChangeBox.valueChanged.connect(lambda: sizeChange(workspace))
    return prefLayout


def sizeChange(workspace):
    workspace.sizeChangeText.setText("Font Size: " + str(round(workspace.sizeChangeBox.value(), 1)) + "x")
    workspace.fontPointSize = workspace.sizeChangeBox.value()
    showSteps(workspace)
