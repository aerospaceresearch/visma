from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QSplitter, QComboBox, QLabel
from PyQt5.QtCore import Qt

from visma.gui.steps import stepsPref
from visma.gui.plotter import plotPref

#######
# GUI #
#######


def preferenceLayout(workSpace):
    """GUI layout for preferences

    Arguments:
        workSpace {QtWidgets.QWidget} -- main layout

    Returns:
        hbox {QtWidgets.QHBoxLayout} -- preferences layout
    """

    hbox = QHBoxLayout()

    workSpace.QSCheckBox = QCheckBox("Quick Simplifier")
    workSpace.QSCheckBox.setChecked(True)
    workSpace.QSCheckBox.toggled.connect(lambda: buttonState(workSpace.QSCheckBox, workSpace))

    workSpace.SSSCheckBox = QCheckBox("Step-by-step Solution")
    workSpace.SSSCheckBox.setFixedSize(200, 30)
    workSpace.SSSCheckBox.setChecked(True)
    workSpace.SSSCheckBox.toggled.connect(lambda: buttonState(workSpace.SSSCheckBox, workSpace))

    workSpace.GPCheckBox = QCheckBox("Graph Plotter")
    workSpace.GPCheckBox.setChecked(False)
    workSpace.GPCheckBox.toggled.connect(lambda: buttonState(workSpace.GPCheckBox, workSpace))

    splitter1 = QSplitter(Qt.Vertical)
    splitter1.addWidget(workSpace.QSCheckBox)  # Quick Simplifier
    splitter1.addWidget(workSpace.SSSCheckBox)  # Step-by-step Solution
    splitter1.addWidget(workSpace.GPCheckBox)  # Graph Plotter

    # Input Type Box
    comboLabel = QLabel()
    comboLabel.setText("Input Type:")
    combo = QComboBox(workSpace)
    combo.setFixedSize(200, 30)
    combo.addItem("Greek")
    combo.addItem("LaTeX")
    combo.activated[str].connect(workSpace.onActivated)
    stepspref1, stepspref2 = stepsPref(workSpace)
    inputTypeSplitter = QSplitter(Qt.Vertical)
    inputTypeSplitter.addWidget(stepspref1)
    inputTypeSplitter.addWidget(stepspref2)
    inputTypeSplitter.addWidget(comboLabel)
    inputTypeSplitter.addWidget(combo)

    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(splitter1)
    splitter.addWidget(inputTypeSplitter)
    splitter.addWidget(plotPref(workSpace))

    hbox.addWidget(splitter)
    return hbox


def buttonState(button, workSpace):
    """Takes action according to button and its state change trigger

    Arguments:
        button {QtWidgets.QCheckBox} -- preference checkbox
        workSpace {QtWidgets.QWidget} -- main layout
    """

    workSpace.clearAll()

    if button.text() == "Quick Simplifier":
        if button.isChecked() is True:
            workSpace.showQSolver = True
        else:
            workSpace.showQSolver = False

    elif button.text() == "Step-by-step Solution":
        if button.isChecked() is True:
            workSpace.showStepByStep = True
        else:
            workSpace.showStepByStep = False

    elif button.text() == "Graph Plotter":
        if button.isChecked() is True:
            workSpace.showPlotter = True
        else:
            workSpace.showPlotter = False
