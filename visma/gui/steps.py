from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, qApp, QLabel, QDoubleSpinBox, QScrollArea

#######
# GUI #
#######


def stepsFigure(workSpace):
    """GUI layout for step-by-step solution

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        stepslayout {QtWidgets.QVBoxLayout} -- step-by-step solution layout
    """
    workSpace.stepsfigure = Figure()
    workSpace.stepscanvas = FigureCanvas(workSpace.stepsfigure)
    workSpace.stepsfigure.clear()
    workSpace.scroll = QScrollArea()
    workSpace.scroll.setWidget(workSpace.stepscanvas)
    stepslayout = QVBoxLayout()
    stepslayout.addWidget(workSpace.scroll)
    return stepslayout


def showSteps(workSpace):
    """Renders step-by-step solution in matplotlib figure

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout
    """
    workSpace.stepsfigure.suptitle(workSpace.output, y=0.98,
                                   horizontalalignment='center',
                                   verticalalignment='top', size=qApp.font().pointSize()*workSpace.stepsFontSize)
    workSpace.stepscanvas.draw()


###############
# preferences #
###############


def stepsPref(workSpace):

    workSpace.sizeChangeText = QLabel("Steps font size: " + str(round(workSpace.stepsFontSize, 1)) + "x")
    workSpace.sizeChangeBox = QDoubleSpinBox()
    workSpace.sizeChangeBox.setFixedSize(200, 30)
    workSpace.sizeChangeBox.setRange(0.1, 10)
    workSpace.sizeChangeBox.setValue(1)
    workSpace.sizeChangeBox.setSingleStep(0.1)
    workSpace.sizeChangeBox.setSuffix('x')
    workSpace.sizeChangeBox.valueChanged.connect(lambda: sizeChange(workSpace))
    return workSpace.sizeChangeText, workSpace.sizeChangeBox


def sizeChange(workSpace):
    workSpace.stepsFontSize = workSpace.sizeChangeBox.value()
    workSpace.sizeChangeText.setText("Steps font size: " + str(round(workSpace.stepsFontSize, 1)) + "x")
    if workSpace.resultOut is True:
        showSteps(workSpace)
