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
    sizeChangeBox = QDoubleSpinBox()
    sizeChangeBox.setRange(0.1, 10)
    sizeChangeBox.setValue(1)
    sizeChangeBox.setSingleStep(0.1)
    sizeChangeBox.setSuffix('x')
    prefLayout.addWidget(workspace.sizeChangeText)
    prefLayout.addWidget(sizeChangeBox)
    sizeChangeBox.valueChanged.connect(lambda: sizeChange(workspace, sizeChangeBox))
    return prefLayout


def sizeChange(workspace, sizeChangeBox):
    workspace.sizeChangeText.setText("Font Size: " + str(round(sizeChangeBox.value(), 1)) + "x")
    workspace.fontPointSize = sizeChangeBox.value()
    showSteps(workspace)
