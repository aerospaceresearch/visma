from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, qApp, QLabel, QDoubleSpinBox, QScrollArea

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
    workspace.scroll = QScrollArea()
    workspace.scroll.setWidget(workspace.stepscanvas)
    stepslayout = QVBoxLayout()
    stepslayout.addWidget(workspace.scroll)
    return stepslayout


def showSteps(workspace):
    """Renders step-by-step solution in matplotlib figure

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout
    """
    workspace.stepsfigure.suptitle(workspace.output, y=0.98,
                                   horizontalalignment='center',
                                   verticalalignment='top', size=qApp.font().pointSize()*workspace.stepsFontSize)
    workspace.stepscanvas.draw()
    hbar = workspace.scroll.horizontalScrollBar()
    hbar.setValue((hbar.minimum()+hbar.maximum())/2)


###############
# preferences #
###############


def stepsPref(workspace):

    workspace.sizeChangeText = QLabel("Steps font size: " + str(round(workspace.stepsFontSize, 1)) + "x")
    workspace.sizeChangeBox = QDoubleSpinBox()
    workspace.sizeChangeBox.setFixedSize(200, 30)
    workspace.sizeChangeBox.setRange(0.1, 10)
    workspace.sizeChangeBox.setValue(1)
    workspace.sizeChangeBox.setSingleStep(0.1)
    workspace.sizeChangeBox.setSuffix('x')
    workspace.sizeChangeBox.valueChanged.connect(lambda: sizeChange(workspace))
    return workspace.sizeChangeText, workspace.sizeChangeBox


def sizeChange(workspace):
    workspace.stepsFontSize = workspace.sizeChangeBox.value()
    workspace.sizeChangeText.setText("Steps font size: " + str(round(workspace.stepsFontSize, 1)) + "x")
    if workspace.resultOut is True:
        showSteps(workspace)
