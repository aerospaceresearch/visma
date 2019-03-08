from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QSplitter, QComboBox, QLabel
from PyQt5.QtCore import Qt

from visma.gui.steps import stepsPref
from visma.gui.plotter import plotPref

#######
# GUI #
#######


def preferenceLayout(workspace):
    """GUI layout for preferences

    Arguments:
        workspace {QtWidgets.QWidget} -- main layout

    Returns:
        hbox {QtWidgets.QHBoxLayout} -- preferences layout
    """

    hbox = QHBoxLayout()

    workspace.QSCheckBox = QCheckBox("Quick Simplifier")
    workspace.QSCheckBox.setChecked(True)
    workspace.QSCheckBox.toggled.connect(lambda: buttonState(workspace.QSCheckBox, workspace))

    workspace.SSSCheckBox = QCheckBox("Step-by-step Solution")
    workspace.SSSCheckBox.setFixedSize(200, 30)
    workspace.SSSCheckBox.setChecked(True)
    workspace.SSSCheckBox.toggled.connect(lambda: buttonState(workspace.SSSCheckBox, workspace))

    workspace.GPCheckBox = QCheckBox("Graph Plotter")
    workspace.GPCheckBox.setChecked(False)
    workspace.GPCheckBox.toggled.connect(lambda: buttonState(workspace.GPCheckBox, workspace))

    splitter1 = QSplitter(Qt.Vertical)
    splitter1.addWidget(workspace.QSCheckBox)  # Quick Simplifier
    splitter1.addWidget(workspace.SSSCheckBox)  # Step-by-step Solution
    splitter1.addWidget(workspace.GPCheckBox)  # Graph Plotter

    # Input Type Box
    comboLabel = QLabel()
    comboLabel.setText("Input Type:")
    combo = QComboBox(workspace)
    combo.setFixedSize(200, 30)
    combo.addItem("Greek")
    combo.addItem("LaTeX")
    combo.activated[str].connect(workspace.onActivated)
    stepspref1, stepspref2 = stepsPref(workspace)
    inputTypeSplitter = QSplitter(Qt.Vertical)
    inputTypeSplitter.addWidget(stepspref1)
    inputTypeSplitter.addWidget(stepspref2)
    inputTypeSplitter.addWidget(comboLabel)
    inputTypeSplitter.addWidget(combo)

    splitter = QSplitter(Qt.Horizontal)
    splitter.addWidget(splitter1)
    splitter.addWidget(inputTypeSplitter)
    splitter.addWidget(plotPref(workspace))

    hbox.addWidget(splitter)
    return hbox


def buttonState(button, workspace):
    """Takes action according to button and its state change trigger

    Arguments:
        button {QtWidgets.QCheckBox} -- preference checkbox
        workspace {QtWidgets.QWidget} -- main layout
    """

    workspace.clearAll()

    if button.text() == "Quick Simplifier":
        if button.isChecked() is True:
            workspace.showQSolver = True
        else:
            workspace.showQSolver = False

    elif button.text() == "Step-by-step Solution":
        if button.isChecked() is True:
            workspace.showStepByStep = True
        else:
            workspace.showStepByStep = False

    elif button.text() == "Graph Plotter":
        if button.isChecked() is True:
            workspace.showPlotter = True
        else:
            workspace.showPlotter = False
