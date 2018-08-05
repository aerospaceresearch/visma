from PyQt5.QtWidgets import QHBoxLayout, QCheckBox

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
    workspace.SSSCheckBox.setChecked(True)
    workspace.SSSCheckBox.toggled.connect(lambda: buttonState(workspace.SSSCheckBox, workspace))

    workspace.GPCheckBox = QCheckBox("Graph Plotter")
    workspace.GPCheckBox.setChecked(True)
    workspace.GPCheckBox.toggled.connect(lambda: buttonState(workspace.GPCheckBox, workspace))

    hbox.addWidget(workspace.QSCheckBox)  # Quick Simplifier
    hbox.addWidget(workspace.SSSCheckBox)  # Step-by-step Solution
    hbox.addWidget(workspace.GPCheckBox)  # Graph Plotter

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
            workspace.showQuickSim = True
        else:
            workspace.showQuickSim = False

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
