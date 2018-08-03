from PyQt5.QtWidgets import QHBoxLayout, QRadioButton

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
    workspace.button1 = QRadioButton("Enable")
    workspace.button1.setChecked(True)
    workspace.button1.toggled.connect(lambda: buttonState(workspace.button1, workspace))
    hbox.addWidget(workspace.button1)

    workspace.button2 = QRadioButton("Disable")
    workspace.button2.toggled.connect(lambda: buttonState(workspace.button2, workspace))

    hbox.addWidget(workspace.button2)

    return hbox


def buttonState(button, workspace):
    """Takes action according to button and its state change trigger

    Arguments:
        button {QtWidgets.QRadioButton} -- preference button
        workspace {QtWidgets.QWidget} -- main layout
    """

    if button.text() == "Enable":
        if button.isChecked() is True:
            workspace.showQuickSim = True

    if button.text() == "Disable":
        if button.isChecked() is True:
            workspace.showQuickSim = False

    workspace.textedit.setText("")
